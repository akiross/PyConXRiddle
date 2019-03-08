from textwrap import dedent as dd
from jinja2 import DictLoader, Environment


env = Environment(
    loader = DictLoader({
        'global_macros': dd('''\
                {% macro open_question(field_name, placeholder="Write here your answer") %}
                <div>
                <div>{{ caller() }}</div>
                <div><label for="{{field_name}}">Answer</label>
                <input type="text" placeholder="{{ placeholder }}"></div>
                </div>
                {% endmacro %}
                {% macro submit_button(text="Submit") %}
                <div><button type="submit">{{ text }}</button></div>
                {% endmacro %}'''),
        'base': dd('''\
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{% block title %}{% endblock %}</title>
            </head>
            <body>
            {% block body %}{% endblock %}
            </body>
            <html>'''),
        'form': dd('''\
            {% extends "base" %}
            {% block title %}10th WASP10 Competition - {% block stage %}{% endblock %}{% endblock %}
            {% block body %}
            <h1>10<sup>th</sup> WASP<sup>10</sup> Competition - {{ self.stage() }}</h1>
            <h2>{% block description %}{% endblock %}</h2>
            <form>
            {% block form %}{% endblock %}
            </form>
            {% endblock %}'''),
    })
)
