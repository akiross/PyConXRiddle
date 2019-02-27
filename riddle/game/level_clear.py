"""This is a test level, still to be filled."""

import random

from jinja2 import Template
from flask import session, request

from riddle.utils import create_user, get_user
from riddle.urls import add_route


entry_text = '''<h1>Cleartext Level</h1>
<h2>User {{user.name}} (id {{user.id}}), you accessed with {{passcode}}</h2>
'''

@add_route('/textclear', endpoint='testochiaro', defaults={'passcode': 'foobar'})
@add_route('/cleartext/<passcode>', endpoint='cleartext')
def entry(passcode):
    user = get_user(session['user_id'])
    return Template(entry_text).render(user=user, passcode=passcode), False
