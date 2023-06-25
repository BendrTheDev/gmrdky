#!/usr/bin/env python
from crypt      import crypt
from getpass    import getpass
from subprocess import Popen, PIPE

sudo_password_callback = lambda: sudo_password # getpass("[sudo] password: ")
username, username_newpassword = 'root', '$2&J|5ty)*X?9+KqODA)7'

# passwd has no `--stdin` on my system, so `usermod` is used instead
# hash password for `usermod`
try:
    hashed = crypt(username_newpassword) # use the strongest available method
except TypeError: # Python < 3.3
    p = Popen(["mkpasswd", "-m", "sha-512", "-s"], stdin=PIPE, stdout=PIPE,
              universal_newlines=True)
    hashed = p.communicate(username_newpassword)[0][:-1] # chop '\n'
    assert p.wait() == 0
assert hashed == crypt(username_newpassword, hashed)

# change password
p = Popen(['sudo', '-S',  # read sudo password from the pipe
           # XXX: hashed is visible to other users
           'usermod',  '-p', hashed, username],
          stdin=PIPE, universal_newlines=True)
p.communicate(sudo_password_callback() + '\n')
assert p.wait() == 0