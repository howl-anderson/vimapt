look at the example in the "../example/package/youdao-dict-2.0/" :

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

1. vimapt
dir "vimapt" is the control of the package, as you see:

    ./vimapt:
    control  copyright
    
    ./vimapt/control:
    youdao-dict
    
    ./vimapt/copyright:
    youdao-dict

"vimapt" content "control" and "copyright" dir:
every have a file named as the same as the package(not inclue the version)

The contain of vimapt/control/youdao-dict:

    control: {
      depends: 'current no support, so~~',
      section: 'see section_list file',
      version: 'x.y.z'
    }

depends section means what you depend on, for example: "xxxx (z y.y.y)"
xxx means package name, "y.y.y" means version, "z" means operate such as ">,<,>=,<=,=="
if only "xxxx" no "(z y.y.y)" means it don't care the version
if only "y.y.y" no "z" means just the "z" equal to "=="
muti-depends can split by ",", for example: "xxx, yyy"
see debian package control, you will know

section just as it says.
section list see section_list file

The contain of vimapt/copyright/youdao-dict:

    copyright: {
      author: 'author name <author@mail>',
      license: 'your license',
      maintiner: 'maintiner's name <maintiner@mail>'
    }

