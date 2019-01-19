import click
import flask

from riddle import database


@click.command('init-db')
@flask.cli.with_appcontext
def init_db():
    """Clear the existing data and create new tables."""
    database.init()
    click.echo('Initialized the database.')
