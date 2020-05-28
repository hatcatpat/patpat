tmux -2 attach-session -t patpat || tmux -2 \
  new-session -s patpat   \; \
  split-window -h -p 30 -t patpat \; \
  send-keys -t 0 "vim ~/Documents/patpat/Python/user_commands.py" C-m   \; \
  send-keys -t 1 "python ~/Documents/patpat/Python/main.py" C-m   \; \
  select-pane -t 0
