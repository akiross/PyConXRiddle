import logging
import pathlib
import functools
import importlib

from flask import Flask, session, request

from riddle import database
from riddle import cli
from riddle import utils

from riddle.utils import create_user, get_level_structure


def page_not_found(err):
    return "Apparently, someone did a mistake.", 404


def level_access_verification():
    """Return a message when user has no access to a requested level."""
    if session.get('user_id') is None:
        # Create a session if none was started yet
        session['user_id'] = create_user()
    # Ensure requested URL can be read
    accessed = request.path[1:]
    levels = get_level_structure()
    if accessed not in levels:
        return None  # Let this be handled by a 404
    print("USER PROGRESS:", utils.query_user_process(session['user_id']))


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
        utils.update_user_progress(session['user_id'], accessed)
        return resp

    return func_


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RIDDLE_CONFIG')

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
            app.logger.info(f"Registering module {mod_name} with route {route}")
            mod = importlib.import_module('.' + mod_name, 'riddle.game')
            app.add_url_rule(route, mod_name, entry_point(mod.entry))
        except AttributeError:
            app.logger.warning(f"Riddle {n} is missing entry point.")
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")

    return app
