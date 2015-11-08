# p

P is a tool to change `PS1` quickly. It's designed for bash and zsh.

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

## License
MIT