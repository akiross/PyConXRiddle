"""This is a test level, still to be filled."""

import random

from flask import session

from riddle.utils import create_user


entry_text = '''<h1>Level 2: testlevel-2</h1>
This is what you see when the user accesses the level.

Now, other things must be done: once you show the level, you need to give some
hints to the user. For example, the hint to solve this riddle is that the user
needs to sum two numbers such that their reminder is not five.

After the hint we will need a way to check the results.
'''


def entry():
    if session.get('user_id') is None:
        session['user_id'] = create_user()
    return {
        'content': f'{entry_text}\n Your user_id is {session["user_id"]}',
    }
