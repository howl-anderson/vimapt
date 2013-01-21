# Vimapt #
vimapt is a vim package manager, it works like debian's apt tools,
# feature #
1. text-base & portable package ball format:"VPB", "VPB" is the abbreviation of "Vim Package Ball", it nomorally write as 'vpb'
2. big and standard web-based repository
3. "one package one config file", make vim package managable, easy to share your config, easy to backup
4. full-stack tools from package-make-tools to repository-build-tools, anything have the tools no mater what do you want to do with vimapt
# Quick start #
## get vimapt ##
1. you can always download it from github/bitbucket
2. i will buy the domain "vimapt.org" for the vimapt's office website, so when i done, you can download from the office website
(as a poor graduate student, zero-income, if you want, you can donate for the vimapt, email me, thank you)
## Install ##
1. in your home dir's subdir '.vim',
you should make dir "vimapt" and "vimrc"
2. put the vimapt source to the "vimapt"
3. bakup you ".vimrc" file(you will use it latter)
clean you ".vimrc", add code as below show

    source ~/.vim/vimapt/vimapt.vim

4. if your ".vimrc" contain your vim setting, mv the common setting to the ".vim/vimrc/vim.vimrc".
if your vim is new, well, jump this
## Usage ##
in your vim console, you type "VimAptGet install xxx" and press enter.
if everything is ok, you well soon get the xxx plugin
Notice: make sure you are online and the xxx plugin is in the repository
# make a vpb package #
use the tools, it's activate, just ask it's simple question. and you will get the package tpl dir
go to your "xxx-yyy" dir,
here xxx stand for your package name, yyy stand for your package version, it very like the debian package workflow
put you plugin file in the right dir, ps: put your xxx.vim to "plugin" dir and so on
run the "put.py" tools in your "xxx-yyy" dir, you will get a file named "xxx-yyy.vpb" in your parent dir.
the .vpb is your package
# build the repository #
you can rsync the repo from the vimapt office website.
but if you want manage you own repo, it still have the tools
# Why not vimapt

vimapt not only allows to:

    keep track and configure your scripts right in .vimrc
    install configured scripts
    update configured scripts
    search by name all available vim scripts
    clean unused scripts up
    run above actions in a single keypress with interactive mode

But also Vimapt:

    pack your package with you config file, so every one can quickly use it
    can bakup you vimrc use git or hg
    update but keep your vimrc
    every can have it's package, beacause you have your own config
    remove package
    package depends can check
    protect the vimscript author and mainiter's right

# Docs #

see :h vimapt vimdoc for more details.

# People Using Vimapt #

see Examples

# FAQ #

see wiki

# Contributors #

see vundle contributors

Thank you!

# Inspiration and ideas from #

    vundle
    pathogen
    bundler
    Scott Bronson

# Also #

    Vimapt was developed and tested with Vim 7.3 on *nux
    Vimapt tries to be the top package manageer for vim
