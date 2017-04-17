How to make a plugin template
===

vimapt has a simple tools in vimapt-tool.deb,
this tools will support to make a tools autmatic.

In the directory where you want make your vimapt package.
for example: '/path/to/your/plugin/dir'

    cd /path/to/your/plugin

then use vimapt tools command:

    vimapt-maketpl

vimapt-maketpl will ask your about info:

    Input you package name:

Input your package name, will only include a-z and '-', NOT include A-Z:

    vimapttest

after that, it will ask:

    Input you package version. Format like x.y.z:

Input the version:

    1.0

tools will output:

    New packaging directory build in: " /tmp/vimapttest-1.0 "
    Jobs done! Template making is succeed!
    Have fun!

Now, in your `/path/to/your/plugin`, you will have a package directory named `vimapttest-1.0`

You can go to it and make your package now
