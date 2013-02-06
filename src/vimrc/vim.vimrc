let $VIMHOME = $HOME."/.vim"

"set vim not compatible to vi
set nocompatible

""set code line length limite
set colorcolumn=0

"set filetype on
filetype plugin indent on

""set syntax on
syntax on

"indent setting
set cindent

""show number line
set number

"set tab to space
set expandtab

""set coffeescript filetype
autocmd BufRead,BufNewFile *.coffee set ft=coffee 

"tab width .py file
autocmd FileType python setl tabstop=4
autocmd FileType python setl shiftwidth=4

""tab width .c file
autocmd FileType c setl tabstop=4
autocmd FileType c setl shiftwidth=4

"tab width .erl file
autocmd FileType erlang setl tabstop=4
autocmd FileType erlang setl shiftwidth=4

""tab width .html file
autocmd FileType html setl tabstop=2
autocmd FileType html setl shiftwidth=2

"tab width .js file
autocmd FileType javascript setl tabstop=2
autocmd FileType javascript setl shiftwidth=2

""tab width .css file
autocmd FileType css setl tabstop=2
autocmd FileType css setl shiftwidth=2

"tab width .php file
autocmd FileType php setl tabstop=4
autocmd FileType php setl shiftwidth=4
"
""tab width coffeescript file
autocmd FileType coffee setl tabstop=4
autocmd FileType coffee setl shiftwidth=4

"tab width vim file
autocmd FileType vim setl tabstop=4
autocmd FileType vim setl shiftwidth=4

""for filetype key map
"source ~/.vim/keymap/keymap.vim
"autocmd BufRead,BufNewFile :call Keymap()

"for ./.vim/templates file
"autocmd BufNewFile *.html 0r $VIMHOME/templates/html.tpl
"nnoremap <c-j> /<+.\{-1,}+><cr>c/+>/e<cr>
"inoremap <c-j> <ESC>/<+.\{-1,}+><cr>c/+>/e<cr>

""for youdao dict
"nmap <C-D> <ESC>:call Youdao()<cr>

"for ~/.vim/syntax/jquery.vim
"au BufRead,BufNewFile jquery.*.js set ft=javascript syntax=jquery
"
"for ~/.vim/plugin/jsbeautify.vim
"nmap <C-G> <ESC>:call g:Jsbeautify()<cr>


""""""""""""""""""""
"  common setting  " 
""""""""""""""""""""

"for NERDtree
"nnoremap <F7> <ESC>:NERDTreeToggle<CR>
"let NERDTreeWinPos = "right"
"
""for taglist
"nnoremap <F6> <ESC>:TlistToggle<CR>

" vimwiki
" let g:vimwiki_use_mouse = 1
" let g:vimwiki_list = [{'path': '/home/howl/Vimwiki/','path_html':
" '/home/howl/Vimwiki/html/','html_header':
" '/home/howl/Vimwiki/template/header.tpl'}] 
"
" """"""""""""""""""""""""""""""
" "  filetype depend setting   "
" """"""""""""""""""""""""""""""
"
"
" " for ~/.vim/php-doc.vim
" "source ~/.vim/php-doc.vim 
" "nnoremap <C-P> :call PhpDoc()<CR>
" "inoremap <C-P> <ESC>:set paste<CR>:exe PhpDoc()<CR>:set nopaste<CR>i
" "inoremap <C-S> <ESC>:set paste<CR>:exe PhpDocSingle()<CR>:set nopaste<CR>i
" "nnoremap <C-P> :call PhpDocSingle()<CR>
" "inoremap <C-r> :call PhpDocRange()<CR>
"
" "for ~/.vim/plugin/phpcs.vim
" ">> key map
" "nmap <F8> <ESC>:Phpcs<CR>
" "nmap <F9> <Esc>:cprev<CR>
" "nmap <F4> <ESC>:cnext<CR>
"
"
" " for less file
" autocmd! BufRead,BufNewFile *.less set filetype=less
"
"
" set tags=tags;
" " for xml/html formator use tidy
" vnoremap ,x :!tidy -q -i --show-errors 0<CR>
"
" "for ~/.vim/ftplugin/javascript/WriteJSDocComment.vim
" au FileType javascript nnoremap <buffer> <C-c>  :<C-u>call
" WriteJSDocComment()<CR>
"
" let g:pep8_map='<leader>8'
"
