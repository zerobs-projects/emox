#!/bin/bash


# filelimiting-tweaking
ulimit -n 1000000


SESSIONNAME="EMOX"
SCRIPT="python3 ./gna.py"
tmux has-session -t $SESSIONNAME &> /dev/null



if [ $? != 0 ] 
 then
    tmux new-session -s $SESSIONNAME -n script -d
    tmux send-keys -t $SESSIONNAME "$SCRIPT" C-m 
    tmux new-window -t $SESSIONNAME 'vnstat -l'
    tmux select-window -t $SESSIONNAME:0 \; a -t $SESSIONNAME


fi

tmux attach -t $SESSIONNAME
