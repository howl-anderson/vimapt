look at the example in the "../example/package/youdao-dict-2.0/" :
下面将要解释vpb包的结构， 下面是 `vimapt-demo-package` 的目录结构

    .:
    doc  plugin  vimapt  vimrc
    
    ./doc:
    youdao-doct.txt
    
    ./plugin:
    youdao-dict  youdao-dict.vim
    
    ./plugin/youdao-dict:
    youdao-dict.py
    
    ./vimapt:
    control  copyright
    
    ./vimapt/control:
    youdao-dict
    
    ./vimapt/copyright:
    youdao-dict
    
    ./vimrc:
    youdao-dict.vimrc

let me tell you:
下面来看看具体有那些文件：

## vimapt目录 ##
1. 首先是vimapt目录
这个目录的结构如下：
dir "vimapt" is the control of the package, as you see:

    ./vimapt:
    control  copyright
    
    ./vimapt/control:
    youdao-dict
    
    ./vimapt/copyright:
    youdao-dict

"vimapt" content "control" and "copyright" dir:
`control` 和 `copyright` 目录都包含并只包含一个和插件名字相同，不包括版本信息，后缀是.yaml的文件
every have a file named as the same as the package(not inclue the version)

### vimapt/control目录 ##
The contain of vimapt/control/youdao-dict:
以下就是 `control` 目录下面的 `vimapt-demo-package` 的文件内容：

    control: {
      depends: 'current no support, so~~',
      section: 'see section_list file',
      version: 'x.y.z'
    }

depends section means what you depend on, for example: "xxxx (z y.y.y)"
可能你已经通过后缀名猜到了，这个文件其实是yaml格式的文件。
`depends` 字段定义的是插件的依赖。格式有点类似与debian软件包里面的control文件的格式
如果是一个依赖那么格式就是 `xxx (z a.b.c)`
`xxxx` 表示的软件的名字
其中`z`代表的是比较符号，比如 `>`/`<`/`>=`/`<=`/`==`
`a.b.c` 代表的是软件的版本号
如果依赖是这种形式 `xxxx` 没有 `(z a.b.c)` 那么表示的是依赖不关心被依赖软件的版本，也就是这个软件安装就行，不管是什么版本
如果依赖形式是 `xxxx (a.b.c)` 表示软件的依赖只能是这个版本，不能是其他，也就是相当与 `xxxx (== a.b.c)`
xxx means package name, "y.y.y" means version, "z" means operate such as ">,<,>=,<=,=="
if only "xxxx" no "(z y.y.y)" means it don't care the version
if only "y.y.y" no "z" means just the "z" equal to "=="
muti-depends can split by ",", for example: "xxx, yyy"
see debian package control, you will know

`section` 字段表示的是这个包的类型，比如是配色啊，和文件类型相关的包还是通用包
section just as it says.
section list see section_list file

## viampt/copyright目录 ##
其内容如下：
The contain of vimapt/copyright/youdao-dict:

    copyright: {
      author: 'author name <author@mail>',
      license: 'your license <url of license full text>',
      maintiner: 'maintiner's name <maintiner@mail>'
    }

基本不需要解释，比较简单了

## vimrc目录 ##
这个目录存放的是插件的配置信息，里面可能有一个和插件名字相同但是后缀是.vimrc的文件，当然也可能没有（如果这个插件真的什么配置选项都没有的话）
原则上 我们鼓励 插件作者在这个文件里详细的把所有的配置选项全部写出来，并加上比较详细的注释,这样用户就能最快的了解和使用这个插件了

## plugin目录 ##
这个目录是用来存放插件的
我们希望的插件是这样的：
在这个目录下面有一个和插件名字一样后缀是.vim的插件文件，至于其他文件放在这个目录下和插件名字相同的子目录里

## doc目录 ##
这个目录存放文档
所以会有一个和插件名字相同但是后缀是.txt的文档文件