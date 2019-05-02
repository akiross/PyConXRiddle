from pathlib import Path
from jinja2 import Template
from flask import current_app
from riddle.urls import add_route

from . import list_page


name = '29938924'


@add_route(f"/proxy/ftp/grid/experiments/evoai/{name}", endpoint="braindump_brain")
def entry():
    root = Path(current_app.static_folder) 
    content = root / name
    resources = [(str(p.relative_to(root.parent)), p.name) for p in content.glob('**/*')]
    return {
        'content': Template(list_page).render(directory=content.name,
                                              resources=resources),
        'answer': 'pass',  # Solved as soon as it is opened
    }
