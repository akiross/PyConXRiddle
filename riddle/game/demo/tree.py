from pathlib import Path
from riddle import utils 
from flask import url_for, current_app
from jinja2 import Template


template = r"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Tree</title>
    <meta name="description" content="The Game Tree">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Levels completed by users</h1>
    <table>
        <thead>
            <tr>
                <th>Level\User</th>
                {% for user in users %}
                <th>{{ user }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for level, rules, users in levels %}
            <tr>
                <td>{{ level }} ({{ ', '.join(rules) }})</td>
                {% for user in users %}
                <td>{{ 'x' if user else '' }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


def entry():
    return user_progress(), False


def user_progress():
    """Return a table of levels solved by each user."""
    # Query all progress from all users
    tpl = Template(template)

    # Prepare data to be visualized
    levels = dict()  # Dict level -> {user solved}
    users = set()  # Set of users
    for user_id, solved_level in utils.query_user_progress(None):
        users.add(user_id)
        levels.setdefault(solved_level, set()).add(user_id)

    # Build table of which user solved which level
    solved = []
    users = sorted(users)  # Sort all users
    level_map = current_app.config['level_map']  # Map level-rules
    ls = utils.get_level_structure()
    ls.remove(utils.get_level_pathname(__file__)[0])  # Remove this special module
    ls = {str(l) for l in ls}
    for l in ls:
        solved.append((l, level_map[l], [u in levels.get(l, {}) for u in users]))

    return tpl.render(users=users, levels=solved)
