"""This is a test level, still to be filled."""

import random

from jinja2 import Template
from flask import session, request

from riddle.utils import create_user, get_user


entry_text = '''<h1>Level 1: testlevel</h1>
<h2>Welcome, user {{user.name}} (id {{user.id}})</h2>
This is what you see when the user accesses the level.

Now, other things must be done: once you show the level, you need to give some
hints to the user. For example, the hint to solve this riddle is that the user
needs to give two numbers such that when summed they are not five.

After the hint we will need a way to check the results.

The most basic thing we can provide, is a field for the answer:
<form method=GET>
    (Comma separated) <input name="answer"></input>
    <input type="submit" value="Send!"></input>
</form>
'''


success_text = '''Congratulations, you did it! That was the right answer, and
you are collecting 2 points.'''


fail_text = '''I am sorry, but this is not correct... Try again, please!'''


def entry():
    if 'answer' in request.args:
        return verify(request.args.get('answer'))

    user = get_user(session['user_id'])
    return Template(entry_text).render(user=user), False
    # return f'{entry_text}\n Your user_id is {session["user_id"]}', False


def verify(ans):
    try:
        a, b, *r = map(int, map(str.strip, ans.split(',')))
        if a + b != 5:
            return success_text, True
    except:
        pass
    return fail_text, False
