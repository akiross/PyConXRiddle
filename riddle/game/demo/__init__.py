"""This module can be used to provide tools for other modules in this level."""

from flask import url_for
from textwrap import dedent
from jinja2 import Environment, DictLoader


# You can keep a Jinja environment with multiple templates
env = Environment(
    loader=DictLoader({
        'base': dedent('''\
            <!doctype html>
            <html>
                <head><title>Hello there!</title></head>
            <body>
                {% block body %}{% endblock %}
            </body>
            </html>'''),
        })
)

# You might want to register useful functions
env.globals.update(url_for=url_for)
