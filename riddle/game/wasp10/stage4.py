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
<p>Alright, you completed the preliminary parts of the challenge and we
are now entering the final phase: from now on, no errors are allowed. If you
answer incorrectly, you will not be able to continue the challenge.</p>
<p>You will still be able to review your answer before submitting.</p>
<form>
{% call open_question("q_final_1") %}What is the sum of the first 500 odd numbers?{% endcall %}
{{ submit_button("Proceed") }}
</form>
{% endblock %}
</form>
'''

confirm_text = '''{% extends "form" %}
<form>
<p>Your answer is:</p>
<p>{{ page.answer }}</p>
<p>Is this correct?</p>
</form>
'''


def entry():
    user = get_user(session['user_id'])
    page = {
        'next_page': '/wasp10/stage0',
        'deadline': 'DOMENICA ALLE 9:00',
    }
    if 'q_final_1' in request.args:
        page['answer'] = 123
        return env.from_string(confirm_text).render(page=page, user=user), False
    return env.from_string(entry_text).render(page=page, user=user), False
