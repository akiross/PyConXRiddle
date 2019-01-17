import logging
import importlib
from flask import Flask
from pathlib import Path


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # from . import challenge
    # app.register_blueprint(challenge.bp)
    # app.add_url_rule('/', endpoint='index')

    @app.errorhandler(404)
    def page_not_found(err):
        return "Apparently, someone did a mistake.", 404
    
    levels = Path(__file__).parent / 'game'
    for n in levels.glob('*.py'):
        try:
            mod = importlib.import_module('.' + n.stem, 'riddle.game')
            app.route('/' + n.stem)(mod.entry)
        except:
            logging.exception(f"Unable to load module {n}")

    return app
