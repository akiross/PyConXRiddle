from hashlib import md5
from pathlib import Path

from flask import session, request, abort, current_app

from riddle.urls import add_route, on_success
from riddle.utils import get_user_flag, set_user_flag, get_user
from riddle.game.wasp10 import env


entry_text = '''\
{% extends "base" %}
{% block body %}
    <p>{{user.name}}, thanks to your help we broke in the server! This page was
    set up to communicate more easily with you. Hopefully, the AI will not tear
    it down before we collected all the required information.</p>
    {% if clues_count == 0 %}
    <p>Use the form below to upload any file that looks interesting and might
    give us a clue: we must understand the AI plans and how to destroy it!</p>
    <p>Anything that is directly related to the AI is a good candidate and
    might give us a chance to understand what is in its "mind"!</p>
    {% else %}
    <p>You upload {{ clues_count }} useful files, but we need more to get to the end of this!</p>
    {% endif %}
    {% if incorrect_file_uploaded %}
    <p>Apparently, this file is not useful for our purpose, but don't stop and try again!</p>
    {% elif correct_file_uploaded %}
    <p>Great! This file is looks promising! We are working on it, but we need more!</p>
    {% endif %}
    <form method=post enctype=multipart/form-data>
        <input type="file" name="file"/>
        <div>
            <button type="submit">Upload</button>
        </div>
    </form>
{% endblock %}
'''

# FIXME better file loading
FILES_LOC = Path(__file__).absolute().parents[4] / 'static' / '29938924'

files = {f.stem: f.open().read().encode() for f in FILES_LOC.glob('*')}
clue_hashes = {md5(f).hexdigest(): n for n, f in files.items()}
clues_count_needed = len(files)


@on_success(redirect='/wasp9/breakin')
@add_route("/wasp9/clues.php", endpoint="wasp9_clues", methods=['GET', 'POST'])
def entry():
    user = get_user(session.get('user_id'))

    clues_count = session.get('clues_count', 0)
    current_app.logger.info(f"Clues count for user {user} is currently {clues_count}/{clues_count_needed}")
    if request.method == 'POST':
        possible_clue = request.files.get('file')
        if possible_clue is None:
            abort(400)
        already_upload_clues = session.get('already_upload_clues', '').split(',')
        clue_hash = md5(possible_clue.stream.read()).hexdigest()
        correct_clue = clue_hashes.get(clue_hash)
        if correct_clue is None:
            return {
                'content': env.from_string(entry_text).render(
                    user=user,
                    clues_count=clues_count,
                    incorrect_file_uploaded=True),
            }
        else:
            if correct_clue not in already_upload_clues:
                clues_count += 1
                session['clues_count'] = clues_count
                session['already_upload_clues'] = f'{",".join(already_upload_clues)},{correct_clue}'
                if clues_count >= clues_count_needed:
                    return {
                        'answer': 'pass',
                        #'content': env.from_string(success_text).render(
                        #    user=user, final_battle_link=final_battle_link),
                    }
            return {
                'content': env.from_string(entry_text).render(
                    user=user,
                    clues_count=clues_count,
                    correct_file_uploaded=True),
            }
    if clues_count >= clues_count_needed:
        return {
            'answer': 'pass',
            #'content': env.from_string(success_text).render(
            #    user=user, final_battle_link=final_battle_link),
        }
    return {
        'content': env.from_string(entry_text).render(user=user, clues_count=clues_count),
    }


if __name__ == '__main__':
    for n, fo in files.items():
        with open(n, 'w') as f:
            f.write(fo.decode('utf-8'))
