from flask import session

from riddle.urls import add_route, on_success
from riddle.utils import get_user, get_user_flag, set_user_flag
from riddle.tools import rot13

from . import env, request_value, deadline

from types import SimpleNamespace


entry_text = '''{% extends "form" %}
{% from "global_macros" import open_question, submit_button, hidden_field %}
{% block stage %}Stage {{ stage_num }}{% endblock %}
{% block form %}
    <p>Alright, you completed the preliminary parts of the challenge and we
    are now entering the final phase: from now on, no errors are allowed. If you
    answer incorrectly, you will not be able to continue the challenge.</p>
    <p>You will still be able to review your answer before submitting.</p>
    {% call open_question("q_final_1") -%}
        What is the sum of the first 500 odd numbers?
    {%- endcall %}
    {{ hidden_field("stage", stage_num) }}
    {{ submit_button("Proceed") }}
{% endblock %}
'''


confirm_text = '''{% extends "form" %}
{% from "global_macros" import open_question, submit_button, hidden_field %}
{% block stage %}Stage {{ stage_num }}{% endblock %}
{% block form %}
    <p>Your answer is:</p>
    <p>{{ page.answer }}</p>
    <p>Is this correct?</p>
    {{ hidden_field("final_answer", page.true_answer) }}
    {{ hidden_field("stage", stage_num) }}
    {{ submit_button("Confirm and proceed") }}
    <a href="javascript:history.back()">Go Back</a>
    {{ page.hidden }}
{% endblock %}
'''


closing_text = '''
<h1>Thanks for playing!</h1>
<p>The challenge is over, thanks for playing. We hope you enjoyed this
challenge and hope to see you the next time.</p>
<p>Since there are some other people still participating in this challenge,
we are unable to give you your score right now: that would provide a way to
guess the correctness of your answers. The results will be published at the
date indicated below.</p>
<p>{{ page.deadline }}</p>
'''

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


@add_route(None, methods=['GET', 'POST'])
@on_success(score=10)  # redirect='/wasp10/stage0', score=10)
def entry():
    # Page information to display
    page = {
        'deadline': deadline,
    }
    # Retrieve user id
    user = get_user(session['user_id'])
    print("Retrieving user ID", user)

    # Retrieve user status
    status_key = f"{__name__}/status"
    progress_status = get_user_flag(user['id'], status_key)
    print("User flag", progress_status)

    # Get answer from form
    for answer in request_value('q_final_1'):
        # Normally, we would show his answer for confirmation
        page['answer'] = answer
        page['true_answer'] = answer  # When confirming use the real answer
        if progress_status is None:  # or True:  # FIXME this is for debugging
            # The first time user sends the data, we show the help message
            set_user_flag(user['id'], status_key, 'tainted')
            page['answer'] = 'help!'
            page['hidden'] = f'<!--\n{help_message}\n-->'
        elif progress_status == 'tainted':
            # The second time, user will not see help message anymore
            set_user_flag(user['id'], status_key, 'cleared')
        return {
            'content': env.from_string(confirm_text).render(page=page,
                                                            user=user,
                                                            stage_num=4)
        }

    # When user confirms the final answer, we check its correctness and score
    for answer in request_value('final_answer'):
        return {
            'answer': 'pass' if verify(answer) else 'fail',
            'content': env.from_string(closing_text).render(page=page,
                                                            user=user,
                                                            stage_num=4),
        }

    return {
        'content': env.from_string(entry_text).render(page=page,
                                                      user=user,
                                                      stage_num=4)
    }


def verify(answer):
    try:
        return int(answer.strip()) == 500 * 500
    except Exception:
        return False  # Any invalid input is no good
