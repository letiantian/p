#!/usr/bin/env python
from __future__ import print_function

import termios, fcntl, sys, os, time, signal

if sys.version_info <(2,7):
    raise Exception('The version of python should greater than or equal to 2.7')

VERSION        = '0.1.0'

CURRENT_SHELL  = ''
CURRENT_CONFIG = ''
PROMPT_CURRENT = 0
PROMPTS        = None

SHELLS  = ('bash', 'zsh')

CONFIGS = dict(
        bash=os.getenv('HOME')+'/.bashrc',
        zsh=os.getenv('HOME')+'/.zshrc',
    )

PCONFIG = os.getenv('HOME')+'/.p'

COLORS  = dict(
        txtblk='\033[0;30m', # Black - Regular
        txtred='\033[0;31m', # Red
        txtgrn='\033[0;32m', # Green
        txtylw='\033[0;33m', # Yellow
        txtblu='\033[0;34m', # Blue
        txtpur='\033[0;35m', # Purple
        txtcyn='\033[0;36m', # Cyan
        txtwht='\033[0;37m', # White
        bldblk='\033[1;30m', # Black - Bold
        bldred='\033[1;31m', # Red
        bldgrn='\033[1;32m', # Green
        bldylw='\033[1;33m', # Yellow
        bldblu='\033[1;34m', # Blue
        bldpur='\033[1;35m', # Purple
        bldcyn='\033[1;36m', # Cyan
        bldwht='\033[1;37m', # White
        unkblk='\033[4;30m', # Black - Underline
        undred='\033[4;31m', # Red
        undgrn='\033[4;32m', # Green
        undylw='\033[4;33m', # Yellow
        undblu='\033[4;34m', # Blue
        undpur='\033[4;35m', # Purple
        undcyn='\033[4;36m', # Cyan
        undwht='\033[4;37m', # White
        bakblk='\033[40m',   # Black - Background
        bakred='\033[41m',   # Red
        bakgrn='\033[42m',   # Green
        bakylw='\033[43m',   # Yellow
        bakblu='\033[44m',   # Blue
        bakpur='\033[45m',   # Purple
        bakcyn='\033[46m',   # Cyan
        bakwht='\033[47m',   # White
        txtrst='\033[0m'     # Text Reset  - Reset
    )
PROMPT_BASH = (
        dict(
            prompt  = '\[{txtgrn}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{txtgrn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{txtcyn}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{txtcyn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldgrn}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{bldgrn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{bldcyn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldylw}\]\$ \[{txtrst}\]'.format(**COLORS), 
            example = '{bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldgrn}\]% \[{txtrst}\]'.format(**COLORS), 
            example = '{bldgrn}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]% \[{txtrst}\]'.format(**COLORS), 
            example = '{bldcyn}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldylw}\]% \[{txtrst}\]'.format(**COLORS), 
            example = '{bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtcyn}\]\u\[{txtrst}\]@\[{txtylw}\]\h\[{txtrst}\] \[{txtgrn}\]\w\[{txtrst}\] \[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} {txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]\u\[{txtrst}\]@\[{bldylw}\]\h\[{txtrst}\] \[{bldgrn}\]\w\[{txtrst}\] \[{bldylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} {bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtcyn}\]\u\[{txtrst}\]@\[{txtylw}\]\h\[{txtrst}\] \[{txtgrn}\]\w\[{txtrst}\] \[{txtylw}\]% \[{txtrst}\]'.format(**COLORS),
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} {txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]\u\[{txtrst}\]@\[{bldylw}\]\h\[{txtrst}\] \[{bldgrn}\]\w\[{txtrst}\] \[{bldylw}\]% \[{txtrst}\]'.format(**COLORS),
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} {bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtcyn}\]\u\[{txtrst}\]@\[{txtylw}\]\h\[{txtrst}\] \[{txtgrn}\]\w\[{txtrst}\] \n\[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} \n{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]\u\[{txtrst}\]@\[{bldylw}\]\h\[{txtrst}\] \[{bldgrn}\]\w\[{txtrst}\] \n\[{bldylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} \n{bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtcyn}\]\u\[{txtrst}\]@\[{txtylw}\]\h\[{txtrst}\] \[{txtgrn}\]\w\[{txtrst}\] \n\[{txtylw}\]% \[{txtrst}\]'.format(**COLORS),
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} \n{txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '\[{bldcyn}\]\u\[{txtrst}\]@\[{bldylw}\]\h\[{txtrst}\] \[{bldgrn}\]\w\[{txtrst}\] \n\[{bldylw}\]% \[{txtrst}\]'.format(**COLORS),
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} \n{bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtpur}\]\u@\h \w\[{txtrst}\] \n\[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{txtpur}user@hostname /home/foo{txtrst} \n{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{txtcyn}\]\u@\h \A \w\[{txtrst}\] \n\[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{txtcyn}user@hostname 13:46 /home/foo{txtrst} \n{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '\[{bakcyn}\]\u@\h \w\[{txtrst}\] \n\[{txtylw}\]\$ \[{txtrst}\]'.format(**COLORS),
            example = '{bakcyn}user@hostname /home/foo{txtrst} \n{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),

    )

PROMPT_ZSH = (
        dict(
            prompt  = '%{$fg[green]%}\$ %{$reset_color%}', 
            example = '{txtgrn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg[cyan]%}\$ %{$reset_color%}', 
            example = '{txtcyn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg[yellow]%}\$ %{$reset_color%}', 
            example = '{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[green]%}\$ %{$reset_color%}', 
            example = '{bldgrn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}\$ %{$reset_color%}\[{bldcyn}\]$ \[{txtrst}\]', 
            example = '{bldcyn}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[yellow]%}\$ %{$reset_color%}', 
            example = '{bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[green]%}%# %{$reset_color%}', 
            example = '{bldgrn}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}%# %{$reset_color%}', 
            example = '{bldcyn}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[yellow]%}%# %{$reset_color%}', 
            example = '{bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '%{$fg[cyan]%}%n%{$reset_color%}@%{$fg[yellow]%}%M%{$reset_color%} %{$fg[green]%}%d%{$reset_color%} %{$fg[yellow]%}$ %{$reset_color%}',
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} {txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}%n%{$reset_color%}@%{$fg_bold[yellow]%}%M%{$reset_color%} %{$fg_bold[green]%}%d%{$reset_color%} %{$fg_bold[yellow]%}$ %{$reset_color%}',
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} {bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg[cyan]%}%n%{$reset_color%}@%{$fg[yellow]%}%M%{$reset_color%} %{$fg[green]%}%d%{$reset_color%} %{$fg[yellow]%}%# %{$reset_color%}',
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} {txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}%n%{$reset_color%}@%{$fg_bold[yellow]%}%M%{$reset_color%} %{$fg_bold[green]%}%d%{$reset_color%} %{$fg_bold[yellow]%}%# %{$reset_color%}',
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} {bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),


        dict(
            prompt  = '%{$fg[cyan]%}%n%{$reset_color%}@%{$fg[yellow]%}%M%{$reset_color%} %{$fg[green]%}%d%{$reset_color%} \n%{$fg[yellow]%}$ %{$reset_color%}',
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} \n{txtylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}%n%{$reset_color%}@%{$fg_bold[yellow]%}%M%{$reset_color%} %{$fg_bold[green]%}%d%{$reset_color%} \n%{$fg_bold[yellow]%}$ %{$reset_color%}',
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} \n{bldylw}$ {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg[cyan]%}%n%{$reset_color%}@%{$fg[yellow]%}%M%{$reset_color%} %{$fg[green]%}%d%{$reset_color%} \n%{$fg[yellow]%}%# %{$reset_color%}',
            example = '{txtcyn}user{txtrst}@{txtylw}hostname{txtrst} {txtgrn}/home/foo{txtrst} \n{txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),
        dict(
            prompt  = '%{$fg_bold[cyan]%}%n%{$reset_color%}@%{$fg_bold[yellow]%}%M%{$reset_color%} %{$fg_bold[green]%}%d%{$reset_color%} \n%{$fg_bold[yellow]%}%# %{$reset_color%}',
            example = '{bldcyn}user{txtrst}@{bldylw}hostname{txtrst} {bldgrn}/home/foo{txtrst} \n{bldylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '%{$fg[cyan]%}%n@%M %d%{$reset_color%}\n%{$fg[yellow]%}%# %{$reset_color%}',
            example = '{txtcyn}user@hostname /home/foo{txtrst} \n{txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),

        dict(
            prompt  = '%{$fg[cyan]%}%n@%M %T %d%{$reset_color%}\n%{$fg[yellow]%}%# %{$reset_color%}',
            example = '{txtcyn}user@hostname 13:46 /home/foo{txtrst} \n{txtylw}% {txtrst}ls -l'.format(**COLORS)
            ),

    )


def get_terminal_rows():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows)


def log(msg):
    print('  \033[90m{msg}\033[0m'.format(msg=str(msg)))


def abort(msg):
    print('\n  \033[31mError: {msg}\033[0m\n\n'.format(msg=str(msg)))
    sys.exit(1)


def version():
    global VERSION
    print(VERSION)

def help():
    print('''

        help

        ''')


def patch_config():
    def write2file(data, file_path):
        with open(file_path, 'a') as out:
            for line in data.split('\n'):
                line = line.strip()
                out.write(line+'\n')

    bash_patch = '''
    ## config for p
    
    alias p="p `basename $(ps -p$$ -o cmd=)` && source $HOME/.p"
    
    ## end
    '''
    zsh_patch = '''
    ## config for p
    
    autoload -U colors && colors
    alias p="p `basename $(ps -p$$ -o cmd=)` && source $HOME/.p"
    
    ## end
    '''

    log('patching {name}'.format(name=CONFIGS['bash']))
    time.sleep(0.5)
    write2file(bash_patch, CONFIGS['bash'])

    log('patching {name}'.format(name=CONFIGS['zsh']))
    time.sleep(0.5)
    write2file(zsh_patch, CONFIGS['zsh'])

    log('Done')
    log('')
    log('It will take effect afeter start a new terminal')


def check_shell(shell_info):
    shell_info = os.path.basename(shell_info)
    if shell_info not in SHELLS:
        abort("only bash and zsh are supported.")
    global CURRENT_SHELL
    CURRENT_SHELL = shell_info


def check_prompts():
    assert CURRENT_SHELL in SHELLS
    global PROMPTS
    PROMPTS = PROMPT_BASH if CURRENT_SHELL=='bash' else PROMPT_ZSH
    if len(PROMPTS) == 0:
        abort("the number of prompts for {shell} is 0".format(shell=CURRENT_SHELL))


def hide_cursor():
    print('\033[?25l')


def show_cursor():
    print('\033[?25h')


def enter_fullscreen():
    print('\033[?1049h\033[H')
    os.system("stty -echo")
    hide_cursor()


def leave_fullscreen():
    print('\033[?1049l')
    os.system("stty echo")
    show_cursor()


def handle_sigint(signum, stack):
    leave_fullscreen()
    sys.exit(1)


def handle_sigtstp(signum, stack):
    leave_fullscreen()
    sys.exit(1)
    # os.kill(os.getpid(), signal.SIGSTOP)


def prev_prompt():
    global PROMPT_CURRENT
    PROMPT_CURRENT -= 1
    if PROMPT_CURRENT < 0:
        PROMPT_CURRENT = len(PROMPTS) - 1


def next_prompt():
    global PROMPT_CURRENT
    PROMPT_CURRENT += 1
    if PROMPT_CURRENT > len(PROMPTS) - 1:
        PROMPT_CURRENT = 0


def clear():
    os.system('clear')


def activate():
    prompt = PROMPTS[PROMPT_CURRENT]['prompt']
    with open(PCONFIG, 'w') as out:
        out.write("export PS1=\"{prompt}\"".format(prompt=prompt))


def display_prompts():
    
    def display(example, selected=False):
        lines = example.split('\n')
        flagged = False
        result = []
        result.append('')
        for line in lines:
            if selected and (not flagged):
                result.append('  \033[36m-> \033[0m{line}\033[0m'.format(line=line))
                flagged = True
            else:
                result.append('     \033[0m{line}\033[0m'.format(line=line))
        return result

    rows           = get_terminal_rows()

    if rows < 6: 
        abort("the window is too small")
    rows = rows-2

    idx = PROMPT_CURRENT
    display_result = display(PROMPTS[idx]['example'], idx == PROMPT_CURRENT)
    up_idx = idx-1
    down_idx = idx+1

    while len(display_result) < rows:
        old_result = display_result[:]
        if up_idx >= 0:
            display_result = display(PROMPTS[up_idx]['example'], False) + display_result
            if len(display_result) > rows:
                display_result = old_result[:]
                break
        old_result = display_result[:]
        if down_idx < len(PROMPTS):
            display_result += display(PROMPTS[down_idx]['example'], False)
            if len(display_result) > rows:
                display_result = old_result[:]
                break
        up_idx   -= 1
        down_idx += 1

        if up_idx < 0 and down_idx >= len(PROMPTS):
            break
        
    print('\n'.join(display_result))


def select_prompt(shell_info):

    check_shell(shell_info)
    check_prompts()

    global PROMPT_CURRENT
    UP   = '\033[A'
    DOWN = '\033[B'

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTSTP, handle_sigtstp)

    enter_fullscreen()
    clear()
    display_prompts()

    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(3)
                if c == UP:
                    prev_prompt()
                    clear()
                    display_prompts()
                elif c == DOWN:
                    next_prompt()
                    clear()
                    display_prompts()
                elif c == '\n':
                    activate()
                    break
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        leave_fullscreen()



## main

def main():

    if len(sys.argv[1:]) == 0:
        help()
        return

    for arg in sys.argv[1:]:
        if arg in ('-h', '--help'):
            help()
            return
        elif arg in ('-v', '--version'):
            version()
            return
        elif arg in ('--patch', ):
            patch_config()
            return
        else:
            select_prompt(arg)
            return

if __name__ == '__main__':
    main()