function AptTest(args)
    echo "hello world" + args
endfunction
command! -nargs=* AptTest call AptTest(<q-args>)