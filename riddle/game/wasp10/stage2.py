"""This is a test level, still to be filled."""

import random

from jinja2 import Environment, Template
from flask import session, request

from riddle.utils import create_user, get_user

from . import env

from types import SimpleNamespace


entry_text = '''{% extends "form" %}
{% from "global_macros" import open_question, submit_button %}
{% block stage %}Stage 2{% endblock %}
{% block form %}
<div>Let's now proceed with some complex math.</div>
<form>
{% call open_question("q_math_1") %}Compute the modulo of $4+3j$?{% endcall %}
{% call open_question("q_math_2") %}Compute $(7+4j)\cdot(17-5j)${% endcall %}
{% call open_question("q_math_3") %}...{% endcall %}
{{ submit_button("Send") }}
</form>
{% endblock %}
<
'''


def entry():
    user = get_user(session['user_id'])
    page = {
        'next_page': '/wasp10/stage0',
        'deadline': 'DOMENICA ALLE 9:00',
    }
    return env.from_string(entry_text).render(page=page, user=user), False
