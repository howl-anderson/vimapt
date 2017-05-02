Vimapt
===
**The missing package manager for Vim**


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

In vim console, type `VimApt install xxx` and press enter.

If everything is OK, you well soon get the `xxx` or packages

Notice: make sure you are online and the `xxx` plugin is in the repository

### vimapt remove

In vim console, type `VimApt remove xxx` and press enter.

Vimapt will remove the package `xxx` from your vim system.
