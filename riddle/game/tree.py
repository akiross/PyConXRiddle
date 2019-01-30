from jinja2 import Template
from riddle.utils import get_level_structure, query_user_process


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
            {% for level, users in levels %}
            <tr>
                <td>{{ level }}</td>
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
    for user_id, solved_level in query_user_process(None):
        users.add(user_id)
        levels.setdefault(solved_level, set()).add(user_id)

    # Build table of which user solved which level
    solved = []
    users = sorted(users)  # Sort all users
    ls = get_level_structure()
    ls.remove(__name__.split('.')[-1])  # Remove this special module
    for l in ls:
        solved.append((l, [u in levels.get(l, {}) for u in users]))

    return tpl.render(users=users, levels=solved)
