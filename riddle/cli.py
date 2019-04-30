import json
import time

import click
import flask
from PIL import Image

from riddle import database
from riddle.tools import (
    make_ith_bit_writer, write_to_image_bit,
    make_highly_variable_graph, calculate_graph_longest_path
)


@click.command('init-db')
@flask.cli.with_appcontext
def init_db():
    """Clear the existing data and create new tables."""
    database.init()
    click.echo('Initialized the database.')


@click.command('write-stega-image')
@click.option('-m', '--message', type=str, required=True)
@click.option('-s', '--img-source-path', type=click.Path(), required=True)
@click.option('-d', '--img-dest-path', type=click.Path(), required=True)
@flask.cli.with_appcontext
def write_stega_image(message, img_source_path, img_dest_path):
    img = Image.open(img_source_path)
    msb_writer = make_ith_bit_writer(5)
    img2 = write_to_image_bit(img, message.encode(), msb_writer)
    img2.save(img_dest_path)
    click.echo(f'new image saved to {img_dest_path}')


@click.command('populate-longest-path')
@click.option('-n', type=int, default=25)
@click.option('-m', type=int, default=19)
@flask.cli.with_appcontext
def populate_longest_path(n, m):
    db = database.get_connection()
    for i in range(n):
        while True:
            t0 = time.time()
            graph = make_highly_variable_graph(m)
            length = calculate_graph_longest_path(graph)
            elapsed = time.time() - t0
            click.echo(f'processing graph {i} found path in {elapsed}')
            if elapsed >= 0.1:
                break
            print('skipping graph: solved too fast')
        graph = json.dumps({k: list(v) for k, v in graph.items()})
        db.execute(
            'INSERT INTO longest_path (graph, len) VALUES (?,?)',
            [graph, length]
        )
        db.commit()