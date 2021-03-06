import logging
import functools
import importlib
import pathlib
import sys


from flask import Flask, session, request, redirect, current_app

from riddle import database
from riddle import cli
from riddle import utils

__version__ = '1.0.0-dev'


def page_not_found(err):
    return "Apparently, someone did a mistake (404).", 404


def user_not_allowed(err):
    return "You can't touch this (403).", 403


def get_routes():
    level_map = current_app.config['level_map']
    # Create a map from routes to level files
    return {r: l for l in level_map for r in level_map[l]}


def level_access_verification():
    """Return a message when user has no access to a requested level."""
    current_app.logger.debug("Checking user accessing")
    # If user does not exist, create a new one
    user = session.get('user_id')
    if user is None:
        current_app.logger.info("No user in session, creating a new user")
        session['user_id'] = utils.create_user()

    # Ensure requested URL can be read
    accessed = request.path[1:]
    current_app.logger.debug(f"Requested path: {accessed}")
    levels = [str(l) for l in utils.get_level_structure()]
    # We might get a request for a mapped entry point
    routes = get_routes()
    
    if '/'+accessed not in routes:
        current_app.logger.info("Cannot find level, should be 404")
        return None  # Let this be handled by a 404

    if current_app.config.get('UNCONFINED', False):
        current_app.logger.warn("Unconfined access enabled")
        return None

    # Query user progress and check permissions
    progress = list(p[:2] for p in utils.query_user_progress(session['user_id']))
    current_app.logger.debug(f"Player progress {progress}")
    user_allowed = utils.is_user_allowed(routes['/'+accessed], progress)
    if not user_allowed:
        current_app.logger.info("User is not allowed")
        return user_not_allowed(None)
    return None  # Proceed as usual


def entry_point(func):
    """Decorator for the riddle entry points.

    Take cares of marking a riddle as solved and adding user score. The entry
    point shall return a dictionary with these optional keys:

     - content: the content to display
     - redirect: url of the page to be redirected with a 303
     - score: how many points to assign the user 
     - answer: None, 'fail' or 'pass' depending on the answer outcome

    At least one of content and redirect must be provided, but redirect has the
    precedence over the content rendering.
    answer can be None, meaning that the page rendering carries no info about
    user answer, in this case user progress nor score is updated.
    score defaults to 1 when answer is pass and 0 when fail.
    """
    @functools.wraps(func)
    def func_(*args, **kwargs):
        accessed = request.path[1:]
        
        # No pass/fail flags by default
        pf_flags = None
        target = None

        # Functions must return a dictionary
        resp = func(*args, **kwargs)
        answer_given = 'answer' in resp
        if answer_given:
            # An answer was given, get pass/fail flags
            if resp['answer'] in ['pass', True, 1]:
                if hasattr(func, 'on_success'):
                    target, score = getattr(func, 'on_success')
                else:
                    score = 1
            elif resp['answer'] in ['fail', False, 0]:
                if hasattr(func, 'on_failure'):
                    target, score = getattr(func, 'on_failure')
                else:
                    score = 0
            else:
                raise ValueError("Answer should be pass or fail")
 
        # Overrides
        if 'score' in resp:
            score = resp['score']
        if 'redirect' in resp:
            target = resp['redirect']

        # If answer was given, save progress
        if answer_given:
            # There are other levels that are set passed at the same time
            force = getattr(func, 'twins', None) is not None
            if force:
                for twin in getattr(func, 'twins'):
                    print("Setting twin level as solved", accessed)
                    utils.update_user_progress(session['user_id'], twin, 0)

            print("Setting level as solved", accessed, score)
            routes = get_routes()
            if '/'+accessed in routes:
                accessed = get_routes()['/'+accessed]
            utils.update_user_progress(session['user_id'], accessed, score, force_score=True)

        # Redirect if necessary
        if target:
            return redirect(target, code=303)
        return resp['content']

    return func_


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_envvar('RIDDLE_CONFIG')

    app.static_folder = app.config.get('STATIC_PATH', 'static')
    app.add_url_rule(
        f'/static/<path:filename>',
        endpoint='static',
        view_func=app.send_static_file)

    # Register default error handlers
    # TODO custom error handlers shall be in riddle.game.__init__
    app.register_error_handler(404, page_not_found)

    app.teardown_appcontext(database.close_connection)
    app.cli.add_command(cli.init_db)
    app.cli.add_command(cli.write_stega_image)
    app.cli.add_command(cli.populate_longest_path)

    app.before_request(level_access_verification)

    level_map = {}
    game_path = app.config.get('GAME_PATH')
    if game_path is not None:
        sys.path.append(game_path)
    else:
        game_path = pathlib.Path(__file__).parent
        app.config['GAME_PATH'] = game_path
    root, level_files = utils.get_level_files(game_path)

    for n in level_files:
        try:
            if utils.is_dunder(n):
                # Dunder files are special, TODO
                app.logger.warning(f"Found dunder {n}")
                continue
            # Regular files are levels to be registered
            path, mod_name = utils.get_level_pathname(n, root)
            app.logger.debug(f"Processing riddle file {path}")
            mod = importlib.import_module('.' + mod_name, 'riddle.game')
            mod.entry.is_entry_point = True  # Mark this as entry point
            # Each entry point might have multiple associated rules
            for rule, options in utils.get_level_routes(path, mod.entry):
                options['view_func'] = entry_point(mod.entry)
                app.logger.info(f"Registering module {mod_name} with route {rule}")
                app.add_url_rule(rule, **options)
                level_map.setdefault(str(path), []).append(rule)
        except AttributeError:
            app.logger.warning(f"Riddle {n} is missing entry point.")
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")
    app.config['level_map'] = level_map
    return app


if __name__ == '__main__':
    create_app().run(port=5001, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
