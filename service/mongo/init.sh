#!/bin/bash

# Input your password
mongo admin -u admin -p secret --eval "db.createUser({user: 'myuser', pwd: 'secret123', roles:[{role:'readWrite',db:'dataprod'}]})"
