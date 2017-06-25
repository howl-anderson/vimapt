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
* Don't support compile, so package's can't compile them-self during the install (e.g. you-complete-me need compile during the dependency).

# version 0.2
* add new package format `vap`, which is abbreviation from `VimApt's Package`. which will support binary file.
* this version will not cover the dependency solver or outer dependency checker or package compiler.
  
# version 0.3
* Add hook for install third-party dependency (mainly for pip package) and compiling package

# version 0.4
* Add dependency solver for package dependency, but don't support version selection (it can specific version, but repo mechanics don't support multi-version of a package :( )
* change the package name role to fit the dependency solver: `sat-solver` aka `simplesat`
* Disable install from file for simplify the implement
* Disable `purge` function for simplify the implement
* Add new feature called `upgrade` to upgrade specific package to newest version
* Add new feature called `upgrade-all` to upgrade all installed package to newest version
** it will cause `update` hard to implement when there is a incompatible config file already exits in system
** `purge` is hard to implement, when `remove` or `uninstall` case many package to uninstall, 
    but not all of them are best to keep config file. For future design, 
    it can be solved more or less by give package an option to indicate if there are configure file want be keep when it be uninstalled.
    
# version 0.5
* Make vim-apt can execute as command in the shell out of vim

# version 0.6
* Clean the code base, refactor the project for better readability.

# version 0.7
* Add new feature that allow user use vim-apt to install github project like `pathgo` / `bundle`.
  Function will implement thought wrapper `pathgo` / `bundle` package but provide a `vimapt` like user experience.
  Something like `VimApt bundle install repo/some-package`
  
# version 0.8
* Add plugin feature, that allow `vimapt` extend by plugin.
  ** package can expect to extend the vimapt's ablility, 
     like some package named `bundle` can allow user use `vimapt` to install package for `bundle`