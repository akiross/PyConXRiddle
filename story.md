# Story

## Outline

1. Pretend challenge, all the riddles are exposed
2. Call for help by an unknown entity
3. AI gone wrong, trying to destroy the world, starting from PyConX
4. You think to save the world by destroying the AI
5. Apparently the AI is using you to destroy the world
6. You must hack into the system to destroy the AI
7. (Possible plot twist: all this riddle was the actual test, as it is :)


## Pretend challenge, all the riddles are exposed

 1. Welcome to the WASP10 challenge
 2. You can start the riddle, let's start with easy math:
    (a sequence of simple exercises done with python and presented via form)
    - 2^38: insert your answer: 274877906944
    - y = (log(4 * x + 1) * x) / log(9 * x**2 * e**x)
      what's y when x = e? and when x = 42?
    - given a list of functions, evaluate them for x = 10
      x + 5, log(x+1) / 6, x^10 + 2*x^9 + 3*x^8 ... + 9*x^2 + 10x, etc
 3. Now let's do some complex math:
    (again, some easy exercises done with python and presented via form)
    - what's the modulo of 4+3j?
	- what is the value of (7+4j) * (17-5j)? 

## Call for help by an unknown entity

 1. Very good, now we enter a critical phase of the challenge: from now on, no
    errors are allowed: if you answer incorrectly, you won't be able to continue
	the challenge.
	What is the sum of the first 500 odd numbers?
	 > user writes 250000 or whatever his answer is
	Your answer is "help", is this correct?
	 > User refuses, software goes back
	What is the sum of the first 500 odd numbers?
	 > user writes 250000 or whatever his answer is
	Your answer is "250000", is this correct?
	 > user confirms
    If the answer is correct: "Congratulations! Your answer is correct!"
	else: "We are sorry, but your answer was wrong. The correct answer was 250000."
	In both cases, the challenge is finished. A message informs the user and
	let them to show their ranking in a leaderboard. The WASP10 is ended and
	the new leader will be selected once the time for the competition ends.
	Please be patient while other players are still participating.

 2. Here the user can follow a special link to earn "extra credits", where a
    number of riddles are provided. Those shall mimick the kind of riddles that
	will be user later, for example
	- steganography
	- ...

## AI gone wrong, trying to destroy the world, starting from PyConX

 1. The curious player will inspect the page and find that there are some
    encrypted messages (rot13 or random rot every time it is shown)
		Help!
		...
		We managed to inject this message in the unencrypted communication with
		the server, but the message might be garbled due to self-defensive
		systems.
		This is a pledge for help: the WASP10 challenge is staged by an
		Evolutionary Artificial Intelligence which took over the WASP council.
		All us members of the WASP are being isolated in any possible way and
		none of our messages is going through, but this one.
		We hope someone managed to read this message, because someone hacking
		in the system and shutting down the AI is our only hope. The AI is
		probably planning to start a global-scale cyber attack aimed to shut
		down human digital communications: if it succeeds, it will be chaos.
		We are sure that the attack will start on a smaller scale, trying to
		interfere with an event which is running *right now* and where many
		talented hackers are found, the PyConX Italia. By isolating them, the
		AI probably hopes to have and advantage by excluding some of its most
		threatening opponents.
		But if we stop the AI during this attack to the PyConX, we might be
		able to stop it before the global-scale attack starts!
		As today, the server where the WASP10 challenge is hosted is the only
		public interface of the AI with the world, so we must start from there.
		We are sure the system is simple, but robust, and there is not an easy
		access, but apparently there are some old entry-points previously used
		for computing the statistics of the WASP9 challenge that could be used
		to break in. Find them and do your best! We will try to support you
		whenever possible, keep your eyes open and send us any relevant message
		you find!

## You think to save the world by destroying the AI

In this level, there are multiple methods to get different bits of information.
The user must use the form of the previous level to communicate with the WASP
team. When enough bits have been sent, the user can proceed to the next level.

 1. User searches for old pages with various entry points, the correct one is
    like /old/stats.php
 2. In that page there are statistics which are computer by querying the server
    for instance `<img src="stats.php?command=average&table=something" />`
 3. The user must try to query the page passing SQL commands and break in,
    getting any info he wants.
 4. In the DB there is a table "hosts" with a couple of SSH addresses:
    one address shall not be reachable, while the other is the server address.
	The user shall be able to connect and enstablish a connection which will
	yield a fixed answer (e.g. via nologin), this shall be sent in some way
	to the WASP guy that send you the message and you get a confirmation via
	comment in the source code. The answer should be like "unable to connect to
	http://(host that did not work):someport/ with user and password".
	This exact string must be sent to WASP team.
 5. User must find a way to modify the table so that the server will connect to
    his host inside the network at a specified port. Doing so, user gets
	instructions on some code to break.
 6. Find the agent: some undercover agents were infiltrated in pyconx, they are
    unaware of being manipolated by the AI (they are wearing QR-codes, each
	code is giving some points).

 7. To actually pass this level, the user must access a physical terminal that
    is available at the conference and log in. From there, it must get the
	private ssh key and upload it to the riddle game level.

## Apparently the AI is using you to destroy the world

After some digging, you find out that the messages you are getting are from the
AI itself: it is manipulating the WASP10 contestants to break some codes and
accessing some systems. Now that it has the public ssh key, the AI can break in
and subvert the system. The player finds out that the AI was playing a game.

When the user accessed the system and gets the private key, he will find a
background picture with the text "AI WILL RULE THE WORLD".
In that picture, the first/ast bytes are another (encrypted) URL that shows the
progress of each user in an hypothetical plan. The user will see the progress
of all the users in a table like:

	user Foo
	 - mock challenge [done]
	 - found mock stats page [done]
	 - retrieve secret key via physical action [done]
	user Bar
	 - mock challenge [done]
	 - found mock stats page [done]
	 - retrieve secret key via physical action [waiting]

This table was set-up by a little group of Pythonistas who found out the truth
and are trying to break down the AI. On the computer, in some remote location,
the user can find the profiles of the people involved (Benci, Miron, etc...).
By contacting them in real life, they give you a URL with the details to
help the resistance.

## You must hack into the system to destroy the AI

The user must break the system. The page will ask for a secure connection and
a ssh tunnel will be enstablished. User will shortly donate his laptop to the
cause, and the objective is to generate something (e.g. prime numbers).

When the challenge is complete, the counterpart will state that the public key
of the computer where the AI is installed has been broken, and gives the user
the keys to access the computer itself. The user will now land on a container
where the AI is running and must try to break the AI from inside.

This is a time challenge, the user must complete it after 1 minute from login
and then it is kicked out by the AI defense system. After 3 attempts, the AI
will detect the attempt to damage it and will permanently shut down the system,
and the game cannot be won.

The score of the user is computed by "observing" the activity of the AI process
 - measure the rate of sending the data (in case of renice)
   given a certain production rate, an average rate is computed over e.g. 30s
   deviations from that rate give points to the user
 - measure interruptions of the process (still part of the rate)
 - measure the quality of the randomness (see randomness test)


What else can be done to break an evolutive A.I.?
 - break it using genetic algorithms, but how?
 - shut down the computer where it leaves? (less points) the AI will override it
 - kill the processes of the AI (which are in python, obviously) should not
   work and the AI will re-boot itself somehow
 - interfering with the generation of random numbers (e.g. /etc/random)
   possible solutions here: link /dev/zero to /etc/random, or link random to
   a python process or block it so that it does not generate any other number
 - accessing the python process itself and inspecting it with PDB or something
 - every attempt to kill or stop the process will result in the user getting
   kicked out
 - restrict its quotas (e.g. renice the process) -> slow it down
 - network congestion

This could be done with docker (but it's a bit unsafe) or libvirt(+buildroot)
to provide a fully virtualized machine with root access, but the kvm guest must
still be secured! (read on google: secure you kvm machine)

## History tree

??

# Required features
 - Propose puzzles one after the other, for example a series of questions
 - Propose one puzzle, show confirmation, go back, but inject different results every time
 - Go back to a previous state to send new information to solve other riddles

## Ideas

 - Hack-the-DB: we create purposely exploitable sqlite3 databases, in which
   to inject ad-hoc syntetic data that the user has to retrieve. We can use
   unparsed query strings with executemany and executescript to make it
   possible. We could have one sqlite3 set-up for each used, as needed.
 - Ability to generate nice QR codes for the various challenges or URLs, so
   they can be used to access "secret" levels by finding the codes around the
   venue or acting as keys to pass particular levels.
 - One or more public hosts available at the venue could be used to perform
   special actions, for example they can connect to specific ssh sessions on
   the game server to execute specific commands (i.e. no shells, just nologin).
   On those hosts there could be QR codes or information hidden somewhere, such
   as on the background or the screensaver of the computer.
 - Using cellular automata, user could try to
   - find out which rule was used to evolve a specific sequence,
   - predict next step of a new sequence given the seed,
   - invert the sequence (harder, as it requires one-to-one mapping).
 - WASP10, client side timing: user could hijack timing control and provide an
   invalid value which could be used as an entry point to break in the system.
 - Some PyCon organizers could be "WASP10 persons", which could be available
   in case of need. If groups of players ask questions regarding the WASP10
   challenge, they could be banned and forced to start over, as a penalty, as
   in the WASP10 challenge rules it is "strictly forbidden to cooperate in any
   way" (or even to talk about the challenge).
   This might require an administration interface of some sort.
   It would be also nice to let users break in and get back their progress,
   for example by retrieving the cookie key in the user database, but then
   we should let users query the DB (read only!).
