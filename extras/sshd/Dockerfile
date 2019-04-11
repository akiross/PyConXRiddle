FROM alpine:3.9

# Serving ssh
EXPOSE 22

# We need a user and a password to create
ARG GAME_USER
ARG GAME_PASS
# We also need a message to print user when logging in
ARG GAME_NLOG

# Ensure they are given!
RUN test -n "$GAME_USER" && test -n "$GAME_PASS" && test -n "$GAME_NLOG"

# Install daemon and setup dirs
RUN apk add --no-cache openssh ; mkdir -p /var/run/sshd

# Use configuration that basically let user do nothing
COPY sshd_config /etc/ssh/sshd_config

# Create game user and password, it's ok to have this info in docker inspect
RUN adduser -s /sbin/nologin -D "$GAME_USER" ; \
    echo "$GAME_USER:$GAME_PASS" | chpasswd ; \
	echo "$GAME_NLOG" >/etc/nologin.txt

# Generate keypair, every time we change configuration this will change
RUN ssh-keygen -t ed25519 -N '' -f /etc/ssh/ssh_host_ed25519_key

# Start server
CMD ["/usr/sbin/sshd", "-D"]
