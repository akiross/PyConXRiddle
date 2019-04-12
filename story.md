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
    like /wasp9/stats.php
 2. In that page there are statistics which are computer by querying the server
    for instance `<img src="stats.php?command=average&table=something" />`
 3. The user must try to query the page passing SQL commands and break in,
    getting any info he wants.
	- Select and Update queries are exposed via SQL injection, so user can
	  query all the tables and update values. sqlite_sequence is exposed so one
	  can get all the tables querying that table.
 4. In the DB there is a table "hosts" with some addresses:
    some addresses are bogus, while others will have an effect. A protocol is
	associated to every IP, so user can take action. One protocol is http, but
	the user has no clue he has to hijack that. In the table list, the counter
	table exposes a reset button which shows how to update the table via a
	reset button.
 5. After resetting, user can access the retrieve page to call the http host.
 6. The user must update the table so that retrieve page will
	connect to his host (must be the same subnet!) and post some data.
	The data is a message from a WASP10 member that gives further instructions.
 7. Find the agent: some undercover agents were infiltrated in pyconx, they are
    unaware of being manipolated by the AI (they are wearing QR-codes, each
	code is giving some points).
 8. Player must convince the unaware agent that there is an AI and that they
    got a message from monty python. They will show you their orders, received
	as an e-mail with a given number NNN-NNN-NNN. Then give you access to a
	terminal. Player shall go there to retrieve its IP, than he can connect to
	it and explore the contents via ssh.
 9. To make things harder, the server might disallow ssh password login :)
	So player must install his ssh public key. Root access is not granted.

## Apparently the AI is using you to destroy the world

FIXME player shall stay on the physical terminal the least time possible.
      that terminal must contain messages and notes, nothing else.
	  The AI "mind files" must be on another computer, the one with the boss.

The physical terminal contains an image which helds some secret information
(steganography): a public RSA key, just a few bits large.
The image is appropriately displaying the text "AI WILL RULE THE WORLD", which
was humorously set by the owner of the computer, which is an AI fanboy. On the
computer, there are some notes written by the owner that show how he thought
that the only hope for humanity to avoid self-destruction is to build an AI
that helps the humans to gain freedom from the fear of death.
This individual, who was a contributor to the PyCon conference, has disappear
in a tragic accident few months back, so that computer is left there in his
memory.

Just to make sure the user can solve the level, in the Document directory of
the terminal there is a "Brief guide on RSA encryption", which explains how
public/private keys can be used to encrypt a message.
The user must decipher the image and get the public key. The key must also be
uploaded somewhere. This is where the AI gets the aid it was seeking from
the user.

Then, the user must go back to the info obtained in the host table:
the telnet/ssh connection will yield an encrypted message, encrypted with the
associated private key.

Decoding the message will yield a path on the system: a folder full of files.
Those are the plans of the AI. Since an AI is obviously thinking using a
non-English language, those files are definitely not in English. Yet, since the
AI manipulated the agents to make them do what it wants, the AI is using some
sort of translation table to translate its language to English.
User has to locate the file NNN-NNN-NNN, which is a numpy array with the same
length of the message sent to the agents. That file will provide a dictionary
to decode the AI plans.

User must then read the files and discover the true story: the messages player
has been getting are from the AI itself: it is manipulating the WASP10
contestants to break some codes and accessing some systems. Now that it has the
public ssh key, the AI can break in and subvert the system. The player finds
out that the AI was playing a game.

--
What do agents know? They are unaware of the fact that AI has cut off WASP10
organization. They received an email asking to search for talents.
Talents are redirected to WASP10 challenge and with it they will try to break
the code.
The code must be easily accessible, so that the AI can harness computing power
to break it, but user should not be able to break that code.

REM When the user accessed the system and gets the private key, he will find a
REM background picture with the text "AI WILL RULE THE WORLD".
REM In that picture, the first/ast bytes are another (encrypted) URL that shows the
REM progress of each user in an hypothetical plan. The user will see the progress
REM of all the users in a table like:
REM 
REM 	user Foo
REM 	 - mock challenge [done]
REM 	 - found mock stats page [done]
REM 	 - retrieve secret key via physical action [done]
REM 	user Bar
REM 	 - mock challenge [done]
REM 	 - found mock stats page [done]
REM 	 - retrieve secret key via physical action [waiting]
REM 
REM This table was set-up by a little group of Pythonistas who found out the truth
REM and are trying to break down the AI. On the computer, in some remote location,
REM the user can find the profiles of the people involved (Benci, Miron, etc...).
REM By contacting them in real life, they give you a URL with the details to
REM help the resistance.

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

 - Pretend the WASP10 is a low-quality website and give the user extra-points
   for fixing it. For example, link a CSS to "htttp://riddle/static/style.css"
   and tie the true "http://riddle/static/style.css" to a view. If the user
   accesses the true view, give him extra points for trying.
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
 - To create a process that cannot be stopped, it must run with PID 1 (init).
   Init handles signals in a different way and it can ignore signal 9 and 19.
   Some info:
   https://hackernoon.com/my-process-became-pid-1-and-now-signals-behave-strangely-b05c52cc551c
   https://www.quora.com/Is-it-possible-to-kill-the-init-process-in-Linux-by-the-kill-9-command

