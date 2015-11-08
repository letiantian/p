#!/usr/bin/env bash

#
# Because of the use of associative array, the version of bash should greater than 4
# 

VERSION="0.1.0"
UP=$'\033[A'
DOWN=$'\033[B'

CURRENT_SHELL=
CURRENT_CONFIG=

SHELLS=("bash"
        "zsh")

CONFIGS=("$HOME/.bashrc"
         "$HOME/.zshrc")

txtblk='\e[0;30m' # Black - Regular
txtred='\e[0;31m' # Red
txtgrn='\e[0;32m' # Green
txtylw='\e[0;33m' # Yellow
txtblu='\e[0;34m' # Blue
txtpur='\e[0;35m' # Purple
txtcyn='\e[0;36m' # Cyan
txtwht='\e[0;37m' # White
bldblk='\e[1;30m' # Black - Bold
bldred='\e[1;31m' # Red
bldgrn='\e[1;32m' # Green
bldylw='\e[1;33m' # Yellow
bldblu='\e[1;34m' # Blue
bldpur='\e[1;35m' # Purple
bldcyn='\e[1;36m' # Cyan
bldwht='\e[1;37m' # White
unkblk='\e[4;30m' # Black - Underline
undred='\e[4;31m' # Red
undgrn='\e[4;32m' # Green
undylw='\e[4;33m' # Yellow
undblu='\e[4;34m' # Blue
undpur='\e[4;35m' # Purple
undcyn='\e[4;36m' # Cyan
undwht='\e[4;37m' # White
bakblk='\e[40m'   # Black - Background
bakred='\e[41m'   # Red
bakgrn='\e[42m'   # Green
bakylw='\e[43m'   # Yellow
bakblu='\e[44m'   # Blue
bakpur='\e[45m'   # Purple
bakcyn='\e[46m'   # Cyan
bakwht='\e[47m'   # White
txtrst='\e[0m'    # Text Reset  - Reset

declare -A prompt_bash
declare -A prompt_zsh

prompt_bash=(
        ["\[${txtgrn}\]\$ \[${txtrst}\]"]="${txtgrn}\$ ${txtrst}ls -l"
        ["\[${txtblu}\]\$ \[${txtrst}\]"]="${txtblu}\$ ${txtrst}ls -l"
        ["\[${txtpur}\]\$ \[${txtrst}\]"]="${txtpur}\$ ${txtrst}ls -l"
        ["\[${txtcyn}\]\$ \[${txtrst}\]"]="${txtcyn}\$ ${txtrst}ls -l"

        ["\[${bldgrn}\]\$ \[${txtrst}\]"]="${bldgrn}\$ ${txtrst}ls -l"
        ["\[${bldblu}\]\$ \[${txtrst}\]"]="${bldblu}\$ ${txtrst}ls -l"
        ["\[${bldpur}\]\$ \[${txtrst}\]"]="${bldpur}\$ ${txtrst}ls -l"
        ["\[${bldcyn}\]\$ \[${txtrst}\]"]="${bldcyn}\$ ${txtrst}ls -l"

        ["\[${bldcyn}\]\u\[${txtrst}\]@\[${bldylw}\]\h\[${txtrst}\] \[${bldgrn}\]\w\[${txtrst}\] \[${bldylw}\]\$ \[${txtrst}\]"]="${bldcyn}user${txtrst}@${bldylw}hostname${txtrst} ${bldgrn}/home/foo${txtrst} ${bldylw}\$ ${txtrst}ls -l"
        ["\[${txtcyn}\]\u\[${txtrst}\]@\[${txtylw}\]\h\[${txtrst}\] \[${txtgrn}\]\w\[${txtrst}\] \[${txtylw}\]\$ \[${txtrst}\]"]="${txtcyn}user${txtrst}@${txtylw}hostname${txtrst} ${txtgrn}/home/foo${txtrst} ${txtylw}\$ ${txtrst}ls -l"

        ["\[${bldcyn}\]\u\[${txtrst}\]@\[${bldylw}\]\h\[${txtrst}\]:\[${bldgrn}\]\w\[${txtrst}\] \[${bldylw}\]\$ \[${txtrst}\]"]="${bldcyn}user${txtrst}@${bldylw}hostname${txtrst}:${bldgrn}/home/foo${txtrst} ${bldylw}\$ ${txtrst}ls -l"
        ["\[${txtcyn}\]\u\[${txtrst}\]@\[${txtylw}\]\h\[${txtrst}\]:\[${txtgrn}\]\w\[${txtrst}\] \[${txtylw}\]\$ \[${txtrst}\]"]="${txtcyn}user${txtrst}@${txtylw}hostname${txtrst}:${txtgrn}/home/foo${txtrst} ${txtylw}\$ ${txtrst}ls -l"

        ["\[${bldcyn}\]\u\[${txtrst}\]@\[${bldylw}\]\h\[${txtrst}\]:\[${bldgrn}\]\w\[${txtrst}\] \[${bldylw}\]\n\$ \[${txtrst}\]"]="${bldcyn}user${txtrst}@${bldylw}hostname${txtrst}:${bldgrn}/home/foo${txtrst} ${bldylw}\n     \$ ${txtrst}ls -l"
        ["\[${txtcyn}\]\u\[${txtrst}\]@\[${txtylw}\]\h\[${txtrst}\]:\[${txtgrn}\]\w\[${txtrst}\] \[${txtylw}\]\n\$ \[${txtrst}\]"]="${txtcyn}user${txtrst}@${txtylw}hostname${txtrst}:${txtgrn}/home/foo${txtrst} ${txtylw}\n     \$ ${txtrst}ls -l"


        ["[\u@\h \w] \A \$ "]="[user@hostname /home/foo] 13:59 \$ "
        ["\[${txtcyn}\]\u@\h \w \A \$ \[${txtrst}\]"]="${txtcyn}user@hostname /home/foo 13:59 \$ ${txtrst}"
    )

prompt_zsh=(
        ["$ "]="$ "
    )



function log() {`
    printf "  \033[90m$@\033[0m\n"
}

function abort() {
    printf "\n  \033[31mError: $@\033[0m\n\n" && exit 1
}

function help_zsh() {
    echo
    log  "Be sure of that \"autoload -U colors && colors\" added before \"PROMPT=\" or \"PS1=\" in $HOME/.zshrc"
}

function get_rows() {
    tput lines
}

function check_shell() {
    if [ $# -eq 0 ]; then
        abort "There is no info about shell was given."
    fi
    s=$1
    let idx=0
    while [ $idx -lt ${#SHELLS[@]} ]; do
        if [ "$s" == "${SHELLS[$idx]}" ]; then
            CURRENT_SHELL=${SHELLS[$idx]}
            CURRENT_CONFIG=${CONFIGS[$idx]}
        fi
        let idx++
    done
    if [ -z "${CURRENT_SHELL}" ]; then
        abort "only bash and zsh are supported."
    fi
}

function enter_fullscreen() {
    tput smcup
    stty -echo
    printf "\e[?25l"    # hide cursor
}

function leave_fullscreen() {
    tput rmcup
    stty echo
    printf "\e[?25h"    # show cursor
}

handle_sigint() {
  leave_fullscreen
  exit $?
}

handle_sigtstp() {
  leave_fullscreen
  kill -s SIGSTOP $$
}

function check_prompts() {
    prompts=()
    examples=()
    let prompts_amount=0

    cmd="
    for key in \"\${!prompt_${CURRENT_SHELL}[@]}\"; do      
        prompts+=(\"\$key\");                      
        examples+=(\"\${prompt_${CURRENT_SHELL}[\$key]}\");
        let prompts_amount++;   
    done
    "

    eval "$cmd"


    # for key in "${!prompt_bash[@]}"; do
    #     prompts+=("$key")       # 必须加引号
    #     examples+=("${prompt_bash[$key]}")
    #     let prompts_amount++
    # done

    if [ $prompts_amount -eq 0 ]; then
        abort "no prompts"
    fi

    ## test
    # echo ${prompts[0]}
    # for var in "${prompts[@]}"; do
    #     echo $var
    # done
    # for var in "${examples[@]}"; do
    #     echo $var
    # done

}

#
# ceiling_divide 32 6 -> 6
#

function ceiling_divide() {
    ceiling_result=$(($1/$2))
    if [ $(($1%$2)) -gt 0 ]; then
        ceiling_result=$((ceiling_result + 1))
    fi
    echo $ceiling_result
}

function display_prompts() {
    local prompt_start
    local prompt_end
    local rows=$(get_rows)
    local display_amount=$prompts_amount

    test $rows -lt 6 && abort "the window is too small"

    let display_amount=rows/2-1  # 一次最多显示这么多
    test $display_amount -lt 1 && let display_amount=1

    let prompt_start=prompt_current/display_amount*display_amount
    let prompt_end=prompt_current/display_amount*display_amount+display_amount

    test $prompt_start -ge $(($prompts_amount-1)) && let prompt_start=prompts_amount-1
    test $prompt_end -ge $(($prompts_amount-1)) && let prompt_end=prompts_amount


    while [ $prompt_start -lt $prompt_end ]; do
        echo
        if [ $prompt_start -eq $prompt_current ]; then
            printf "  \033[36m-> \033[0m${examples[$prompt_start]}\033[0m\n" 
        else
            printf "     \033[0m${examples[$prompt_start]}\033[0m\n" 
        fi
        let prompt_start++
    done
}

function prev_prompt() {
    let prompt_current--
    if [ $prompt_current -lt 0 ]; then
        let prompt_current=prompts_amount-1
    fi
}

function next_prompt() {
    let prompt_current++
    if [ $prompt_current -ge $prompts_amount ]; then
        let prompt_current=0
    fi
}

function activate() {
    echo "export PS1=\"${prompts[$prompt_current]}\"" > $HOME/.p
}

function select_prompt() {
    check_shell $1
    check_prompts
    let prompt_current=0

    enter_fullscreen
    display_prompts

    trap handle_sigint INT
    trap handle_sigtstp SIGTSTP
    
    while true; do
        read -n 3 c
        case "$c" in
            $UP)
                clear; prev_prompt; display_prompts
                ;;
            $DOWN)
                clear; next_prompt; display_prompts
                ;;
            *)
                leave_fullscreen; activate;  exit
                ;;
        esac
    done
}

select_prompt $@
