from riddle.utils import get_level_structure

def entry():
    return user_progress(), False
    return "<br/>\n".join(f"<a href='{l}'>{l}</a>" for l in get_level_structure()), False


def user_progress():
    """Return a table of levels solved by each user."""

    # Get users
    users = ['a', 'b', 'c']
    # Build table
    table = []
    for l in get_level_structure():
        row = [f"<span>{l}</span>"]
        for u in users:
            row.append(f"<span>User result</span>")
        table.append("".join(row))
    return "<br/>\n".join(table)
