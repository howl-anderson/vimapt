#!/bin/bash

# A guarding function to avoid executing an incompletely downloaded script
guard () {
    # Reset
    Color_off='\033[0m'       # Text Reset

    # Regular Colors
    Red='\033[0;31m'          # Red
    Blue='\033[0;34m'         # Blue

    # Constant
    VIMAPT_GIT_REPO_URL='https://bitbucket.org/howl-anderson/vimapt.git'

    # vim detect
    if ! hash "vim" &>/dev/null; then
        echo -e "${Red}vim is not installed${Color_off}"
        exit -2
    fi

    # python supporting detect
    HAS_PYTHON=$(vim --version | grep -c '+python')
    HAS_PYTHON3=$(vim --version | grep -c '+python3')

    if ! ([ ${HAS_PYTHON} ] || [ ${HAS_PYTHON3} ]); then
        echo -e "${Red}vim not support python binding${Color_off}"
        exit -1
    fi

    check_python_pip () {
        PIP=0
        if [ ${HAS_PYTHON3} ]; then
            if hash "pip3" &>/dev/null; then
                PIP='pip3'
            fi
        else
            if hash "pip" &>/dev/null; then
                PIP='pip'
            fi
        fi
        if ! [ ${PIP} ]; then
            if ${HAS_PYTHON3}; then
                echo -e "${Red}need 'pip3' (command not found)${Color_off}"
            else
                echo -e "${Red}need 'pip' (command not found)${Color_off}"
            fi
            exit 1
        fi
    }

    check_system_dependency () {
        if ! hash "$1" &>/dev/null; then
            echo -e "${Red}need '$1' (command not found)${Color_off}"
            exit 1
        fi
    }

    fetch_repo () {
        # make sure directories exists
        mkdir -p "$HOME/.VimApt"
        mkdir -p "$HOME/.VimApt/vimapt/"

        if [[ -d "$HOME/.VimAptRepo" ]]; then
            # Update VimApt
            git -C "$HOME/.VimAptRepo/.git" pull

            # update file from .VimAptRepo to .VimApt
            cp -R "$HOME/.VimAptRepo/src/vimapt/"{bin,library,tool} "$HOME/.VimApt/vimapt/"
            cp "$HOME/.VimAptRepo/src/vimapt/vimapt.vim" "$HOME/.VimApt/vimapt/"

            echo -e "${Blue}Successfully update VimApt${Color_off}"
        else
            git clone ${VIMAPT_GIT_REPO_URL} "$HOME/.VimAptRepo"

            # copy file from .VimAptRepo to .VimApt
            cp -R "$HOME/.VimAptRepo/src/"{vimapt,vimrc} "$HOME/.VimApt/"

            echo -e "${Blue}Successfully clone VimApt${Color_off}"
        fi
    }

    install_vim () {
        # backup .vimrc file
        if [[ -f "$HOME/.vimrc" ]]; then
            mv "$HOME/.vimrc" "$HOME/.vimrc_back"
            echo -e "${Blue}BackUp $HOME/.vimrc${Color_off}"
        fi

        # copy .vimrc
        cp "$HOME/.VimAptRepo/src/vimapt/entry_point.vimrc" "$HOME/.vimrc"

        # backup .vim directory
        if [[ -d "$HOME/.vim" ]]; then
            if [[ "$(readlink $HOME/.vim)" =~ \.VimApt$ ]]; then
                echo -e "${Blue}Installed VimApt for vim${Color_off}"
            else
                mv "$HOME/.vim" "$HOME/.vim_back"
                echo -e "${Blue}BackUp $HOME/.vim${Color_off}"

                ln -s "$HOME/.VimApt" "$HOME/.vim"
                echo -e "${Blue}Installed VimApt for vim${Color_off}"
            fi
        else
            ln -s "$HOME/.VimApt" "$HOME/.vim"
            echo -e "${Blue}Installed VimApt for vim${Color_off}"
        fi
    }

    install_pip_dependency () {
        if [ ${HAS_PYTHON3} ]; then
            pip install -r "$HOME/.vim/vimapt/library/requirements.txt"
        else
            pip3 install -r "$HOME/.vim/vimapt/library/requirements.txt"
        fi
    }

#    install_neovim () {
#        if [[ -d "$HOME/.config/nvim" ]]; then
#            if [[ "$(readlink $HOME/.config/nvim)" =~ \.SpaceVim$ ]]; then
#                echo -e "${Blue}Installed SpaceVim for neovim${Color_off}"
#            else
#                mv "$HOME/.config/nvim" "$HOME/.config/nvim_back"
#                echo -e "${Blue}BackUp $HOME/.config/nvim${Color_off}"
#                ln -s "$HOME/.SpaceVim" "$HOME/.config/nvim"
#                echo -e "${Blue}Installed SpaceVim for neovim${Color_off}"
#            fi
#        else
#            ln -s "$HOME/.SpaceVim" "$HOME/.config/nvim"
#            echo -e "${Blue}Installed SpaceVim for neovim${Color_off}"
#        fi
#    }

#    uninstall_vim () {
#        if [[ -d "$HOME/.vim" ]]; then
#            if [[ "$(readlink $HOME/.vim)" =~ \.SpaceVim$ ]]; then
#                rm "$HOME/.vim"
#                echo -e "${Blue}Uninstall VimApt for vim${Color_off}"
#                if [[ -d "$HOME/.vim_back" ]]; then
#                    mv "$HOME/.vim_back" "$HOME/.vim"
#                    echo -e "${Blue}Recover $HOME/.vim${Color_off}"
#                fi
#            fi
#        fi
#        if [[ -f "$HOME/.vimrc_back" ]]; then
#            mv "$HOME/.vimrc_back" "$HOME/.vimrc"
#            echo -e "${Blue}Recover $HOME/.vimrc${Color_off}"
#        fi
#    }

#    uninstall_neovim () {
#        if [[ -d "$HOME/.config/nvim" ]]; then
#            if [[ "$(readlink $HOME/.config/nvim)" =~ \.SpaceVim$ ]]; then
#                rm "$HOME/.config/nvim"
#                echo -e "${Blue}Uninstall SpaceVim for neovim${Color_off}"
#                if [[ -d "$HOME/.config/nvim_back" ]]; then
#                    mv "$HOME/.config/nvim_back" "$HOME/.config/nvim"
#                    echo -e "${Blue}Recover $HOME/.config/nvim${Color_off}"
#                fi
#            fi
#        fi
#    }

    usage () {
        echo "VimApt install script : V 0.1.0"
        echo "    Install VimApt for vim"
        echo "        curl -sLf https://vimapt.org/install.sh | bash"
    }


    if [ $# -gt 0 ]
    then
        case $1 in
#            uninstall)
#                uninstall_vim
#                uninstall_neovim
#                exit 0
#                ;;
            install)
                check_system_dependency 'git'
                fetch_repo
                if [ $# -eq 2 ]
                then
                    case $2 in
#                        neovim)
#                            install_neovim
#                            exit 0
#                            ;;
                        vim)
                            install_vim
                            exit 0
                    esac
                fi
                install_vim
#                install_neovim
                exit 0
                ;;
            -h)
                usage
                exit 0
        esac
    fi

    check_python_pip
    check_system_dependency 'git'

    fetch_repo
    install_vim
    install_pip_dependency
#    install_neovim

    echo -e "${Blue}VimApt have been installed! Have fun!${Color_off}"

    # end of guard
}

# download finished fine
guard $@
