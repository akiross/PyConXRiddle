from pathlib import Path
from jinja2 import Template
from flask import current_app

list_page = """
<!doctype html>
<html>
<body>
    <ul>
    {% for url, name in resources %}
        <li><a href="/{{url}}">{{name}}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
"""


# TODO better URL
def entry():
    root = Path(current_app.static_folder) 
    content = root / '29938924'
    resources = [(str(p.relative_to(root.parent)), p.name) for p in content.glob('**/*')]
    return {
        'content': Template(list_page).render(resources=resources),
        'answer': 'pass',  # Solved as soon as it is opened
    }
