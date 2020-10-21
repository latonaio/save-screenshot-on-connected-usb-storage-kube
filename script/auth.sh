#!/usr/bin/env bash
XAUTH=/home/$(whoami)/.docker.xauth.$USER
echo $XAUTH
touch $XAUTH
xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

