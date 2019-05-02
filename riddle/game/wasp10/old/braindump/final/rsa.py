import random

from pathlib import Path
from flask import session, request, current_app

from riddle.urls import add_route
from riddle.utils import get_user
from riddle.tools import generate_big_prime, SimpleRSA
from riddle.game.wasp10 import env


game_text = '''\
{% extends "base" %}
{% block body %}
    <h1>Good news!</h1>
    <p>We made it! The files you uploaded allowed us to map the language used
    internally by the AI, we are now able to understand its thoughts! This
    gives us the ability to tear it down, but before that we need to break in
    the system.</p>
    <p>Here, this is the knowledge we extracted from the brain!</p>
    <ul>
    {% for url, name in brain_files %}
        <li><a href="/{{url}}">{{name}}</a></li>
    {% endfor %}
    </ul>
    <p>To break in, we can try to get a remote shell on the machine, but to get
    in we need a key. Apparently, the AI is using some sort of public key
    encryption method to authorize incoming connections to it. I found this
    public key: we need to break it! Help me finding the two factors that
    were used to create the key, and send them to me by using the following
    form.</p>
    <pre>
-----BEGIN RSA PUBLIC KEY-----
{{ composite }}
-----END RSA PUBLIC KEY-----
    </pre>
    {% if show_message %}
    <div><b>Those are not the right factors, try again!</b></div>
    {% endif %}
    <form method="POST">
        <div><label>Factor</label><input type="text" name="prime1" /></div>
        <div><label>Factor</label><input type="text" name="prime2" /></div>
        <div>
            <button type="submit">Submit</button>
        </div>
    </form>
{% endblock %}
'''


success_text = '''\
{% extends "base" %}
{% block body %}
    <h1>Success!</h1>
    <p>You did it! The factors you provided were correct!</p>
    <p>The Evolutionary Artificial Intelligence has been deactivated.</p>
{% endblock %}
'''


@add_route("/wasp9/breakin", endpoint="wasp9_breakin", methods=['GET', 'POST'])
def entry():
    user = get_user(session.get('user_id'))

    # Get the translated files
    root = Path(current_app.static_folder) 
    content = root / 'humans' / 'plans'
    brain = [(str(p.relative_to(root.parent)), p.name)
             for p in content.glob('**/*')]

    # Generate two unique primes for this user
    rng = random.Random()
    rng.seed(user['id'])
    p1 = generate_big_prime(62, rng)
    p2 = generate_big_prime(62, rng)
    p1, p2 = sorted([p1, p2])

    show_message = False
    if request.method == 'POST':
        try:
            up1 = int(request.form.get('prime1', 0))
            up2 = int(request.form.get('prime2', 0))
            up1, up2 = sorted([up1, up2])
            if up1 == p1 and up2 == p2:
                return {
                    'content': env.from_string(success_text).render(user=user),
                                                                    
                }
            else:
                show_message = True
        except ValueError:
            show_message = True

    rsa = SimpleRSA(p1, p2, rng=rng)

    return {
        'content': env.from_string(game_text).render(
            user=user,
            composite=rsa.serialize_key(rsa.public_key).decode(),
            show_message=show_message,
            brain_files=brain,
        ),
    }
