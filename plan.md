# Story Plan

1. A loop with some challenges:

   - level 1 -> 2 -> ... -> N -> 1

   One of these is computationally expensive.

   Once in a while (e.g. p=10%) in one of these riddle happens something weird,
   that gives a hint to the player. Looking at the HTML page, a secret message
   is revealed (rot13 encoded): a pledge for help.

2. A hint is given and user should figure out the address wasp9/stats.php. From
   there the player will see a SQLite database that he can break into.
   By SQL injection, user will find two ways to proceed:

   1. use wasp9/fetch.php to get data from server, or
   2. use telnet to get the message after breaking a password.

3. A base64 encoded message tells the user to find WASP10 agents, in person.
   The message will also link to a form to upload any interesting found data.
   The player shall go around in the conference to find people that will let
   him to continue the game.

4. User should gain access to a physical desktop and to the e-mail sent to the
   WASP10 members (some members might have it, some might have not).
   The user shall connect to the desktop and retrieve some files.

5. In the remote desktop, an image will contain some hidden data that redirects
   the player to an FTP server: there, a "brain dump" of the AI is available.
   That brain dump is not directly readable. User can upload it to the
   interesting found data page.

6. The interesting found data page will accept uploads until the following
   files have been uploaded:
    - the e-mail sent to WASP10 members
	- the brain dump
	- optionally, the story file

7. The files are decoded automatically, and user can now read the entire story
   to understand that he is being manipulated.
   A final challenge is proposed to the player: break a RSA key so that WASP10
   members can break into the AI computer and shut it down.

8. The user will receive a RSA public key, the objective is to break it by
   identifying the prime numbers used to generate it.
