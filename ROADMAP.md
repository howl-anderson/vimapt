# version 0.1

* `install` / `remove` / `purge` package
* update package list by command `update`
* show repository packages list by command `repolist`
* show installed packages list by command `list`
* show list of packages that can purge (i.e. package that can be remove or purge) by command `purgelist`
* check dependency and conflict but not solve them automaticly

* packages have version infomation, but dependency solver can not use such infomation now.
* so VimApt can not upgrade package or check version now.
