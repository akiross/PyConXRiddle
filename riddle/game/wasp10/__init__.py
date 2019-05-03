import re
import random
import functools

from flask import request, session, url_for, current_app
from textwrap import dedent as dd
from jinja2 import DictLoader, Environment

from riddle import urls
from riddle.utils import create_user, get_user, get_user_flag
from riddle.tools import rot13


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
                <hr/>
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
            <script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML' async></script>
            <!-- https://motherfuckingwebsite.com/ -->
            </head>
            <body>
            {% block body %}{% endblock %}
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
                {% set text = add_help_message() %}
                {% if text %}
                {{ text }}
                <div>
                    &lt;button type="submit"&gt;Send&lt;/
                {% else %}
                {{ submit_button("Send") }}
                {% endif %}
            {% endblock %}'''),
    })
)


help_message = rot13('''\
We managed to inject this message in the unencrypted communication with
the server, but the message might be garbled due to self-defensive
systems.
This is a pledge for help: the WASP10 challenge is staged by an
Evolutionary Artificial Intelligence which took over the WASP10 council.
All us members of the WASP10 are being isolated in any possible way and
none of our messages is going through, but this one.
We hope you found and read this message, because someone hacking
in the system and shutting down the AI is our only hope. The AI is
probably planning to start a global-scale cyber attack aimed to shut
down human digital communications: if it succeeds, it will be chaos.
We are sure that the attack will start on a smaller scale, trying to
interfere with an event which is running *right now* and where many
talented hackers are found, the PyConX Italia. By isolating them, the
AI probably hopes to have and advantage by excluding some of its most
threatening opponents.
But if we stop the AI during this attack to the PyConX, we might be
able to stop it before the global-scale attack starts!
We believe the server where the WASP10 challenge is hosted is the only
public interface of the AI with the world, so we must start from there.
We are sure the system is simple, but robust, and there is not an easy
access, but apparently there are some old entry-points previously used
for computing the statistics of the WASP9 challenge that could be used
to break in. Find them and do your best! We will try to support you
whenever possible, keep your eyes open and send us any relevant message
you find!'''.strip())


def add_help_message():
    # could also check if sanity is tainted
    user_flag = get_user_flag(session['user_id'], 'sanity-status')
    if not random.randint(0, 1) and user_flag is not None:
        return f'<!--\n{help_message}\n-->'
    return ''


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
                    try:
                        answers[i] = question(answer)
                    except:
                        # In case of exception, assume it is not passed
                        current_app.logger.warn(f"Error while checking answer '{answer}' in question {question.__name__}")
                        answers[i] = False
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
