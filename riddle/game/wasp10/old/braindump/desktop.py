from pathlib import Path
from jinja2 import Template
from flask import current_app
from riddle.urls import add_route

from . import list_page


BASE_URL = "/backups/wasp-members/creator-pc"


@add_route(BASE_URL + "/", endpoint="braindump_desktop", defaults={'path': None})
@add_route(BASE_URL + "/<path:path>", endpoint="braindump_desktop_sub")
def entry(path):
    root = Path(current_app.static_folder) 
    content = root / 'creator-home'

    if path is not None:
        path.replace('..', '')
        content /= path
    else:
        path = ""

    directories, resources = [], []
    for res in content.glob('*'):
        if res.is_dir():
            if path:
                directories.append((f"{BASE_URL}/{path}/{res.name}", res.name))
            else:
                directories.append((f"{BASE_URL}/{res.name}", res.name))
        else:
            resources.append((str(res.relative_to(root.parent)), res.name))

    return {
        'content': Template(list_page).render(directory=content.name,
                                              directories=directories,
                                              resources=resources),
        'answer': 'pass',  # Solved as soon as it is opened
    }
