Vimapt
===

Vimapt is a vim package manager, "vimapt" is the abbreviate of "Vim's Advantage Package Tools".

## Feature ##
1. web-based repository
2. "one package, one config file", make vim package manageable, easy to share your config, easy to backup
3. full-stack tools from package-make-tools to repository-build-tools, anything have the tools no mater what do you want to do with vimapt


## Get vimapt
you can always download from github / bitbucket

## Install
1. in your home dir's subdir `.vim`, you should make directory `vimapt` and `vimrc`, if their already exists, backup them.
2. put the vimapt source to the `vimapt`, if you get the source from git repository, vimapt's source locate in `src` directory.
3. backup you `.vimrc` file (you will use it latter)
4. clean you `.vimrc`, add code as below show  

    `source ~/.vim/vimapt/vimapt.vim`

5. if your `.vimrc` contain your vim setting, move the common setting to the `.vim/vimrc/vim.vimrc`.
6. execute `pip install -r ~/.vim/vimapt/library/requirements.txt`
 and `pip3 install -r ~/.vim/vimapt/library/requirements.txt` to install all the dependencies that vimapt will need.

## Usage

### vimapt update

In vim console, type `:VimApt update` and press enter.

vimapt will connect to the official repository, and update package list.

### vimapt repolist

In vim console, type `:VimApt repolist` and press enter.

vimapt will show the list of all package that you can install.

### vimapt install

In vim console, type `:VimApt install xxx` and press enter.

If everything is OK, you well soon get the `xxx` or packages

Notice: make sure you are online and the `xxx` plugin is in the repository

### vimapt remove

In vim console, type `:VimApt remove xxx` and press enter.

Vimapt will remove the package `xxx` from your vim system.

### Tips

Vimapt support auto complete very well. you can auto complete command and packages.
Please notice that vim use TAB as auto complete key.

#### auto complete on commands

In vim console, type `:VimApt `, notice that last character is blank character. 
now you can press Tab / TAB to auto-complete now. Just like auto-complete function in shell. 

Partial command auto-complete is also supported. For example, you want type command `:VimApt install`,
 In vim console, type `:VimApt inst`, and now you can press Tab / TAB to auto-complete now,
 vimapt will auto complete the command line to `:VimApt install`.
 
#### auto complete on packages

Almost every command in vimapt support auto-complete.For example, if you want remove a package that named 'example-package',
When you type `:VimApt remove example-`, then press TAB / Tab, if there are only one package installed in vimapt which name begin with `example-`,
vimapt will auto-completed with `:VimApt remove example-package`,
if there multiply packages which name begin with `example-`, vimapt will auto-recycle during those package names.

## Tutorial

After you installed vimapt, here I will use install `nerd-tree` as an example, show the process of how usage vimapt.

1. Update your vimapt repository cache.
    
    Using `:Vimapt update`, vimapt will update package list to newest package list.
2. Install `nerd-tree`
    
    Using `:Vimapt install nerd-tree`, vimapt will install the package to your vim. Tips: you can use auto-complete function of vimapt.
3. Using `nerd-tree`
    
    Since, `nerd-tree` is installed, you can use it now, press `Ctrl-D` in normal mode, see if the `nerd-tree` works, press the key again will close the tree.
4. Remove `nerd-tree`
    
    If you don't want `nerd-tree` anymore, you can using `:Vimapt remove nerd-tree`, remove the package.
    After removing, you can press `Ctrl-D` to see if it still work. if everything is ok, the key should not work anymore.