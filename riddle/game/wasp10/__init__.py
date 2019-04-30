import re
import functools

from flask import request, session, url_for
from textwrap import dedent as dd
from jinja2 import DictLoader, Environment

from riddle import urls
from riddle.utils import create_user, get_user, get_user_flag, add_help_message


env = Environment(
    loader = DictLoader({
        'global_macros': dd('''\
            {% macro open_question(field_name, placeholder="Write here your answer") %}
            <div>
                <div>{{ caller() }}</div>
                <div>
                    <label for="{{ field_name }}">Answer</label>
                    <input type="text" name="{{ field_name }}" placeholder="{{ placeholder }}">
                </div>
            </div>
            {% endmacro %}
            {% macro hidden_field(name, value) %}
            <input type="hidden" name="{{ name }}" value="{{ value }}" />
            {% endmacro %}
            {% macro submit_button(text="Submit") %}
            <div>
                <button type="submit">{{ text }}</button>
            </div>
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
            <div>User info: {{ user }}</div>
            {% block body %}{% endblock %}
            {{ add_help_message() }}
            </body>
            </html>'''),
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
        'std_stage': dd('''{% extends "form" %}
            {% from "global_macros" import open_question, submit_button, hidden_field %}
            {% block stage %}Stage {{ stage_num }}{% endblock %}
            {% block form %}
                {% for question in questions %}
                    {% call open_question(question.__name__, question.__annotations__.get('return', "Your answer here")) %}
                        {{ question.__doc__ }}
                    {% endcall %}
                {% endfor %}
                {{ hidden_field("stage", stage_num) }}
                {{ submit_button("Send") }}
            {% endblock %}'''),
    })
)


env.globals.update(url_for=url_for)
env.globals.update(add_help_message=add_help_message)



deadline = 'Saturday, May 4th'


def flexible_complex(s):
    """Converts to complex a number that is both x+yj and yj+x.
    Built-in complex() won't parse the second case.
    """
    m = re.match('()', s)


def validate(validator, strip=True, check_only=False, ignore_spaces=True):
    """Validate input by calling validator and returning None on exception.
    This decorator should be applied to question functions to ensure that
    given answer is of the expected type. If validator raises an exception,
    the decorated function will silently return None, as the input is
    considered invalid.
    If check_only is True, then the (bool) output of validator will be used to
    check if the validation passes or not.
    """
    spaces = re.compile(r'\s+')
    def _deco(f):
        @functools.wraps(f)
        def _func(ans):
            if strip:
                ans = ans.strip()
            if ignore_spaces:
                ans = re.sub(spaces, '', ans)
            try:
                if check_only:
                    if not validator(ans):
                        return None
                else:
                    ans = validator(ans)
            except:  # Catch all the exceptions!
                return None  # We count this answer as not given
            return f(ans)  # Call function outside the try-catch
        return _func
    return _deco


def request_value(key):
    """Retrieve a value from request arguments."""
    if key in request.form:
        return (request.form[key],)
    if key in request.args:
        return (request.args[key],)
    return ()


def make_entry_point(stage, questions, on_answer):
    """Help making a standard entry point with validated questions."""
    @urls.on_answer(redirect=on_answer)
    def _entry():
        user = get_user(session['user_id'])
        # Ensure we got an answer from the form
        if request_value("stage") == (str(stage),):
            # Evaluate answers
            answers = [None] * len(questions)
            for i, question in enumerate(questions):
                for answer in request_value(question.__name__):
                    answers[i] = question(answer)
                    print("Question", question.__name__, "was", "passed" if answers[i] else "failed")
            # Return 
            score = sum(bool(a) for a in answers)
            if get_user_flag(session['user_id'], 'sanity-status') is not None:
                score = 0
            return {
                'score': score,
                'answer': 'pass',  # Consider the stage solved
            }
        else:
            return {
                'content': env.from_string('{% extends "std_stage" %}').render(
                    questions=questions,
                    stage_num=stage,
                    user=user),
            }
    return _entry
