# SSH Control-Master
By default, ssh creates a new connection each time you login to a remote host. This is inneficient as well as it's quite annoying to have to authenticate each time you connect.

Arguably the best solution is to use a facility build into ssh called "Control Master". instead of using a new connection each time, it makes a connection and binds it to a unix socket which can be used and re-used by many ssh processes.

To setup ssh controlmaster, run the following in your terminal
```bash
cat <<EOF>>$HOME/.ssh/config
Host *
    GSSAPIAuthentication no
    ControlMaster auto
    ControlPath ~/.ssh/sockets/ssh_mux_%h_%p_%r
    ControlPersist 2h
    ServerAliveInterval 60
    ServerAliveCountMax 10
EOF
mkdir $HOME/.ssh/sockets
```

That's it. The next time you connect to a remote host, you will have to authenticate, from then until you lose the connection, any ssh process will use the same connection.