from hashlib import md5

from flask import session, request, abort

from riddle.urls import add_route, without_answer
from riddle.utils import get_user_flag, set_user_flag
from riddle.game.wasp10 import env


#  TODO storia
entry_text = '''\
{% extends "base" %}
{% block body %}
    <h1>Aiutaci!</h1>
    <p>storia, storia, storia..</p>
    {% if clues_count == 0 %}
        <p> Abbiamo bisogno di file prodotti dall'AI per poter decifrare il linguaggio che usa,
        una volta che avrai caricato i file necessari ti potremo dare più informazioni, guardati in giro! </p>
    {% else %}
        <p> Hai caricato {{ clues_count}} file utili a noi ma ne servono di più per poterti aiutare </p>
    {% endif %}
    {% if incorrect_file_uploaded %}
        <p> Mi dispiace ma questo file non ci serve a nulla, riprova!</p>
    {% elif correct_file_uploaded %}
        <p> Bravo! hai trovato un file utile iniziamo subito a lavorarci, ma ce ne servono altri continua a cercare </p>
    {% endif %}
    <form method=post enctype=multipart/form-data>
        <input type="file" name="file"/>
        <div>
            <button type="submit"> Invia</button>
        </div>
    </form>
{% endblock %}
'''

#  TODO storia e link sfida finale
success_text = '''\
{% extends "base" %}
{% block body %}
    <h1>Successo!</h1>
    <p>storia, storia, storia..</p>
    <a href="{{final_battle_link}}"> vai e sconfiggi il AI </a>
{% endblock %}
'''


first_file = b'''\
this is the first file
'''

second_file = b'''\
this is the second file
'''

clue_hashes = {
    md5(first_file).hexdigest(): 'first_file',
    md5(second_file).hexdigest(): 'second_file'
}

clues_count_needed = 2


@without_answer
@add_route("/wasp9/clues.php", endpoint="wasp9_clues", methods=['GET', 'POST'])
def entry():
    user_id = session.get('user_id')
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
                    user=user_id,
                    clues_count=clues_count,
                    incorrect_file_uploaded=True),
            }
        elif correct_clue and correct_clue not in already_upload_clues:
            clues_count += 1
            session['clues_count'] = clues_count
            session['already_upload_clues'] = f'{already_upload_clues},{correct_clue}'
            if clues_count >= clues_count_needed:
                return {
                    'content': env.from_string(success_text).render(user=user_id,
                                                                    final_battle_link='/link/per/sfida/finale'),
                }
            return {
                'content': env.from_string(entry_text).render(
                    user=user_id,
                    clues_count=clues_count,
                    correct_file_uploaded=True),
            }
    if clues_count >= clues_count_needed:
        return {
            'content': env.from_string(success_text).render(user=user_id, final_battle_link='/link/per/sfida/finale'),
        }
    return {
        'content': env.from_string(entry_text).render(user=user_id, clues_count=clues_count),
    }


if __name__ == '__main__':
    files = {
        'first.txt': first_file,
        'second.txt': second_file}
    for n, fo in files.items():
        with open(n, 'w') as f:
            f.write(fo.decode('utf-8'))
