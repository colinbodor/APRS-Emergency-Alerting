#!/bin/sh
#tmux new-session -d -s aprs '/opt/APRS/aea/naads.py'


# -d says not to attach to the session yet. top runs in the first
# window
tmux new-session -d bash
# In the most recently created session, split the (only) window
# and run htop in the new pane
tmux split-window -h '/opt/APRS/aea/listen.py'
# Split the new pane and run perl
tmux split-window -h '/opt/APRS/aea/naads.py'
# Make all three panes the same size (currently, the first pane
# is 50% of the window, and the two new panes are 25% each).
tmux select-layout tiled
tmux resize-pane -U 8
# Now attach to the window
tmux attach-session
