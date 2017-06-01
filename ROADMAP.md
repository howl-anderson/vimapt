# version 0.1

* `install` / `remove` / `purge` package
* update package list by command `update`
* show repository packages list by command `repolist`
* show installed packages list by command `list`
* show list of packages that can purge (i.e. package that can be remove or purge) by command `purgelist`
* check dependency and conflict but not solve them automaticly

* packages have version infomation, but dependency solver can not use such infomation now.
* So VimApt can not upgrade package or check version now.

## disadvantage features found so far
### VPB's limitation
* VPB not support other-encoding than UTF8, so packages contain other encoding file are not supported (e.g. easymotion package)
* VPB not support binary file, so packages contain binary files (mainly image files) are not supported (e.g. vim-colors-solarized package) 
### Leak support for outer dependency check or auto-installer
* Don't support outer dependency check, so package's requirement may not met (e.g. jedi-vim package need jedi package which is an outer dependency).
* Don't support compile, so package's can't compile themself during the install (e.g. you-complete-me need compile during the dependency).

# version 0.2
* add new package format `vap', which is abbrevation from `VimApt's Package`. which will support binary file.
* this version will not cover the dependency solver or outer dependency checker or package compiler.
  
