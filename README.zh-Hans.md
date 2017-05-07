Vimapt
===

Vimapt是一个Vim的软件包管理器／软件包管理软件, 其中"vimapt"是"Vim's Advantage Package Tools"的缩写.

## 特性 ##
1. 基于Web的软件包仓库
2. "一个软件包，一个配置文件", 使得vim的软件包更易于管理，更容易分享配置和更容易备份
3. 从软件打包到软件安装的全系列支持工具，让使用者非常容易使用vimapt


## 获取 vimapt
你可以从 github / [bitbucket](https://bitbucket.org/howl-anderson/vimapt) 上下载

## 安装

Vimpat提供了自动安装的脚本:

    `curl -sLf http://www.vimapt.org/install.sh | bash`
    
Windows用户请按照`手动安装`章节进行安装

## 手动安装
在你开始安装前,你需要确认你的vim支持python扩展,通过执行`vim --version`, 你需要观察输出的特性列表中是否有`+python`或者 `+python3`,
前者表示支持python2,后者表示支持python3. `-python`或者 `-python3` 分别表示对上述特性不支持. vimapt需要vim支持python,
同时你需要记住vim对python支持的版本情况,因为后续会用到这个信息.

1. 将vimapt的源代码放到`.vim`目录中. 如果你是从git仓库获取的代码, vimapt的源代码位于`src`目录.
2. 备份你的`.vimrc`文件 (稍后你将用到)
3. 清除`.vimrc`内容并添加如下代码: 

    `source ~/.vim/vimapt/vimapt.vim`

5. 如果你的备份的`.vimrc`包含有设置信息, 那么请把它移动到这个文件`.vim/vimrc/vim.vimrc`.
6. 执行 `pip install -r ~/.vim/vimapt/library/requirements.txt` 如果你的vim支持python2
或者 `pip3 install -r ~/.vim/vimapt/library/requirements.txt` 如果你的vim支持python3, 这些命令是为了安装vimapt所需的python依赖包.

## 使用

### vimapt update

在vim终端中, 输入 `:VimApt update` 并按回车.

vimapt将会连接官方仓库,并更新本地软件列表.

### vimapt repolist

在vim终端中, 输入 `:VimApt repolist` 并按回车.

vimapt将会显示一个你可以安装的软件的列表.

### vimapt install

在vim终端中, 输入 `:VimApt install xxx` 并按回车.

如果一切正常,你将很快会被提示 `xxx` 软件包安装成功.

注意: 这个过程需要你的计算机联网并且 `xxx` 包在仓库中

### vimapt remove

在vim终端中, 输入 `:VimApt remove xxx` 并按回车.

vimapt 将会把 `xxx` 从你的系统中移除.

### 小贴士

Vimapt 对自动补全的支持非常好. 你可以补全命令和软件包的名字.
请注意vim使用 TAB 作为自动补全的触发键.

#### 自动补全命令

在vim终端中, 输入 `:VimApt `, 注意最后一个输入字符是空格. 
现在你按 Tab / TAB 去自动补全. 就像shell中的自动补全一样. 你会轮流看到可能的命令.

部分命令补全也是支持的. 比如, 你想输入命令 `:VimApt install`,
在vim终端中, 输入 `:VimApt inst`, 现在你按 Tab / TAB 去自动补全.
 vimapt将会自动帮你补全命令至 `:VimApt install`.
 
#### 自动补全软件包名

几乎所有的vimapt命令都支持补全.比如, 你想移除名为 'example-package'的包,
当你输入 `:VimApt remove example-`, 然后按 TAB / Tab, 如果vimapt中安装的包只有一个包名字开头为 `example-`,
vimapt会自动补全命令 `:VimApt remove example-package`,
如果有多个包开头是 `example-`, vimapt 会自动循环显示这些名字.

## 教程

在安装vimapt后, 这里将使用安装 `nerd-tree` 作为案例, 来显示使用vimapt的一般流程.

1. 更新你的vimapt仓库.
    
    使用 `:Vimapt update`, vimapt 将会自动更新至最新的软件列表.
2. 安装 `nerd-tree`
    
    使用  `:Vimapt install nerd-tree`, vimapt将会自动帮你安装该软件. 提示:你可以使用自动补全来加速你的输入.
3. 使用 `nerd-tree`
    
    现在 `nerd-tree` 已经安装完成, 你可以开始使用了, 通过在普通模式中按键 `Ctrl-D`, 你可以看见`nerd-tree`的文件树出现在左侧, 再次按`Ctrl-D`则消失.
4. 移除 `nerd-tree`
    
    当你不再需要 `nerd-tree` 了, 你可以使用 `:Vimapt remove nerd-tree` 来移除这个包.
    移除后,你可以使用按键 `Ctrl-D` 来确定它是否还能工作. 如果一切正常,这个按键应该不会起作用了.