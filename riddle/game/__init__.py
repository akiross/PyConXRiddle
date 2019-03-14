"""This is the home page"""

import random

from jinja2 import Template
from flask import session

from riddle.utils import get_user


entry_text = '''<h1>Home Page!</h1>
<h2>Welcome, user {{user.name}} (id {{user.id}})</h2>
'''


def entry():
    user = get_user(session['user_id'])
    return Template(entry_text).render(user=user), False

