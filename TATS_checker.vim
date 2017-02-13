if exists('g:loaded_syntastic_tsf_tats_checker')
    finish
endif
let g:loaded_syntastic_tsf_tats_checker = 1

if !exists('g:syntastic_tsf_tats_sort')
    let g:syntastic_tsf_tats_sort = 1
endif

let s:save_cpo = &cpo
set cpo&vim

function! SyntaxCheckers_tsf_tats_IsAvailable() dict
    return executable(self.getExec())
endfunction

function! SyntaxCheckers_tsf_tats_GetHighlightRegex(item)
    if match(a:item['text'], 'assigned but unused variable') > -1
        let term = split(a:item['text'], ' - ')[1]
        return '\V\\<'.term.'\\>'
    endif

    return ''
endfunction

function! SyntaxCheckers_tsf_tats_GetLocList() dict
    let makeprg = self.makeprgBuild({
                \ 'args': '-w -T1',
                \ 'args_after': '-c' })

    "this is a hack to filter out a repeated useless warning in rspec files
    "containing lines like
    "
    "  foo.should == 'bar'
    "
    "Which always generate the warning below. Note that ruby >= 1.9.3 includes
    "the word "possibly" in the warning
    let errorformat = '%-G%.%#warning: %\(possibly %\)%\?useless use of == in void context,'

    " filter out lines starting with ...
    " long lines are truncated and wrapped in ... %p then returns the wrong
    " column offset
    let errorformat .= '%-G%\%.%\%.%\%.%.%#,'

    let errorformat .=
                \ '%-GSyntax OK,' .
                \ '%E%f:%l: syntax error\, %m,' .
                \ '%Z%p^,' .
                \ '%W%f:%l: warning: %m,' .
                \ '%Z%p^,' .
                \ '%W%f:%l: %m,' .
                \ '%-C%.%#'

    let env = { 'RUBYOPT': '' }

    return SyntasticMake({ 'makeprg': makeprg, 'errorformat': errorformat, 'env': env })
endfunction

call g:SyntasticRegistry.CreateAndRegisterChecker({
            \ 'filetype': 'tsf',
            \ 'name': 'tats' })

let &cpo = s:save_cpo
unlet s:save_cpo

" vim: set sw=4 sts=4 et fdm=marker:
