import importlib
import pathlib

from flask import Flask

from riddle import database
from riddle import cli


def page_not_found(err):
    return "Apparently, someone did a mistake.", 404


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RIDDLE_CONFIG')

    app.register_error_handler(404, page_not_found)
    app.teardown_appcontext(database.close_connection)
    app.cli.add_command(cli.init_db)

    levels = pathlib.Path(__file__).parent / 'game'
    for n in levels.glob('*.py'):
        try:
            mod = importlib.import_module('.' + n.stem, 'riddle.game')
            app.route('/' + n.stem)(mod.entry)
        except Exception as e:
            app.logger.exception(f"Unable to load module {n}: {e}")

    return app
