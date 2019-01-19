# PyConXRiddle
The riddle for PyCon X

The idea is to have a web server that can be used to serve riddles.
Riddles are described in modules (one per riddle) and dependencies among levels
are described with a directory structure:

 - all riddles in a directory shall be completed before the riddles in the
   sub-directories are accessible;
 - there is no order in how the riddles within the same directory are accessed.

Each riddle has an entry-point which is enabled when the riddle is enabled.

## Example structure

     game/
      +--- intro.py
      +--. level0
         +--- testA0.py
         +--- testB0.py
         +--- testC0.py
         +--. level1A
         |  +--- testA1.py
         |  +--. level2
         |     +--- testA2.py
         +--. level1B
            +--- testB1.py

In this case, to win the game the user shall complete the intro level first,
then he can complete tests A0, B0 or C0 in any order, but tests A1, A2 and B1
are not accessible. Once A0, B0 and C0 are completed, A1 and B1 are accessible,
and after A1 is complete, A2 can be accessed to beat the game. Note that it is
not necessary to complete test B1 to access A2, as in folder level1A there is
only one module, testA1, which is the sole requisite to access level2.
  
## Codebase

One shall strive to make the game the more stateless as possible. The software
stores the progress of the game (which levels have been completed) in a cookie
on the browser. It should be possible to continue the game given that cookie.
When a cookie is created, an unique ID is generated to identify the user.

Using using a stateless server helps in:
 - scaling easily (no databases required);
 - faster serving (just resume where you left by a sequence of if-elses);
 - easier maintainance (don't worry about lost data);
 - easier versioning of the riddles, in case their working changes.

Each riddle is in a single python file (usually, they are not huge), and they
will export some data used by the software.


## Install

It's possible to install the project dependecies with pipenv:

`pipenv install`

or pip:

`pip install -r requirements.txt`


## Run

A configuration `.cfg` file is needed to run the application.
There is a ready made file `dev.cfg` in the root of the project that can be used for development.

The database should be initialized calling the command:

`flask init-db` 

The path of the preferred config file should be set to the environment variable `RIDDLE_CONFIG`:

`export RIDDLE_CONFIG=/path/to/config/file`

To run the application execute this command:

`flask run`

for production this one:

`gunicorn -w {worker_number} -b {host}:{port} 'riddle:create_app()'`

(obviusly you need to replace the placeholders with the correct values)