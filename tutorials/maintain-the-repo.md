# 如何维护vimapt软件仓库 #

## 仓库结构 ##

the struct of the repo:

    index  pool

    ./index:
    package
    
    ./pool:
    aaaa_x.y.x.vpb

## index/package ##
文件结构如下：

autocomplpop: {path: pool/autocomplpop_2.14.1-1.vpb, version: 2.14.1-1}
ctrlp: {path: pool/ctrlp_1.79-1.vpb, version: 1.79-1}
matrix: {path: pool/matrix_1.10-1.vpb, version: 1.10-1}
nerd-commenter: {path: pool/nerd-commenter_2.3.0-1.vpb, version: 2.3.0-1}
nerd-tree: {path: pool/nerd-tree_4.2.0-1.vpb, version: 4.2.0-1}
pdv: {path: pool/pdv_1.1.4-1.vpb, version: 1.1.4-1}
phpcs: {path: pool/phpcs_1.1-1.vpb, version: 1.1-1}
powerline: {path: pool/powerline_1.0-1.vpb, version: 1.0-1}
pyflakes: {path: pool/pyflakes_3.0.1-1.vpb, version: 3.0.1-1}
pylint: {path: pool/pylint_0.5-1.vpb, version: 0.5-1}
supertab: {path: pool/supertab_2.0-1.vpb, version: 2.0-1}
surround: {path: pool/surround_2.0-1.vpb, version: 2.0-1}
tagbar: {path: pool/tagbar_2.4.1-1.vpb, version: 2.4.1-1}
taglist: {path: pool/taglist_4.5-1.vpb, version: 4.5-1}
tasklist: {path: pool/tasklist_1.0.1-1.vpb, version: 1.0.1-1}
vimapt: {path: pool/vimapt_1.0-1.vpb, version: 1.0-1}
vimwiki: {path: pool/vimwiki_2.0.1-1.vpb, version: 2.0.1-1}
zencoding: {path: pool/zencoding_0.80-1.vpb, version: 0.80-1}

从技术上说，这个package文件其实是yaml格式的，每一行一个软件，并包含软件的两个属性，一个是软件的位置，一个是软件的版本信息

## 相关工具 ##
当 `pool` 目录的软件发生变化时， 你在顶级目录运行 `vimapt-makeindex` 就可以自动重建 `/index/package`
when there is new vpb package add to the /pool in the top of the repo:

you just use `vimapt-makeindex`, file /index/package will rebuild
