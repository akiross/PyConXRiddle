from hashlib import md5

from flask import session, request, abort

from riddle.urls import add_route, without_answer
from riddle.utils import get_user_flag, set_user_flag, get_user
from riddle.tools import generate_big_prime
from riddle.game.wasp10 import env


game_text = '''\
{% extends "base" %}
{% block body %}
    <h1>Success!</h1>
    <p>We made it! The files you uploaded allowed us to map the language used
    internally by the AI, we are now able to understand its thoughts! This
    gives us the ability to tear it down, but before that we need to break in
    the system.</p>
    <p>To do so, we can try to get a remote shell on the machine, but to get in
    we need a key. Apparently, the AI is using some sort of public key
    encryption method to authorize incoming connections to it. I found this
    public key: we need to break it! Help me finding the two factors that were
    used to create the key, and send them to me by using the following form.</p>
    <h4>{{ composite }}</h4>
    <form method="POST">
        <label>Factor</label><input type="text" name="prime1" />
        <label>Factor</label><input type="text" name="prime2" />
        <div>
            <button type="submit">Submit</button>
        </div>
    </form>
{% endblock %}
'''


@add_route("/wasp9/breakin", endpoint="wasp9_breakin")
def entry():
    user = get_user(session.get('user_id'))

    # Generate two unique primes for this user
    rng = random.Random()
    rng.seed(user['id'])
    p1 = generate_big_prime(8, rng)
    p2 = generate_big_prime(8, rng)

    return 
    

    clues_count = session.get('clues_count', 0)
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
        elif correct_clue and correct_clue not in already_upload_clues:
            clues_count += 1
            session['clues_count'] = clues_count
            session['already_upload_clues'] = f'{",".join(already_upload_clues)},{correct_clue}'
            if clues_count >= clues_count_needed:
                return {
                    'content': env.from_string(success_text).render(
                        user=user, final_battle_link=final_battle_link),
                }
            return {
                'content': env.from_string(entry_text).render(
                    user=user,
                    clues_count=clues_count,
                    correct_file_uploaded=True),
            }
    if clues_count >= clues_count_needed:
        return {
            'content': env.from_string(success_text).render(
                user=user, final_battle_link=final_battle_link),
        }
    return {
        'content': env.from_string(entry_text).render(user=user, clues_count=clues_count),
    }
