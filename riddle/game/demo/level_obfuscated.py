"""This is a test level, still to be filled."""

import random

from jinja2 import Template
from flask import session, request

from riddle.utils import create_user, get_user
from riddle.urls import add_encoded_route


entry_text = '''<h1>Obfuscated Level</h1>
<h2>User {{user.name}} (id {{user.id}}), you accessed with {{passcode}}</h2>
'''


# Obfuscate level name by inverting the order of its name
@add_encoded_route('/{name}/<passcode>', lambda x: x[::-1])
def entry(passcode):
    user = get_user(session['user_id'])
    return Template(entry_text).render(user=user, passcode=passcode), False
