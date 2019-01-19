from riddle import database


def create_user():
    db = database.get_connection()
    cur = db.execute('INSERT INTO user DEFAULT VALUES')
    db.commit()
    return cur.lastrowid


def update_user_progress(user_id, level):
    db = database.get_connection()
    db.execute(
        'INSERT INTO progress (user_id, level) values(?,?)',
        [user_id, level])
    db.commit()
