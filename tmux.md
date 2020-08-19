## Aliases

```
alias tkill='tmux kill-server'
alias tatt='tmux attach -t main'
alias tls='tmux ls'
```

## Script Execution

I can run the following code from the `.bash_profile` file to have a tmux session straight after logging in to the cluster.
```
tmux_clients=$(tmux list-clients -t Main | wc -l)
if [[ $tmux_clients = 0 ]]; then
    source $HOME/trun.sh
fi
```

The file `trun.sh` which I want to execute on a startup may have the following content:
```
sessions=$(tmux ls | cut -d ':' -f1)

if [[ -n $sessions ]] && [[ $sessions == *"Main"* ]]; then
    tmux attach -t Main
else
    tmux new-session -s Main -n 'tty' -d
    
    tmux new-window -n 'tty'

    tmux new-window -n 'tty'

    tmux new-window -n 'tty'

    tmux new-window -n 'monitoring'
    tmux split-window -h
    tmux send-keys -t "1" 'htop' Enter
    tmux select-pane -t "2"
    tmux send-keys -t "2" 'watch -n 1.0 nvidia-smi' Enter

    tmux new-window -n 'jupyter'

    tmux select-window -t 1

    tmux attach -t 'Main'
fi
```

## Configuration

Example of the configuration file with style and keybings definitions:

###### <center>tmux.conf</center>
```
# =======================================================
#                       GENERAL SETTINGS
# =======================================================

# Remap prefix from 'C-b' (Control-b) to 'M-a' (Alt-a)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Deleting history with clear as it adds a blank line making a gap between the status line and prompt
bind -n C-l send-keys "C-e"\; send-keys "C-u"\; send-keys "clear"\; send-keys "Enter"

# Launch tmux with a non-login shell
set -g default-command "${SHELL}"

# Time for a message to appear
set-option -g display-time 1000

# No delay for escape key press
set -sg escape-time 0

# History limit
set -g history-limit 20000

# Hide the status bar
bind q set status


# =======================================================
#                  WINDOWS AND PANES 
# =======================================================

# Default name for a newly created window
bind c new-window -n 'tty'

# Indexing
set -g base-index 1
set -g pane-base-index 1
set -g renumber-windows on    # renumber windows when a window is closed
set -g allow-rename off

# Split panes using \ and -
bind \ split-window -h -c '#{pane_current_path}'
bind - split-window -v -c '#{pane_current_path}'
unbind '"'
unbind %

# Use Alt + vim arrows to switch panes
bind -n M-h select-pane -L 
bind -n M-j select-pane -D 
bind -n M-k select-pane -U 
bind -n M-l select-pane -R 

# Use Alt + n/p to switch window
bind -n M-p previous-window 
bind -n M-n next-window      

# Use Alt + number to select a window
bind -n M-1 select-window -t 1 
bind -n M-2 select-window -t 2 
bind -n M-3 select-window -t 3 
bind -n M-4 select-window -t 4 
bind -n M-5 select-window -t 5 
bind -n M-6 select-window -t 6 
bind -n M-7 select-window -t 7 
bind -n M-8 select-window -t 8 
bind -n M-9 select-window -t 9 

# Toggle last window
bind -n M-b last-window

# Pane Border colors
set -g pane-border-style 'fg=#7C5400'
set -g pane-active-border-style 'fg=#FFB414'


# =======================================================
#                      MOUSE MODE
# =======================================================

# Enable mouse mode
set -g mouse on

# Unbind righ mouse click (which marks a pane as M)
unbind-key -n MouseDown3Pane

# Drag windows on the status bar
bind-key -n MouseDrag1Status swap-window -t=

# Mouse selection
bind -T copy-mode-vi MouseDragEnd1Pane select-pane \;\

# Clear selection
bind -T copy-mode-vi MouseDown1Pane select-pane \; send-keys -X clear-selection


# =======================================================
#                       VI MODE                       
# =======================================================

# turn on vi mode
setw -g mode-keys vi
set -g status-keys vi

# copy-paste mode
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection
bind -T copy-mode-vi r send-keys -X rectangle-toggle

# copy to linux clipboard
bind -T copy-mode-vi y select-pane \;\
    send-keys -X copy-pipe "xclip -i -selection clipboard" \;\
    send-keys -X clear-selection \;\
    display-message "Highlighted selection copied to system clipboard" 

# copy to linux clipboard wo clearing selection
bind -T copy-mode-vi C-c send-keys -X copy-pipe "xclip -i -selection clipboard" \;\
    display-message "Highlighted selection copied to system clipboard" 


# =======================================================
#                       STATUS BAR                      
# =======================================================

set -g status-position top
set -g status-style "bg=colour236"

set -g status-left ""
set -g status-right "#[fg=colour246]Session: #[fg=colour117]#S"
set -g status-right-length 20

set -g status-justify left
setw -g window-status-separator '  '

setw -g window-status-style "fg=colour13,none,bg=colour239"
setw -g window-status-format ' #I#[fg=colour250]:#[fg=colour250]#W '

setw -g window-status-current-style "fg=colour117,bold,bg=colour242"
setw -g window-status-current-format ' #I#[fg=colour250]:#[fg=colour255]#W#[fg=colour117]#F '

# message line for commands
set -g message-style "fg=colour11, bg=colour236"

# toggle local/remote bar
bind -T root F12  \
    set prefix None \;\
    set key-table off \;\
    set status-style "bg=colour236" \;\
    setw -g window-status-style "fg=colour246,none,bg=colour236" \;\
    setw -g window-status-format ' #I#[fg=colour246]:#[fg=colour246]#W ' \;\
    set window-status-current-style "fg=colour246,bold,bg=colour236" \;\
    set window-status-current-format ' #I#[fg=colour246]:#[fg=colour246]#W#[fg=colour246]#F ' \;\
    refresh-client -S    

bind -T off F12 \
    set -u prefix \;\
    set -u key-table \;\
    set -u status-style \;\
    set -g window-status-style "fg=colour13,none,bg=colour239" \;\
    set -g window-status-format ' #I#[fg=colour250]:#[fg=colour250]#W ' \;\
    set -u window-status-current-style \;\
    set -u window-status-current-format \;\
    refresh-client -S

# ======================================================
#                       PLUGINS                      
# ======================================================

# allow plugins usage
set -g @plugin 'tmux-plugins/tpm'

# plugin for correct behavior less/man with mouse scrolling
set -g @plugin 'nhdaly/tmux-better-mouse-mode'
set -g @emulate-scroll-for-no-mouse-alternate-buffer 'on'

# required line
run -b '~/.tmux/plugins/tpm/tpm'
```
