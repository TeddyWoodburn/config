HISTSIZE=1000
SAVEHIST=2000
HISTFILE=~/.zsh_history
setopt hist_ignore_dups hist_ignore_space append_history

PROMPT='%K{green}%F{black}%n %~%f%k '

alias ls='ls --color=auto'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

alias k=kubectl
alias kns=kubens

alias pipo='python3 ~/Documents/pip_cache/offline_pip.py'
alias pyhton3=python3
alias pytohn3=python3
alias py=python3

fpath=(~/Documents/.zsh/completions $fpath)
autoload -Uz compinit
compinit

bindkey -v
