"""This is a test level, still to be filled."""

import random

from jinja2 import Environment, Template
from flask import session, request

from riddle.utils import create_user, get_user

from . import env

from types import SimpleNamespace


entry_text = '''{% extends "form" %}
{% from "global_macros" import open_question, submit_button %}
{% block stage %}Stage 1{% endblock %}
{% block form %}

<form>
{% call open_question("q_math_1") %}Compute 2<sup>38</sup>{% endcall %}
{% call open_question("q_math_2") %}Given the equation $$y = (log(4 * x + 1) * x) / log(9 * x**2 * e**x)$$ please compute $y$ when $x=42$.{% endcall %}
{% call open_question("q_math_3") %}Given this function, evaluate for $x={0, 2, 4, ...}${% endcall %}
{{ submit_button("Send") }}
</form>
{% endblock %}
<
'''


def entry():
    user = get_user(session['user_id'])
    page = {
        'next_page': '/wasp10/stage2',
        'deadline': 'DOMENICA ALLE 9:00',
    }
    return env.from_string(entry_text).render(page=page, user=user), False
