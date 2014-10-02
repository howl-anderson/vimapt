for vimrc_file in split(glob('~/.vim/vimrc/*.vimrc'), '\n')
    execute 'source' vimrc_file
endfor

let s:current_file=expand("<sfile>")
let s:command_list = ['install', 'githubinstall', 'remove', 'purge', 'update', 'repolist', 'list', 'purgelist']
let runtimepath_stream = &runtimepath
let runtimepath_list = split(runtimepath_stream, ',')
let vim_dir_var = get(runtimepath_list, 0)
let s:vim_dir_path = expand(vim_dir_var)
let s:package_list = []
let s:package_remove_list = []
let s:package_purge_list = []

function VimAptInstall(vim_dir, package_name)
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/install.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("a:vim_dir"), vim.eval("a:package_name")]
    execute "pyfile " . python_script
    "let shell = "python " . l:python_script . " " . a:vim_dir . " " . a:package_name
    "echo shell
    "let output = system(shell)
    "echo output
endfunction

function VimAptGithubInstall(vim_dir, user_package)
    let user_package_list = split(a:user_package, "/")
    let user_name = user_package_list[0]
    let package_name = user_package_list[1]
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/github_install.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("a:vim_dir"), vim.eval("l:user_name"), vim.eval("l:package_name")]
    execute "pyfile " . python_script
    "let shell = "python " . l:python_script . " " . a:vim_dir . " " . a:package_name
    "echo shell
    "let output = system(shell)
    "echo output
endfunction

function VimAptGetRemove(vim_dir, package_name)
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/remove.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("a:vim_dir"), vim.eval("a:package_name"), python_script]
    execute "pyfile " . python_script
endfunction

function VimAptGetPurge(vim_dir, package_name)
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/purge.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("a:vim_dir"), vim.eval("a:package_name"), python_script]
    execute "pyfile " . python_script
endfunction

function VimAptGetUpdate()
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/update.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("s:vim_dir_path")]
    execute "pyfile " . python_script
endfunction

function VimApt(command_arg, ...)
    let vapt_command = ''
    for commands in s:command_list
        if commands == a:command_arg
            let vapt_command = commands
        endif
    endfor
    if a:0 == 1
        let package_arg = a:1
    endif
    if vapt_command == 'install'
        call VimAptInstall(s:vim_dir_path, package_arg)
    elseif vapt_command == 'githubinstall'
        call VimAptGithubInstall(s:vim_dir_path, package_arg)
    elseif vapt_command == 'remove'
        call VimAptRemove(s:vim_dir_path, package_arg)
    elseif vapt_command == 'purge'
        call VimAptPurge(s:vim_dir_path, package_arg)
    elseif vapt_command == 'update'
        call VimAptUpdate()
    elseif vapt_command == 'list'
        call VimAptList()
    elseif vapt_command == 'repolist'
        call VimAptRepolist()
    elseif vapt_command == 'purgelist'
        call VimAptPurgelist()
    else
        echo "Error: unknow command"
    endif
endfunction

function VimAptPackageList()
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/pkg_list.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("s:vim_dir_path")]
    execute "pyfile " . python_script
endfunction

function VimAptPackageRemoveList()
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/pkg_remove_list.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("s:vim_dir_path")]
    execute "pyfile " . python_script
endfunction

function VimAptPackagePurgeList()
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python bin_dir = os.path.join(current_dir, 'bin')
    python sys.path.append(bin_dir)
    python python_script = os.path.join(current_dir, 'bin/pkg_purge_list.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("s:vim_dir_path")]
    execute "pyfile " . python_script
endfunction

function VimAptList()
    call VimAptPackageRemoveList()
    echo join(s:package_remove_list, "\n")
endfunction

function VimAptRepolist()
    call VimAptPackageList()
    echo join(s:package_list, "\n")
endfunction

function VimAptPurgelist()
    call VimAptPackagePurgeList()
    echo join(s:package_purge_list, "\n")
endfunction

function VimAptComplete(ArgLead, CmdLine, CursorPos)
    let token = split(a:CmdLine, '\_s\+')
    if len(token) == 1
    " there no arg
        return join(s:command_list, "\n")
    elseif len(token) == 2
    " there have one arg
        let complete_package_flag = 0
        let current_command = get(token, 1)
        for commands in s:command_list
            if commands == current_command 
                if current_command != "update" && current_command != "repolist" && current_command != "list" && current_command != "purgelist"
                    let complete_package_flag = 1 
                endif
            endif
        endfor
        if strpart(a:CmdLine, strlen(a:CmdLine)-1, 1) != ' '
            return join(s:command_list, "\n")
        elseif complete_package_flag
            if current_command == "install"
                call VimAptPackageList()
                return join(s:package_list, "\n")
            elseif current_command == "remove"
                call VimAptPackageRemoveList()
                return join(s:package_remove_list, "\n")
            elseif current_command == "purge"
                call VimAptPackagePurgeList()
                return join(s:package_purge_list, "\n")
            endif
        else
            return ""
        endif
    else
        call VimAptPackageList()
        return join(s:package_list, "\n")
    endif
endfunction

command! -nargs=* -complete=custom,VimAptComplete VimApt call VimApt(<f-args>)
