# what is vimapt #

vim following numerous plug-in, but do not have a very good plug-in manager.
Vundle, pathogen, vim-addon-manager vim-plugin-manager can alleviate to some extent on the sharp contradictions, but these implementations relative to the python's "pip" ruby's "gem", node.js's "npm" it is a big change.
emacs 24 introduces a plug-in manager, the end of the era of emacs is no official plugin manager, I temporarily do not know specifically how to effect. But should also be good
vimapt is to better manage vim package (package here is similar to the concept and plug-ins, but the scope to cover more extensively) designed a set of system
From the packet format, remote warehouse architecture, packaging tools, command-line installation tool to vim internal command to install the script, all toolchain complete,
So named because of its implementation and the the architecture way and debian's apt tools similar vimapt

# Why vimapt #

1. The concept of the package
    vim is the concept of the package, the package can be either plain some plug-ins, it may be a plug-in configuration file, and may also be the vim of color documents, or even multiple plug-ins or other forms of mixture. package dependencies that may exist between (TODO: the current version vimapt for yet implemented this feature), such as a plug-in configuration file package, obviously it has to rely on this plugin provides package, or the configuration file does not make sense

2. The concept of the warehouse
    Provide similar linux distro warehouses similar standardized the remote packet warehouse, provide carefully check the package through a rigorous screening provides official assurance (TODO: due to staffing and funding issues, is preparing for the official repository for vim plugin)

3. Packages of standard format
    all vimapt's use of a self-developed simple and effective package format, we call it "vpb", meaning that the vim package ball a vpb package format is simple, and extremely easy to implement, very generic packet compression, production simple. The unzip fast. And provide official tools. Developed tools, very easy

4. Easy to distribute
    vpb format allows you downloaded to your bag (package can create their own production process is very easy, and provides the official tool), you can plug your carefully configured (obviously this is not outside the standard warehouse), labeled the vpb package, Share to your friends, or as a standard package redistributed

5. Offline support
    Offline you can not use the package manager? Not. Our package for offline use only one premise is that it's dependent on you own to meet, it's dependent or is already installed, or that you have downloaded, however, we may introduce a tool, to help you offline processing rely automatic according to the situation of download dependencies. TODO: Of course, the current version also does not implement this tool, so off you need to own query information dependence detection has not been achieved, and we do not deal with dependent offline package However, at least for now, need to rely on the package, very rare, so you can feel free to make use of the offline package

6. Socializing
    We will (TODO: this has not been achieved) launched a social users website for the interaction between users, exchange code to release private vimapt package of these private vimapt package will get the same treatment to the standard package

7. Configuration independence and separation
    We usually know if a plugin is really easy to use, not only with the plug-in itself, and plug configuration vimapt configuration package allows you to install the release configuration package, even the use of unknown origin or private configuration package, the maximum possible to ensure the freedom of all configurations are used alone

8. Version control
    The usual vim plugin manager is in the home under ". Vimrc" add configuration information, and a file manager, however, all the configuration, it is confusing and not good to do version control, we select the configuration file which is stored and stored separately, to guarantee the availability

9. Automatically updated (TODO: not implemented yet)
    the vim package system is to have the automatic update feature, you can get to know those packages are updated, you can choose to update or not to update your current configuration file, whether to keep updated

10. Environmental detection and conflicts
    of many vim plugin is needed vim to turn this option on or turn off that option, requires people to manually add configuration, and the needs of the various plug-ins may conflict, when people feel that it is a headache, vimapt will support environmental detection (TODO: not implemented yet). Automatically detect the environment and change the environment, as well as plug-in collision detection

11. Copyright protection package
    we will add copyright information to ensure that copyright, rather than a mess of code rights
