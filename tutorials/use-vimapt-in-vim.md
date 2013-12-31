# how to use the vimapt command in vim #
# 如何在vim中使用vimapt命令 #
you can use `:VimAptGet <command> <package>` in you vim
你可以在vim中使用形式是这样的 `:VimAptGet <command> <package>` 的命令
command is one of `install`/`remove`/`purge`, the same mean with apt-get in debian
你最常用的应该是 `install`/`remove`/`purge` 这几个命令，而这几个命令和debian的 `apt-get` 参数完全相同

## 安装软件 ##
例如你想安装的软件名叫做 `vimapt-demo-package` , 好吧， 确实是有这么一个软件，仅用于演示vimapt功能的插件
那么你可以在你的vim中输入 `VimAptGet install vimapt-demo-package` 然后回车，vimapt会自动到网络上下载这个插件，几秒种之后，它就会提示你插件安装成功

这里提示一个vimapt的小的人性化设计：你可以使用tab来人性化的补全。同样是安装上面的软件， 
你可以这样做： `VimA<tab> in<tab> vimapt-d<tab>` 如果一切正常你将得到相同的命令串 `VimAptGet install vimapt-demo-package`
是不是很方便呢

## 卸载软件 ##
你可以使用类似的命令完成卸载功能： `VimAptGet remove vimapt-demo-package` ，这个时候你也可以使用tab自动补全的。
有一个类似的命令叫做purge（用过debian系Linux的人都知道），区别就是remove删除插件，插件的配置将被保留。
而purge则是完全删除插件，配置也将被删除。

## purge ##
这个功能和remove类似，但是不保留插件的配置文件