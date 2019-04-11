# sshd

This directory contains tool to create a sshd server that user can play with.

Additional information is given to the user when he tries to log-in. User shall
own valid username and password to login, and the server will just yield a
message which contains the information for the user to continue.

The server is configured for a single user that has no port forwarding and no
login (/sbin/nologin). The /etc/nologin.txt is set to a custom message that can
help the user in its journey.

To build the image, you can use this command

    docker build -t game_sshd \
                 --build-arg GAME_USER=monty-python \
    		     --build-arg GAME_PASS=somepass \
    		     --build-arg GAME_NLOG="Cannot connect to http://example.com" .
