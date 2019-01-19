"""This is a test level, still to be filled."""

import random


entry_text = '''This is what you see when the user accesses the level.

Now, other things must be done: once you show the level, you need to give some
hints to the user. For example, the hint to solve this riddle is that the user
needs to sum two numbers such that their reminder is not five.

After the hint we will need a way to check the results.
'''


success_text = '''Congratulations, you did it! That was the right answer, and
you are collecting 2 points.'''


fail_text = '''I am sorry, but this is not correct... Try again, please!'''


def entry():
    return entry_text


def verify():
    if random.random() < 0.25:
        return success_text
    return fail_text

