Vimapt
===
**The missing package manager for Vim**


Vimapt is a vim package manager, it's name have double meaning one is "vimapt" is the abbreviate of "VIM's Advantage Package Tools", two it works like `apt` tools on debian.

## Feature ##
1. text-based and  portable package ball format: "VPB", "VPB" is the abbreviation of "Vim Package Ball", it normally write as 'vpb'
2. web-based centerise repository
3. "one package, one config file", make vim package manageable, easy to share your config, easy to backup
4. full-stack tools from package-make-tools to repository-build-tools, anything have the tools no mater what do you want to do with vimapt


## Get vimapt
1. you can always download from github / bitbucket
2. I will buy the domain "vimapt.org" as vimapt's office website, so when I done, you can download from the office website
(if you want, you can donate for the vimapt, email me, thank you)

## Install
1. in your home dir's subdir `.vim`, you should make directory `vimapt` and `vimrc`
2. put the vimapt source to the `vimapt`
3. bakup you `.vimrc` file (you will use it latter)
4. clean you `.vimrc`, add code as below show  
`source ~/.vim/vimapt/vimapt.vim`

5. if your `.vimrc` contain your vim setting, move the common setting to the `.vim/vimrc/vim.vimrc`. if your vim is new, well, jump this step

## Usage

In vim console, type `VimApt install xxx` and press enter.

If everything is OK, you well soon get the `xxx` plugin

Notice: make sure you are online and the `xxx` plugin is in the repository

## Make a vpb package
Use the tools, it's interactive, just ask few simple questions. Then you will get the package template directory named `xxx-yyy`

Here `xxx` stand for your package name, `yyy` stand for your package version, it very like the debian package workflow

put you plugin file in the right directory (e.g. put your xxx.vim to "plugin" directory)

run the `put.py` tools in your `xxx-yyy` directory, you will get a file named `xxx-yyy.vpb` in your parent directory.
and the `xxx-yyy.vpb` file is your package

## Build the repository
general user should use office repository.

but if you want manage you own repository, it still have the tools for you.

## Why not vimapt
Vimapt not only allows to:

* keep track and configure your scripts right in .vimrc
* install configured scripts
* update configured scripts
* search by name all available vim scripts
* clean unused scripts up
* run above actions in a single keypress with interactive mode

But also vimapt:

* pack your package with you config file, so every one can quickly use it
* can bakup you vimrc use git or hg
* update but keep your vimrc
* every can have it's package, beacause you have your own config
* remove package
* package depends can check
* protect the vimscript author and mainiter's right

## Docs

see :h vimapt vimdoc for more details.

## People Using vimapt

see Examples

## FAQ

see wiki

## Contributors
see vundle contributors

Thank you!

## Inspiration and ideas from

* Debian's apt tools
* Homebrew on Mac OS X

## Also

Vimapt was developed and tested with Vim 7.3 on *nux

Vimapt try to be **the missing one**
