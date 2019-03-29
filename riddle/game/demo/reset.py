from flask import session
from riddle.utils import create_user, get_user


def entry():
    # Create a new user overwriting the previous ID
    uid = create_user()
    user = get_user(uid)
    print("RESET USER TO", user)
    session['user_id'] = uid
    return {
        'content': f"<p>Aight! Yer criminal record be now swab!</p>\
                     <p>Ye be now {user['name']}, ahoy!</p>",
    }
