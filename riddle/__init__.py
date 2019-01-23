import logging
import pathlib
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
            app.route(route, endpoint=mod_name)(mod.entry)
        except AttributeError:
            app.logger.warning(f"Riddle {n} is missing entry point.")
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")

    return app
