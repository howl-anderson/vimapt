" detect if python feature is supported
if has('python')
        let s:python = 'python'
        let s:pyfile = 'pyfile'
elseif has('python3')
        let s:python = 'python3'
        let s:pyfile = 'py3file'
else
        echo "VimApt require vim support python or python3, which not, VimApt aborted!"
        finish 
endif

" python abstruct function
function VimAptPythonCall(clause)
    execute s:python . ' ' . a:clause 
endfunction

" pycall abstruct function
function VimAptPyfileCall(python_file)
    execute s:pyfile . ' ' . a:python_file 
endfunction

" VimApt abstruct command
function VimAptCommand(command_name, ...)
    let s:command_args = a:000

    call VimAptPythonCall('import vim')
    call VimAptPythonCall('import os')
    call VimAptPythonCall('import sys')

    call VimAptPythonCall('current_dir = os.path.dirname(vim.eval("s:current_file"))')
    call VimAptPythonCall('library_dir = os.path.join(current_dir, "library")')
    call VimAptPythonCall('sys.path.append(library_dir)')
    call VimAptPythonCall('third_party_dir = os.path.join(current_dir, "third_party")')
    call VimAptPythonCall('sys.path.append(third_party_dir)')

    call VimAptPythonCall('python_script = os.path.join(current_dir, "bin/' . a:command_name . '.py")')
    call VimAptPythonCall('vim.command("let s:python_script = \"" + python_script + "\"")')
    
    call VimAptPythonCall('sys.argv = ["", vim.eval("s:vim_dir_path")]')
    call VimAptPythonCall('sys.argv.extend(vim.eval("s:command_args"))')

    call VimAptPyfileCall(s:python_script)
endfunction


for vimrc_file in split(glob('~/.vim/vimrc/*.vimrc'), '\n')
    execute 'source' vimrc_file
endfor



for vimrc_file in split(glob('~/.vim/vimrc/*.vimrc'), '\n')
    execute 'source' vimrc_file
endfor

let s:current_file = expand("<sfile>")
let s:command_list = ['install', 'remove', 'purge', 'update', 'repolist', 'list', 'purgelist']
let runtimepath_stream = &runtimepath
let runtimepath_list = split(runtimepath_stream, ',')
let vim_dir_var = get(runtimepath_list, 0)
let s:vim_dir_path = expand(vim_dir_var)
let s:package_list = []
let s:package_remove_list = []
let s:package_purge_list = []

function VimAptInstall(vim_dir, package_name)
    call VimAptCommand('install', a:package_name)
endfunction

function VimAptRemove(vim_dir, package_name)
    call VimAptCommand('remove', a:package_name)
endfunction

function VimAptPurge(vim_dir, package_name)
    call VimAptCommand('purge', a:package_name)
endfunction

function VimAptUpdate()
    call VimAptCommand('update')
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
    elseif vapt_command == 'remove'
        call VimAptRemove(s:vim_dir_path, package_arg)
    elseif vapt_command == 'purge'
        call VimAptPurge(s:vim_dir_path, package_arg)
    elseif vapt_command == 'update'
        call VimAptUpdate()
    elseif vapt_command == 'list'
        call VimAptList()
    elseif vapt_command == 'repolist'
        call VimAptRepoList()
    elseif vapt_command == 'purgelist'
        call VimAptPurgeList()
    else
        echo "Error: unknow command"
    endif
endfunction

function VimAptPackageList()
    call VimAptCommand('pkg_list')
endfunction

function VimAptPackageRemoveList()
    call VimAptCommand('pkg_remove_list')
endfunction

function VimAptPackagePurgeList()
    call VimAptCommand('pkg_purge_list')
endfunction

function VimAptList()
    call VimAptPackageRemoveList()
    echo join(s:package_remove_list, "\n")
endfunction

function VimAptRepoList()
    call VimAptPackageList()
    echo join(s:package_list, "\n")
endfunction

function VimAptPurgeList()
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
