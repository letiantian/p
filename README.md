# p

P is a tool to change `PS1` quickly. **It's designed for bash and zsh.**

## Installation

```plain
$ sudo make install
$ \p --patch
```

Then, start a new bash/zsh and run `p`:  

![](./demo.gif)

## Details

`\p --patch` will append configurations into `~/.bashrc` and `~/.zshrc`. 

For  `~/.bashrc`, the configuration is: 
```shell
## config for p

alias p="p `basename $(ps -p$$ -o cmd=)` && source $HOME/.p"

## end
```

For  `~/.zshrc`, the configuration is: 
```shell
## config for p

autoload -U colors && colors
alias p="p `basename $(ps -p$$ -o cmd=)` && source $HOME/.p"

## end
```

`p` by default is installed to _/usr/local/bin_.  

Currently, `p` is implemented by _Python_. A version by _Shell_ is in the development.  Other programming languages will be used to implement `p`, but the timing is not clear.

## Reference 
[n](https://github.com/tj/n/)

[Color Bash Prompt - Archlinux wiki](https://wiki.archlinux.org/index.php/Color_Bash_Prompt)

[Zsh - Archlinux wiki](https://wiki.archlinux.org/index.php/Zsh)

[Zsh/Guide - gentoo wiki](https://wiki.gentoo.org/wiki/Zsh/Guide)

[How can I change the color of my prompt in zsh?](http://stackoverflow.com/questions/689765/how-can-i-change-the-color-of-my-prompt-in-zsh-different-from-normal-text)

[ANSI escape code - wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)  
[How do I get a single keypress at a time? - python docs](https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time)

[Terminal control/Preserve screen](http://rosettacode.org/wiki/Terminal_control/Preserve_screen)  

[Python method for reading keypress?](http://stackoverflow.com/questions/12175964/python-method-for-reading-keypress)  

[nodejs how to read keystrokes from stdin](http://stackoverflow.com/questions/5006821/nodejs-how-to-read-keystrokes-from-stdin)

[How to capture the arrow keys in node.js](http://stackoverflow.com/questions/17470554/how-to-capture-the-arrow-keys-in-node-js)


## License
MIT