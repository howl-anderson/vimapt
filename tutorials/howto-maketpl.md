# how to make a plugin tpl #
vimapt has a simple tools in vimapt-tool.deb,
this tools will support to make a tools autmate.

in the dir where you want make your vimapt package.
for example: '/path/to/your/plugin/dir'

    `cd /path/to/your/plugin/dir'

them use vimapt tools command:

    vimapt-maketpl

then, the vimapt-maketpl will ask your about info:

    Input you package name:

input your pakcage name, will only include a-z and '-', NOT include A-Z:

    vimapttest

then it will ask:

    Input you package version. Format like x.y.z:

input the version:

    1.0

tools will output:

    New packaging dir build in: " /tmp/vimapttest-1.0 "
    Every thing done! Tpl making is successed!
    Have fun!

now, in your '/path/to/your/plugin/dir', you will have a package dir named 'vimapttest-1.0'
then you can in it and make your package now
