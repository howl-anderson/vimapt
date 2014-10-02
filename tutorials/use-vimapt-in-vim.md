How use the vimapt command in vim
===

## Command in vimapt

You can use `:VimApt <command> <package>` in you vim terminal

`<command>` usually be one of `install`/`remove`/`purge`, the same mean with apt-get in debian or ubuntu

## VimApt install
Assume you want to install a package named `vimapt-demo-package`, well, it's indeed exits. but only used for demo function.

To finish this work, you need input `:VimApt install vimapt-demo-package` and press enter, vimapt will download and install it for you all automatic. 

Here comes a tips:

Vimapt comes with autocomplete function.

* You can complete the command (`install`/`remove`/`purge`)
* You can complete the package name also.

Vim use `<tab>` as autocomplete key.

You can use `VimA<tab> in<tab> vimapt-d<tab>` to get `VimAptGet install vimapt-demo-package`


## VimApt remove
You can use `VimApt remove vimapt-demo-package` to remove `vimapt-demo-package` package

`remove` will remove package but keep the configure file in case of you reinstall the package some day

## VimApt purge ##
similar with `remove`, but don't keep package configure file