"""This is a test level, still to be filled."""

import random

from jinja2 import Environment, Template
from flask import session, request

from riddle.utils import create_user, get_user

from . import env, deadline

from types import SimpleNamespace


entry_text = '''{% extends "base" %}
{% block title %}10th WASP10 Competition{% endblock %}
{% block body %}
<div>
    <h1>Welcome to the 10<sup>th</sup> WASP<sup>10</sup> Competition</h1>
    <h2>Welcome, participant {{ user.name }}</h2>
    <p>Before starting, let us thank you for joining this challenge.<br/>
    As you already know, the WASP<sup>10</sup> (Worldwide Association of 10-Sigma Programmers)
    is seeking for a new leader. As it is custom in our association, the leader,
    formally in charge as <b>President of the WASP<sup>10</sup></b>, is selected among a pool of
    excellence programmers through a worldwide competition.</p>
    </p>
</div>
<div>
    <h3>Background information on WASP<sup>10</sup></h3>
    <p>For many years, this competition happened behind closed doors and was
    accessible to distinguished programmers exclusively by invitation by other
    members of the association. Elitarism and secrecy were a fundamental part of
    the WASP<sup>10</sup> spirit, altough it is well known that the existence of the
    association is now a public fact and some members take advantage of its
    prestige in various ways.</p>
    <p>WASP<sup>10</sup> was founded in 1969, when the programming community was much smaller
    across the globe, the World-Wide Web was not born yet and computers were not
    a commodity as they are today. The first president, a kind and modest person,
    was elected by voting, and not with a challenge. It was, in fact, himself that
    after being elected, proposed that the next president could be selected via a
    challenge, held every 5 years and accessible to all the WASP<sup>10</sup> members and
    invited programmers.</p>
    <p>Due to the diffusion of computers and their programmers, in 2009, right after 
    her election, the 9-th president of the association, in a glorious act of
    courage, decreted that starting from the next challenge, in 2014, the challenge
    would be open to public, to increase the chances to find greater talents
    outside the association boundaries.</p>
    <p>This decision had consequences. Many members of the community opposed, and
    the backlash was violent, especially among the oldest members of the association.
    For this reason, WASP<sup>10</sup> members came to a compromise: the challenge would be
    open to public, but starting at a later date and with a smaller audience.</p>
</div>
<div>
    <h3>WASP<sup>10</sup> at PyConX Italy</h3>
    <p>For the reasons described above, WASP<sup>10</sup> is finally revealed to the public
    in the context of PyConX Italy. The reasons for this choice is twofolds:
    <ul>
    <li>PyCon Italia is now an international conference hosting about 1000 attendees
    coming from every corner of the world. Among them, there are many talented
    programmers, including many notable members of the WASP<sup>10</sup>.</li>
    <li>The conference is held in a time and a location that are significant for
    many of the WASP<sup>10</sup> members. In particular, Florence has given birth to the
    first WASP<sup>10</sup> President and it is where he, with some of the funding members,
    met to discuss about the association before it was born.</li>
    </ul>
    </p>
    <p>For this reason, we are happy to announce that the WASP<sup>10</sup> Competition is
    open to the general public and, in this particular instance, to the participants
    of the 10<sup>th</sup> PyCon Italia conference.</p>
    <p>According with the rules enstablished by the association members in 2009, it
    will be responsibility of the new President to definitely open the competition
    to the world wide community of programmers or go back to an invitation basis.</p>
</div>
<div>
    <h3>Rules of the competition</h3>
    <p>Balance, fairness and opportunity are pillars of every WASP<sup>10</sup> Competition.</p>
    <p>This mean that the challenge tries to comprise many tasks which spread across
    all the programming speciailization, trying to avoid biases at all cost.</p>
    <p>Fairness among participants is expected. No one must try to interfere with
    the work of other participants, not even by helping. One must not accept the
    help of other participants in any case. The challenges in this competition are
    designed for individuals, and any discovered attempt of cooperation is frown
    upon and will be banned.</p>
    <p>The participants must absolutely refrain to interfere with the competition
    delivery mechanisms. In other words, one must not attempt to hack or break
    the system for any reason. Any participant caught in doing so will be banned
    and, of course, in case of victory, the result will be invalidated.</p>
    <p>The time used to complete the challenge will be recorded. The results of the
    competition will include time to complete and, given the same score, the 
    participant who used less time to complete will be the winner.</p>
    <p>Each challenge is scored for the quality of the output. The score points of
    each challenge is not disclosed, but it is given that wrong or empty answers
    are scored 0 points. There is no penalty in making mistakes.</p>
    <p>This competition has been revised in view of the opening to the public.
    Naturally, we are not considering to lower the standards of this competition,
    but we will provide a "gentle introduction", comprising of few preliminary
    questions, for participants who are not familiar with this type of competition.
    Here follows a list of things to keep in mind.
    </p>
    <ul>
        <li>Stages will be subsequent, from this one to the last, with a growing level
        of difficulty.</li>
        <li>A question will be clearly stated to define objectives of the stage.</li>
        <li>A form will be provided to input your answer(s).</li>
        <li>If necessary, you can use the tools of your choice to
        compute your answer(s).</li>
        <li>Some levels may require you to input some source code. In this case, it is
        mandatory to answer using the Python programming language.</li>
    </ul>
</div>
<div>
    <h3>You can begin!</h3>
    <p>By clicking the following link, your timer will start and you will have
    until {{ page.deadline }} to complete the competition. When time is over, every
    challenge not completed will be automatically scored 0 points.</p>
</div>
<div><a href="{{ page.next_page }}">Start the Competition!</a></div>
{% endblock %}
'''


def entry():
    user = get_user(session['user_id'])
    page = {
        'next_page': '/wasp10/stage1',
        'deadline': deadline,
    }
    return {
        'content': env.from_string(entry_text).render(page=page, user=user),
    }
