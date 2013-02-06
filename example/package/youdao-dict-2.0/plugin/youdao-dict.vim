function! Youdao()
    let l:word = expand("<cword>")
    python import vim
    python sys.argv = ["",vim.eval("word")]
    pyfile $HOME/\.vim/plugin/youdao/youdao\.py
endfunction
