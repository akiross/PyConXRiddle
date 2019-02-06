import logging
import pathlib
import functools
import importlib

from flask import Flask, session, request

from riddle import database
from riddle import cli
from riddle import utils

__version__ = '0.2.0-dev'

def page_not_found(err):
    return "Apparently, someone did a mistake.", 404


def user_not_allowed(err):
    return "You can't touch this.", 403


def level_access_verification():
    """Return a message when user has no access to a requested level."""
    # If user does not exist, create a new one
    user = utils.get_user(session['user_id'])
    if user is None:
        session['user_id'] = utils.create_user()

    # Ensure requested URL can be read
    accessed = request.path[1:]
    levels = utils.get_level_structure()
    if accessed not in levels:
        return None  # Let this be handled by a 404
    # Query user progress and check permissions
    progress = utils.query_user_progress(session['user_id'])
    user_allowed = utils.is_user_allowed(accessed, progress)
    if not user_allowed:
        return user_not_allowed(None)
    return None  # Proceed as usual


def entry_point(func):
    """Decorator for the riddle entry points.

    Take cares of marking a riddle as solved when the second return
    value of func is True.
    """
    @functools.wraps(func)
    def func_(*args, **kwargs):
        accessed = request.path[1:]
        # Functions must return two values: response and riddle solved status
        resp, solved = func(*args, **kwargs)
        if not solved:
            return resp
        # Mark riddle as solved
        logging.info(f"User solved the riddle {accessed}") # Not idiomatic FIXME
        utils.update_user_progress(session['user_id'], accessed)
        return resp

    return func_


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RIDDLE_CONFIG')

    # Register default error handlers
    # TODO custom error handlers shall be in riddle.game.__init__
    app.register_error_handler(404, page_not_found)

    app.teardown_appcontext(database.close_connection)
    app.cli.add_command(cli.init_db)

    app.before_request(level_access_verification)

    root, level_files = utils.get_level_files()
    for n in level_files:
        try:
            name = n.relative_to(root).parent / n.stem
            app.logger.debug(f"Processing riddle file {name}")
            mod_name = str('.'.join(name.parts))
            route = '/' + str(name)
            mod = importlib.import_module('.' + mod_name, 'riddle.game')
            app.logger.info(f"Registering module {mod_name} with route {route}")
            app.add_url_rule(route, mod_name, entry_point(mod.entry))
        except AttributeError:
            app.logger.warning(f"Riddle {n} is missing entry point.")
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")

    return app
