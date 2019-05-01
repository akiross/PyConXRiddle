import json

from flask import session, current_app, redirect

from riddle.urls import add_route, on_success
from riddle.utils import (
    get_user, get_user_flag, set_user_flag,
    get_graph
)

from . import env, request_value


entry_text = '''{% extends "form" %}
{% from "global_macros" import open_question, submit_button, hidden_field %}
{% block stage %}Stage {{ stage_num }}{% endblock %}
{% block form %}
    <p>Alright, you completed the preliminary parts of the challenge and we
    are now entering the final phase: from now on, no errors are allowed. If you
    answer incorrectly, you will not be able to continue the challenge.</p>
    <p>You will still be able to review your answer before submitting.</p>
    {% call open_question("q_final_1") -%}
        <p>Please compute the distance between 0 and most distant edge of this graph:</p>
        <pre>{%- for k, v in graph.items() %}{{k}} → {% for el in v %}{{el}} {% endfor %}
{% endfor %}</pre>
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
    <p>{{ answer }}</p>
    <p>Is this correct?</p>
    {{ hidden_field("final_answer", answer) }}
    {{ hidden_field("stage", stage_num) }}
    {{ submit_button("Confirm and proceed") }}
    <a href="javascript:history.back()">Go Back</a>
{% endblock %}
'''


fail_text = '''
<h1>The answer is not correct!</h1>
<p>You can try again!</>
<a href="javascript:window.history.go(-2)">Go Back</a>
'''


@add_route(None, methods=['GET', 'POST'])
@on_success('/wasp10/stage1', 10)
def entry():
    page = {}
    # Retrieve user id
    user = get_user(session['user_id'])
    current_app.logger.debug(f"Retrieving user ID {user}")

    # Retrieve user status
    status_key = "sanity-status"
    progress_status = get_user_flag(user['id'], status_key)
    current_app.logger.debug(f"User flag {progress_status}")

    graph_id = session.get('graph_id')
    graph_id, graph, llength = get_graph() if graph_id is None else get_graph(graph_id)
    session['graph_id'] = graph_id
    graph = json.loads(graph)
    current_app.logger.info(f'{user} has been assigned {graph_id} graph id')
    # Get answer from form
    for answer in request_value('q_final_1'):
        return {
            'content': env.from_string(confirm_text).render(answer=answer,
                                                            page=page,
                                                            user=user,
                                                            stage_num=4)
        }

    # When user confirms the final answer, we check its correctness and score
    for answer in request_value('final_answer'):
        if verify(answer, llength):
            set_user_flag(user['id'], status_key, 'tainted')
            return {
                'answer': 'pass'
            }
        return {
            'content': env.from_string(fail_text).render(),
        }
    return {
        'content': env.from_string(entry_text).render(page=page,
                                                      user=user,
                                                      stage_num=4,
                                                      graph=graph),
    }


def verify(answer, expected_response):
    try:
        return int(answer.strip()) == int(expected_response)
    except Exception:
        return False  # Any invalid input is no good
