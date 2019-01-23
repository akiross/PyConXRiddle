import logging
import pathlib
import importlib

from flask import Flask, session, request

from riddle import database
from riddle import cli

from riddle.utils import create_user, get_level_structure


def page_not_found(err):
    return "Apparently, someone did a mistake.", 404


def level_access_verification():
    """Return a message when user has no access to a requested level."""
    print("Request is", request.path)
    print("Level structure is", get_level_structure())
    #if session.get('user_id') is None:
    #    session['user_id'] = create_user()
    #    return "Sorry but you cannot ahahah"


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RIDDLE_CONFIG')

    app.register_error_handler(404, page_not_found)
    app.teardown_appcontext(database.close_connection)
    app.cli.add_command(cli.init_db)

    app.before_request(level_access_verification)

    levels = pathlib.Path(__file__).parent / 'game'
    for n in levels.glob('*.py'):
        try:
            app.logger.info(f"Registering module {n.stem}")
            mod = importlib.import_module('.' + n.stem, 'riddle.game')
            app.route('/' + n.stem)(mod.entry)
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")

    return app
