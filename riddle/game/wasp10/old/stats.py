"""This is a poorly coded statistics page that gives user info."""

import zlib
import random
import sqlite3
import datetime

from pathlib import Path
from jinja2 import Template
from flask import session, request, current_app

from riddle.names import random_name, _names, _adjectives
from riddle.utils import create_user, get_user, unset_user_flag
from riddle.urls import without_answer, add_route

from .. import env
from . import get_database


entry_text = '''{% extends "base" %}
{% block body %}
<h1>Statistics</h1>
{% if message is defined %}
<div>{{ message }}</div>
{% endif %}
{% if fetch_counters is defined %}
<div><a href="{{ url_for("wasp9_fetch") }}">Fetch data</a></div>
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
    <!-- via fetch.php -->
    <div>Remember to <i>fetch</i> new data after reset.</div>
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


@without_answer
@add_route("/wasp9/stats.php", endpoint="wasp9_stats")
def entry():
    user = get_user(session['user_id'])
    # print("GOT USER DATA", user)
    db = get_database(user)
    unset_user_flag(session['user_id'], 'sanity-status')
    # Make this mutable
    args = dict(request.args)


    do_select = 'table' in args
    do_update = 'update' in args

    # Ensure we are getting a clear intention
    if do_select and do_update:
        return {
            'content': env.from_string(error_text).render(
                message=f'''<div><h3>Error</h3></div><div>500 (Query Error)</div>
                <h3>table xor update</h3>
                <div>Cannot update and query table at the same time</div>
                '''
            ),
        }
    elif not do_select and not do_update:
        # Hinting that a table parameter is required
        return {
            'content': env.from_string(error_text).render(
                message=f'''<div><h3>Error</h3></div><div>500 (Query Error)</div>
                <h3>No table</h3><div>Please specify a table to see statistics.</div>
                '''
            ),
        }

    try:
        if do_select:
            table = args.pop('table')
            query = f'SELECT * FROM {table}'
            where = ' and '.join(f'{f} = "{v}"' for f, v in args.items())
            if where:
                query += f' WHERE {where}'
            # print("query", query)
            with db:
                ans = db.execute(query)
                descriptions = [d[0].replace('_', ' ').title()
                                for d in ans.description]
                rows = ans.fetchall()
                answers = [{
                    'name': table.capitalize() + " stats",
                    'header': descriptions,
                    'rows': rows,
                }]
                # print("ans", answers)

                if "Value" in descriptions:
                    pos = descriptions.index("Value")
                    answers[-1]['tail'] = [{
                        'labelspan': pos,
                        'label': "Total",
                        'value': sum(r[pos] for r in rows),
                        'afterspan': len(descriptions) - pos - 1,
                    }]

                args = dict(user=user, query=answers)
                # Show how to perform updates by showing a button here
                if table == 'counter':
                    args['reset_counters'] = True

                return {
                    'content': env.from_string(entry_text).render(args),
                }
        else:
            update = args.pop('update')
            query = f'UPDATE {update} SET '
            query += ', '.join([f'{col} = "{val}"' for col, val in args.items()])
            # print("query", query)
            with db:
                db.execute(query)
                args = dict(user=user, message="Updated successfully.")
                if update == 'counter':
                    args['fetch_counters'] = True
                return {
                    'content': env.from_string(entry_text).render(args),
                }
    except (sqlite3.OperationalError, sqlite3.IntegrityError, sqlite3.Warning) as exc:
        # Hinting that SQLite is being used
        return {
            'content': env.from_string(error_text).render(
                message=f'''<div><h3>Error</h3></div><div>500 (SQLite Error)</div>
                <h3>Message</h3><div>{str(exc).capitalize()}</div>
                '''
            ),
        }
