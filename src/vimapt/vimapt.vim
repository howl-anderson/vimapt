for vimrc_file in split(glob('~/.vim/vimrc/*.vimrc'), '\n')
    exe 'source' vimrc_file
endfor

let s:current_file=expand("<sfile>")

function VimAptGetInstall(vim_dir, package_name)
    echo s:current_file
    python import vim
    python import os
    python import sys
    python current_dir = os.path.dirname(vim.eval("s:current_file"))
    python python_script = os.path.join(current_dir, 'tools/get.py')
    python vim.command('let l:python_script = "' + python_script + '"')
    python sys.argv = ["", vim.eval("a:vim_dir"), vim.eval("a:package_name"), python_script]
    " echo l:python_script
    " pyfile $HOME/\.vim/plugin/youdao/youdao\.py
    execute "pyfile " . python_script
endfunction

function VimAptGet(command_arg, package_arg)
    let vapt_command = ''
    let command_list = ['install', 'remove']
    for commands in command_list
        if commands == a:command_arg
            let vapt_command = commands
        endif
    endfor
    echo vapt_command
    echo a:package_arg
    let runtimepath_stream = &runtimepath
    let runtimepath_list = split(runtimepath_stream, ',')
    let vim_dir_var = get(runtimepath_list, 0)
    let vim_dir_path = expand(vim_dir_var)
    echo vim_dir_path
    call VimAptGetInstall(vim_dir_path, a:package_arg)
endfunction


command! -nargs=* VimAptGet call VimAptGet(<f-args>)
