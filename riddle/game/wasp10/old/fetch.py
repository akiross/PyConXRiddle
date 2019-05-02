"""This is a poorly coded statistics page that gives user info."""

import socket

from http import client
from pathlib import Path
from jinja2 import Template
from base64 import b64encode
from urllib.error import URLError
from urllib.request import urlopen
from flask import session, request, current_app

from riddle.names import random_name, _names, _adjectives
from riddle.utils import create_user, get_user
from riddle.urls import without_answer, add_route

from .. import env
from . import get_database, success_message


entry_text = '''{% extends "base" %}
{% block body %}
<h1>Statistics</h1>
{% if message is defined %}
<div>{{ message }}</div>
{% endif %}
{% for table in query %}
<h1>{{ table.name }} </h1>
<table>
    <tr>
    {%- for h in table.header -%}
        <th>{{ h }}</th>
    {%- endfor -%}
    </tr>
    {% for row in table.rows -%}
    <tr>
        {%- for f in row -%}
            <td>{{ f }}</td>
        {%- endfor %}
    </tr>
    {% endfor %}
    {% for row in table.tail %}
    <tr>
        <td colspan="{{ row.labelspan }}">{{ row.label }}</td>
        <td>{{ row.value }}</td>
        <td colspan="{{row.afterspan}}"></td>
    </tr>
    {% endfor %}
</table>
{% endfor %}
{% if reset_counters is defined %}
<div>
    <h3>Reset counters</h3>
    <form method="get" action="{{ url_for("wasp9_stats") }}">
        <input type="hidden" name="update" value="counter" />
        <input type="hidden" name="count" value="0" />
        <button type="submit">Reset counters</button>
    </form>
</div>
{% endif %}
{% endblock %}
'''

error_text = '''{% extends "base" %}
{% block body %}
<h1>WASP9 - Unexpected error!</h1>
<div>
    Do not worry, you probably did nothing wrong.
    Our technical staff has been notified.
</div>
<div>
    Technical details for geeks
    <div>{{message}}</div>
</div>
{% endblock %}
'''


@add_route("/wasp9/fetch.php", endpoint="wasp9_fetch")
def entry():
    user = get_user(session['user_id'])
    print("GOT USER DATA", user)
    db = get_database(user)

    with db:
        res = db.execute('SELECT * FROM hosts WHERE id = 2')
        target = res.fetchone()[1]
        print("Target database:", target)

    try:
        # Ensure host is a valid IP address
        if ':' in target:
            host, port = target.split(':')
        else:
            host = target
        socket.inet_aton(host)
        try:
            req = urlopen(f'http://{target}',
                          b64encode(success_message.encode()),
                          timeout=2).read(1)
            return {
                'content': f'Content was retrieved successfully.',
                'success': True,
            }
        except URLError:
            return {
                'content': f'Unable to connect to {target}',
            }
        except (client.RemoteDisconnected, client.BadStatusLine):
            return {
                'content': f'Server closed connection unpexpectedly.',
                'success': True,
            }
    except (socket.error, ValueError):
        return {
            'content': f'Invalid IP address for host 2, refusing to connect.',
        }
