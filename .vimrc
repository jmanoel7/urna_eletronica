" ============================================
" My vimrc <joaomanoel7@gmail.com>
" ============================================

" ============================================
" Note to myself:
" DO NOT USE <C-z> FOR SAVING WHEN PRESENTING!
" ============================================

"set nonu
"set lbr
"set tw=500
"set nowrap "no line wrapping
"set fo-=t  "no line wrapping text when typing
"set so=7            " Set 7 lines to the curors - when moving vertical..
"set ruler           "Always show current position
"set hid             "Change buffer - without saving
"set nohidden
"set nomodeline
"set whichwrap+=<,>,h,l
"set nolazyredraw "Don't redraw while executing macros

" Tell vim to remember certain things when we exit
"  '100 :  marks will be remembered for up to 10 previously edited files
"  "100 :  will save up to 100 lines for each register
"  :100 :  up to 20 lines of command-line history will be remembered
"  %    :  saves and restores the buffer list
"  n... :  where to save the viminfo files
set viminfo='100,\"100,:100,%,n~/.viminfo

function! ResCur()
  if line("'\"") <= line("$")
    normal! g`"
    return 1
  endif
endfunction

augroup resCur
  autocmd!
  autocmd BufWinEnter * call ResCur()
augroup END

" initial config for easytags
let g:easytags_include_members=1

" Encoding and Font
" set gfn=Dejavu\ Sans\ Mono
set gfn=JetBrainsMonoMedium\ Nerd\ Font\ Mono\ Medium\ 12
set encoding=utf8
try
    lang pt_BR
catch
endtry

" vim autocomplete
set omnifunc=syntaxcomplete#Complete

" Vim Gui
if has("gui_running")
  set guioptions-=T
  set lines=40
  set co=120
endif

" Spell Checker
set nospell spelllang=pt_br

" Automatic reloading of ~/.vimrc
autocmd! bufwritepost ~/.vimrc source %

" Better copy & paste
" When you want to paste large blocks of code into vim, press F2 before you
" paste. At the bottom you should see ``-- INSERT (paste) --``.
set pastetoggle=<F2>
set clipboard=unnamed

" Mouse and backspace
set backspace=eol,start,indent
set mouse=a  " on OSX press ALT and click
set bs=2     " make backspace behave like normal again

" confirm before quit
set confirm

" vim auto write
set autowrite

" Rebind <Leader> key
" I like to have it here becuase it is easier to reach than the default and
" it is next to ``m`` and ``n`` which I use for navigating between tabs.
let mapleader=","
let g:mapleader=","

" Write Command
nmap <leader>w :w!<cr>

" Edit ~/.vimrc config file
map <leader>e :e! ~/.vimrc<cr>

" GnuPG Encrypt
vnoremap <Leader><C-e> :!gpg2 --batch --no-tty --yes --default-key 607A5E65 --default-recipient-self --armor --encrypt 2>/dev/null<CR>

" GnuPG Decrypt
vnoremap <Leader><C-d> :!gpg2 --batch --no-tty --yes --default-key 607A5E65 --default-recipient-self --armor --decrypt 2>/dev/null<CR>

" Security Enviremont
nnoremap <Leader><C-s> :set viminfo=<CR>:set noswapfile noundofile nobackup<CR>:set bin<CR>:let ch_save = &ch\|set ch=2<CR>

" Files .cpt
augroup CPT
    au!
    au BufReadPre *.cpt set bin
    au BufReadPre *.cpt set viminfo=
    au BufReadPre *.cpt set noswapfile
    au BufReadPost *.cpt let $vimpass = inputsecret("Password: ")
    au BufReadPost *.cpt silent '[,']!ccrypt -cb -E vimpass
    au BufReadPost *.cpt set nobin
    au BufWritePre *.cpt set bin
    au BufWritePre *.cpt '[,']!ccrypt -e -E vimpass
    au BufWritePost *.cpt u
    au BufWritePost *.cpt set nobin
augroup END

" set up zope page templates as the zpt filetype
autocmd BufNewFile,BufRead *.pt,*.cpt,*.zpt set filetype=zpt syntax=xml

" CTRL-X and SHIFT-Del are Cut
vnoremap <C-x> "+x
vnoremap <S-Del> "+x

" CTRL-C and CTRL-Insert are Copy
vnoremap <C-c> "+y
vnoremap <C-Insert> "+y

" CTRL-V and SHIFT-Insert are Paste
inoremap <C-v> <ESC>:set paste<CR>"+gp<ESC>:set nopaste<CR>i<RIGHT>
nnoremap <C-v> :set paste<CR>"+gp<ESC>:set nopaste<CR>
vnoremap <C-v> "+gP
inoremap <S-Insert> <ESC>:set paste<CR>"+gp<ESC>:set nopaste<CR>i<RIGHT>
nnoremap <S-Insert> :set paste<CR>"+gp<ESC>:set nopaste<CR>
vnoremap <S-Insert> "+gP

" Remove whitespaces from end of line
nnoremap <leader><F4> 1GVG:s/\s*$//<CR>:<ESC>

" Case Words
vnoremap <Leader><C-1> :s/\(.\)/\L\1\E/g<CR>1GVG:s/\(\<.\)/\U\1\E/g<CR>1GVG:s/\(\<.\{1,3}\>\)/\L\1\E/g<CR>1GVG:s/ \(i\|ii\|iii\|iv\|v\|vi\|vii\|viii\|ix\|x\)$/\U\1\E/<CR>

" Setup Python Files
autocmd FileType python set sw=4
autocmd FileType python set ts=4
autocmd FileType python set sts=4

" Setup Django Files
let g:last_relative_dir = ''
nnoremap \1 :call RelatedFile ("models.py")<cr>
nnoremap \2 :call RelatedFile ("views.py")<cr>
nnoremap \3 :call RelatedFile ("urls.py")<cr>
nnoremap \4 :call RelatedFile ("admin.py")<cr>
nnoremap \5 :call RelatedFile ("tests.py")<cr>
nnoremap \6 :call RelatedFile ( "templates/" )<cr>
nnoremap \7 :call RelatedFile ( "templatetags/" )<cr>
nnoremap \8 :call RelatedFile ( "management/" )<cr>
nnoremap \0 :e settings.py<cr>
nnoremap \9 :e urls.py<cr>

fun! RelatedFile(file)
    #This is to check that the directory looks djangoish
    if filereadable(expand("%:h"). '/models.py') || isdirectory(expand("%:h") . "/templatetags/")
        exec "edit %:h/" . a:file
        let g:last_relative_dir = expand("%:h") . '/'
        return ''
    endif
    if g:last_relative_dir != ''
        exec "edit " . g:last_relative_dir . a:file
        return ''
    endif
    echo "Cant determine where relative file is : " . a:file
    return ''
endfun

fun SetAppDir()
    if filereadable(expand("%:h"). '/models.py') || isdirectory(expand("%:h") . "/templatetags/")
        let g:last_relative_dir = expand("%:h") . '/'
        return ''
    endif
endfun
autocmd BufEnter *.py call SetAppDir()

" pretty-printing JSON, PYTHON IMPORT AND PYTHON STYLE GOOGLE
nnoremap <leader><F5> :up<CR>:execute '%!json' \| w<CR>
nnoremap <leader><F6> :up<CR>:execute '%!python -m json.tool' \| w<CR>
nnoremap <leader><F7> :up<CR>:execute '%!isort ' . expand('%')<CR>
nnoremap <leader><F8> :up<CR>:execute '%!yapf ' . expand('%') \| w<CR>

" Bind nohl
" Removes highlight of your last search
" ``<C>`` stands for ``CTRL`` and therefore ``<C-n>`` stands for ``CTRL+n``
noremap <C-n> :nohl<CR>
vnoremap <C-n> :nohl<CR>
inoremap <C-n> :nohl<CR>

" Quicksave command
noremap <C-Z> :update<CR>
vnoremap <C-Z> <C-C>:update<CR>
inoremap <C-Z> <C-O>:update<CR>

" Quick quit command
noremap <Leader>q :q<CR>     " Quit current window
noremap <Leader>Q :qa!<CR>   " Quit all windows

" bind Ctrl+<movement> keys to move around the windows, instead of using Ctrl+w + <movement>
" Every unnecessary keystroke that can be saved is good for your health :)
map <c-j> <c-w>j
map <c-k> <c-w>k
map <c-l> <c-w>l
map <c-h> <c-w>h

" easier moving between tabs
map <Leader>n <esc>:tabprevious<CR>
map <Leader>m <esc>:tabnext<CR>

" map sort function to a key
vnoremap <Leader><F3> :sort<CR>

" easier moving of code blocks
" Try to go into visual mode (v), thenselect several lines of code here and
" then press ``>`` several times.
vnoremap < <gv  " better indentation
vnoremap > >gv  " better indentation

" Show whitespace
" MUST be inserted BEFORE the colorscheme command
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
au InsertLeave * match ExtraWhitespace /\s\+$/

" Errors and Visualbell
set noerrorbells
set novisualbell
"set t_vb=
"set tm=500

" Enable syntax highlighting
" You need to reload this file for the change to apply
set nocompatible
set magic "Set magic on, for regular expressions
set showmatch "Show matching bracets when text indicator is over them

" Showing line numbers and length
set number  " show line numbers
set tw=149  " width of document (used by gd)
set nowrap  " don't automatically wrap on load
set fo-=t   " don't automatically wrap text when typing
set colorcolumn=150
highlight ColorColumn ctermbg=233

" easier formatting of paragraphs
vmap Q gq
nmap Q gqap

set history=1000
set undolevels=1000

" Real programmers don't use TABs but spaces
set textwidth=120
set tabstop=4
set softtabstop=4
set shiftwidth=4
set shiftround
set expandtab
set smarttab
set smartindent
set autoindent

" Make search case insensitive
set hlsearch
set incsearch
set ignorecase
set smartcase

" Disable stupid backup and swap files - they trigger too many events
" for file system watchers
set nobackup
set nowritebackup
set noswapfile

" Better navigating through omnicomplete option list
" See http://stackoverflow.com/questions/2170023/how-to-map-keys-for-popup-menu-in-vim
"set completeopt=longest,menuone
"function! OmniPopup(action)
"    if pumvisible()
"        if a:action == 'j'
"            return "\<C-N>"
"        elseif a:action == 'k'
"            return "\<C-P>"
"        endif
"    endif
"    return a:action
"endfunction
"inoremap <silent><C-j> <C-R>=OmniPopup('j')<CR>
"inoremap <silent><C-k> <C-R>=OmniPopup('k')<CR>

" Set CTRL+SPACE to Omni Code Completion
"if !has("gui_running")
"    inoremap <C-@> <C-x><C-o>
"else
"    inoremap <C-Space> <C-x><C-o>
"endif

" Set CTRL+i to User Defined Completion
"inoremap <C-i> <C-x><C-u>

" Setup Pathogen to manage your plugins
" mkdir -p ~/.vim/autoload ~/.vim/bundle
" curl -so ~/.vim/autoload/pathogen.vim https://raw.githubusercontent.com/tpope/vim-pathogen/master/autoload/pathogen.vim
" Now you can install any plugin into a .vim/bundle/plugin-name/ folder
filetype off
execute pathogen#infect()
execute pathogen#helptags()
filetype plugin indent on
syntax on


" ============================================================================
" Plugins Setup
" ============================================================================


" ============================================================================= 
" Color scheme
" cd ~/.vim/bundle
" git clone https://github.com/jmanoel7/vim-colors.git
" ============================================================================= 

set background=dark
set t_Co=256
colorscheme wombat256mod
"colorscheme wombat_mbe


" ============================================================================= 
" Settings for vim-powerline
" cd ~/.vim/bundle
" git clone https://github.com/Lokaltog/vim-powerline.git
" ============================================================================= 

set laststatus=2


" ============================================================================= 
" Settings for ctrlp
" cd ~/.vim/bundle
" git clone https://github.com/kien/ctrlp.vim.git
" ============================================================================= 

let g:ctrlp_max_height = 30
set wildignore+=*.swp
set wildignore+=*.bak
set wildignore+=*.class
set wildignore+=*.pyc
set wildignore+=*_build/*
set wildignore+=*/coverage/*


" ============================================================================= 
" Python folding and more
" cd ~/.vim/bundle
" git clone https://github.com/jmanoel7/vim-utils.git
" ============================================================================= 

set nofoldenable


" ============================================================================= 
" Vim Games
" cd ~/.vim/bundle
" git clone https://github.com/jmanoel7/vim-games.git
" ============================================================================= 


" ============================================================================= 
" GnuPG
" cd ~/.vim/bundle
" git clone https://github.com/jamessan/vim-gnupg.git
" ============================================================================= 

let g:GPGPreferArmor=1
let g:GPGPreferSign=1
let g:GPGUseAgent=1
let g:GPGExecutable="gpg"


" ============================================================================= 
" scriptease.vim: A Vim plugin for Vim plugins
" cd ~/.vim/bundle
" git clone https://github.com/tpope/vim-scriptease.git
" ============================================================================= 


" ============================================================================= 
" VIM Table Mode
" cd ~/.vim/bundle
" git clone https://github.com/dhruvasagar/vim-table-mode.git
" ============================================================================= 


" ============================================================================= 
" VIM Latex-Suite
" cd ~/.vim/bundle
" git clone https://github.com/vim-latex/vim-latex.git
" ============================================================================= 

set shellslash
set grepprg=grep\ -nH\ $*
let g:tex_flavor='latex'


" ============================================================================= 
" Emmet (ex-Zen Coding) - vim plugins for HTML and CSS hi-speed coding
" cd ~/.vim/bundle
" git clone http://github.com/mattn/emmet-vim/
" ============================================================================= 

"let g:user_emmet_mode='n'    "only enable normal mode functions.
"let g:user_emmet_mode='inv'  "enable all functions, which is equal to
let g:user_emmet_mode='a'    "enable all function in all mode.
let g:user_emmet_install_global = 0
autocmd FileType html,css,django EmmetInstall
let g:user_emmet_leader_key='<C-Z>'


" ============================================================================= 
" L9 : Vim-script library
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/L9.git vim-l9
" ============================================================================= 


" ============================================================================= 
" FuzzyFinder
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/FuzzyFinder vim-fuzzyfinder
" ============================================================================= 

map <leader>f :FufFileWithCurrentBufferDir<CR>
map <leader>m :FufFileWithFullCwd<CR>
map <leader>b :FufBuffer<CR>


" ============================================================================= 
" MRU
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/mru.vim.git
" ============================================================================= 

map <leader><space> :MRU<CR>
let g:MRU_Max_Entries = 1000
let g:MRU_Window_Height = 15
let g:MRU_Max_Menu_Entries = 20
let g:MRU_Max_Submenu_Entries = 15


" ============================================================================= 
" TagBar
" cd ~/.vim/bundle
" git clone https://github.com/majutsushi/tagbar
" ============================================================================= 

let g:tagbar_usearrows=1
let g:tagbar_width=30
let g:tagbar_singleclick=1
" Use <F9> to open Tagbar in Right side
nmap <F9> :TagbarToggle<CR>


" ============================================================================= 
" Vim-EasyTags
" cd ~/.vim/bundle
" git clone https://github.com/xolox/vim-easytags.git
" ============================================================================= 

let g:easytags_cmd = '/usr/bin/ctags'
let g:easytags_file = '~/.vim/tags'
let g:easytags_by_filetype = '~/.vim/tags_dir'
let g:easytags_events = ['BufWritePost']
let g:easytags_python_enabled = 1
"let g:easytags_python_script = ???
set tags=./tags;,~/.vim/tags
let g:easytags_dynamic_files = 1


" ============================================================================= 
" Vim-Misc
" cd ~/.vim/bundle
" git clone https://github.com/xolox/vim-misc.git
" ============================================================================= 


" ============================================================================= 
" Syntastic
" cd ~/.vim/bundle
" git clone https://github.com/scrooloose/syntastic.git
" ============================================================================= 

"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"let g:syntastic_always_populate_loc_list = 1
"let g:syntastic_auto_loc_list = 1
"let g:syntastic_check_on_open = 1
"let g:syntastic_check_on_wq = 0
nmap <F8> :SyntasticCheck<CR>
nnoremap <silent> <C-d> :lclose<CR>:bdelete<CR>
cabbrev <silent> bd <C-r>=(getcmdtype()==#':' && getcmdpos()==1 ? 'lclose\|bdelete' : 'bd')<CR>
"let g:syntastic_aggregate_errors = 1
"let g:syntastic_always_populate_loc_list = 1
let g:syntastic_enable_perl_checker = 1
let g:syntastic_perl_checkers = ['perlcritic', 'podchecker', 'perl']
"let g:syntastic_python_checkers = ['flake8', 'pep8', 'pyflakes', 'python3']
let g:syntastic_python_checkers = ['pyflakes', 'python3.11']
let g:syntastic_python_python_exec = '/usr/bin/python3.11'
let g:syntastic_zpt_checkers = ['zptlint']
let g:syntastic_html_checkers = ['tidy', 'w3']
let g:syntastic_html_tidy_exec = 'tidy5'
"let g:syntastic_html_w3_api (string; default: 'http://validator.w3.org/check')
"let g:syntastic_html_w3_exec (string; default: 'curl')
" list of errors to ignore
"let g:syntastic_html_tidy_ignore_errors (list; default: [])
"let g:syntastic_html_tidy_ignore_errors = [ '<input> proprietary attribute "role"' ]
" list of additional blocklevel tags, to be added to --new-blocklevel-tags
"let g:syntastic_html_tidy_blocklevel_tags (list; default: [])
" list of additional inline tags, to be added to --new-inline-tags
"let g:syntastic_html_tidy_inline_tags (list; default: [])
" list of additional empty tags, to be added to --new-empty-tags
"let g:syntastic_html_tidy_empty_tags (list; default: [])
let g:syntastic_xhtml_checkers = ['tidy', 'jshint']
let g:syntastic_xml_checkers = ['xmllint']
let g:syntastic_javascript_checkers = ['jslint', 'jshint']
let g:syntastic_javascript_jslint_args = "--white --nomen --regexp --browser --devel --windows --sloppy --vars"
let g:syntastic_json_checkers = ['jsonlint']
let g:syntastic_css_checkers = ['csslint', 'prettycss']
let g:syntastic_php_checkers = ['phplint', 'php']
let g:syntastic_java_checkers = ['javac']
let g:syntastic_nasm_checkers = ['nasm']
let g:syntastic_sh_checkers = ['shellcheck']
let g:syntastic_zsh_checkers = ['zsh']
let g:syntastic_tex_checkers = ['lacheck', 'chktex']
let g:syntastic_text_checkers = ['language_check']
let g:syntastic_text_language_check_args = '--language=pt-BR'


" ============================================================================= 
" Ultisnips
" cd ~/.vim/bundle
" git clone https://github.com/SirVer/ultisnips.git
" ============================================================================= 

" The default value for g:UltiSnipsJumpBackwardTrigger interferes with the
" built-in complete function: |i_CTRL-X_CTRL-K|. A workaround is to add the
" following to your vimrc file or switching to a plugin like Supertab or
" YouCompleteMe.
"inoremap <c-x><c-k> <c-x><c-k>

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
" let g:UltiSnipsListSnippets="<C-x><C-i>"
" let g:UltiSnipsExpandTrigger="<C-e>"
" let g:UltiSnipsJumpForwardTrigger="<c-n>"
" let g:UltiSnipsJumpBackwardTrigger="<c-p>"
let g:UltiSnipsExpandTrigger       = "<C-j>"
let g:UltiSnipsJumpForwardTrigger  = "<C-j>"
let g:UltiSnipsJumpBackwardTrigger = "<C-p>"
let g:UltiSnipsListSnippets        = "<C-k>" "List possible snippets based on current file

" If you want :UltiSnipsEdit to split your window.
"let g:UltiSnipsEditSplit="vertical"

" To use python version 2.x
"let g:UltiSnipsUsePythonVersion = 2

" To use python version 3.x
let g:UltiSnipsUsePythonVersion = 3


" ============================================================================= 
" vim-snippets
" cd ~/.vim/bundle
" git clone https://github.com/honza/vim-snippets.git
" ============================================================================= 

map <Leader><C-b> Oimport ipdb; ipdb.set_trace() # BREAKPOINT<C-c>


" ============================================================================= 
" SimpylFold
" cd ~/.vim/bundle
" git clone https://github.com/tmhedberg/SimpylFold.git
" ============================================================================= 

let g:SimpylFold_docstring_preview = 1
"let g:SimpylFold_fold_docstring = 0
autocmd BufWinEnter *.py setlocal foldexpr=SimpylFold(v:lnum) foldmethod=expr
autocmd BufWinLeave *.py setlocal foldexpr< foldmethod<


" ==============================================================================
" vim-fugitive
" cd ~/.vim/bundle
" git clone https://github.com/tpope/vim-fugitive.git
" ==============================================================================

let g:statusline="%{fugitive#statusline()}"


" ==============================================================================
" vim-repeat
" cd ~/.vim/bundle
" git clone git://github.com/tpope/vim-repeat.git
" ==============================================================================


" ==============================================================================
" vim-surround
" cd ~/.vim/bundle
" git clone git://github.com/tpope/vim-surround.git
" ==============================================================================

let b:surround_{char2nr("v")} = "{{ \r }}"
let b:surround_{char2nr("{")} = "{{ \r }}"
let b:surround_{char2nr("%")} = "{% \r %}"
let b:surround_{char2nr("b")} = "{% block \1block name: \1 %}\r{% endblock \1\1 %}"
let b:surround_{char2nr("i")} = "{% if \1condition: \1 %}\r{% endif %}"
let b:surround_{char2nr("w")} = "{% with \1with: \1 %}\r{% endwith %}"
let b:surround_{char2nr("f")} = "{% for \1for loop: \1 %}\r{% endfor %}"
let b:surround_{char2nr("c")} = "{% comment %}\r{% endcomment %}"


" ==============================================================================
" delimitMate
" cd ~/.vim/bundle
" git clone https://github.com/Raimondi/delimitMate.git
" ==============================================================================

autocmd FileType python let b:delimitMate_autoclose = 1
autocmd FileType javascript let b:delimitMate_autoclose = 1
autocmd FileType css let b:delimitMate_autoclose = 1
autocmd FileType xml let b:delimitMate_autoclose = 1
autocmd FileType html let b:delimitMate_autoclose = 1


" ==============================================================================
" TaskList.vim
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/TaskList.vim.git
" ==============================================================================

map <F7> :TaskList<CR>


" ==============================================================================
" vim-misc-xolox
" cd ~/.vim/bundle
" git clone https://github.com/xolox/vim-misc.git vim-misc-xolox
" ==============================================================================


" ==============================================================================
" Easy note taking in Vim
" cd ~/.vim/bundle
" git clone https://github.com/xolox/vim-notes.git
" ==============================================================================

let g:notes_directories = ['~/OneDrive/Notas']
autocmd BufNewFile,BufRead */.git/COMMIT_EDITMSG setlocal filetype=notes


" ==============================================================================
" Vim Outliner of Markups
" cd ~/.vim/bundle
" git clone https://github.com/vim-voom/vim-voom.github.com.git
" ==============================================================================


" ==============================================================================
" Univeral Text Linking - Execute URLs, footnotes, open emails, organize ideas
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/utl.vim.git
" ==============================================================================


" ==============================================================================
" NERD Commenter
" cd ~/.vim/bundle
" git clone https://github.com/preservim/nerdcommenter.git
" ==============================================================================

" Create default mappings
let g:NERDCreateDefaultMappings = 1

" Add spaces after comment delimiters by default
let g:NERDSpaceDelims = 1

" Use compact syntax for prettified multi-line comments
let g:NERDCompactSexyComs = 1

" Align line-wise comment delimiters flush left instead of following code indentation
let g:NERDDefaultAlign = 'left'

" Set a language to use its alternate delimiters by default
let g:NERDAltDelims_java = 1

" Add your own custom formats or override the defaults
let g:NERDCustomDelimiters = { 'c': { 'left': '/**','right': '*/' } }

" Allow commenting and inverting empty lines (useful when commenting a region)
let g:NERDCommentEmptyLines = 1

" Enable trimming of trailing whitespace when uncommenting
let g:NERDTrimTrailingWhitespace = 1

" Enable NERDCommenterToggle to check all selected lines is commented or not 
let g:NERDToggleCheckAllLines = 1


" ==============================================================================
" NerdTree
" cd ~/.vim/bundle
" git clone https://github.com/scrooloose/nerdtree.git
" how to using NERDTree :
" http://ykyuen.wordpress.com/2011/04/04/nerdtree-the-file-explorer-in-vivim/
" ==============================================================================

" Enable this for make NERDTree load every opening files
"autocmd VimEnter * NERDTree " Make Always Load NERDTree every opening files
"autocmd VimEnter * wincmd p " Automatically go to buffer every time open files

" FIXING NERDTree, automatically close if there no file edited
"https://github.com/scrooloose/nerdtree/issues/21
autocmd WinEnter * call s:CloseIfOnlyNerdTreeLeft()

" Use <CTRL> + <F9> for opening File Explorer
map <F3> :NERDTreeToggle<CR>
let g:NERDTreeShowBookmarks=1
let g:NERDTreeMouseMode=3
let g:NERDTreeWinSize=30

" Close all open buffers on entering a window if the only
" buffer that's left is the NERDTree buffer
function! s:CloseIfOnlyNerdTreeLeft()
  if exists("t:NERDTreeBufName")
    if bufwinnr(t:NERDTreeBufName) != -1
      if winnr("$") == 1
        q
      endif
    endif
  endif
endfunction

" Open Window Explorer NerdTree & Tagbar using (left-right sidebar) using <Leader><F9>
function! ToggleNERDTreeAndTagbar()
    let w:jumpbacktohere = 1

" Detect which plugins are open
    if exists('t:NERDTreeBufName')
        let nerdtree_open = bufwinnr(t:NERDTreeBufName) != -1
    else
        let nerdtree_open = 0
    endif
    let tagbar_open = bufwinnr('__Tagbar__') != -1

" Perform the appropriate action
    if nerdtree_open && tagbar_open
        NERDTreeClose
        TagbarClose
    elseif nerdtree_open
        TagbarOpen
    elseif tagbar_open
        NERDTreeToggle
    else
        NERDTreeToggle
        TagbarOpen
    endif

" Jump back to the original window
    for window in range(1, winnr('$'))
        execute window . 'wincmd w'
        if exists('w:jumpbacktohere')
            unlet w:jumpbacktohere
            break
        endif
    endfor
endfunction

" now you can open NERDTree and Tagbar using <leader><F9>
" http://stackoverflow.com/questions/6624043/how-to-open-or-close-nerdtree-and-tagbar-with-leader
nmap <leader><F9> :call ToggleNERDTreeAndTagbar()<CR>


" ==============================================================================
" Settings for vim-project
" cd ~/.vim/bundle
" git clone https://github.com/amiorin/vim-project.git
" ==============================================================================

let g:project_enable_welcome = 0
let g:project_use_nerdtree = 1

set rtp+=~/.vim/bundle/vim-project/
call project#rc("~/git/")

Project "esab/urna_eletronica"
Project "esab/Audio-Player"


" ==============================================================================
" Extended session management for Vim (:mksession on steroids)
" cd ~/.vim/bundle
" git clone https://github.com/xolox/vim-session.git
" ==============================================================================

"let g:loaded_session=1
let g:session_autoload='no'
let g:session_autosave='no'


" ==============================================================================
" Vim Markdown
" cd ~/.vim/bundle
" git clone https://github.com/plasticboy/vim-markdown.git
" ==============================================================================

let g:vim_markdown_folding_disabled = 0
let g:vim_markdown_folding_style_pythonic = 1
let g:vim_markdown_folding_level = 1
let g:vim_markdown_no_default_key_mappings = 0
let g:vim_markdown_toc_autofit = 1
let g:vim_markdown_emphasis_multiline = 0
set conceallevel=2
let g:vim_markdown_fenced_languages = ['python=py']
let g:vim_markdown_fenced_languages = ['bash=sh']
let g:vim_markdown_follow_anchor = 1
" let g:vim_markdown_anchorexpr = "'<<'.v:anchor.'>>'"
let g:vim_markdown_math = 1
let g:vim_markdown_frontmatter = 1
let g:vim_markdown_toml_frontmatter = 1
let g:vim_markdown_json_frontmatter = 1
let g:vim_markdown_strikethrough = 1
let g:vim_markdown_new_list_item_indent = 4
let g:vim_markdown_no_extensions_in_markdown = 1
let g:vim_markdown_autowrite = 1
" let g:vim_markdown_auto_extension_ext = 'txt'
" let g:vim_markdown_auto_insert_bullets = 0
" let g:vim_markdown_new_list_item_indent = 0
let g:vim_markdown_edit_url_in = 'tab'


" ==============================================================================
" Better JSON for VIM
" cd ~/.vim/bundle
" git clone https://github.com/elzr/vim-json.git
" ==============================================================================

let g:vim_json_syntax_conceal = 1
":setlocal foldmethod=syntax


" ==============================================================================
" gVim menu for txt2tags
" cd ~/.vim/bundle
" git clone https://github.com/vim-scripts/txt2tags-menu.git
" ==============================================================================


" ==============================================================================
" YouCompleteMe
" cd ~/.vim/bundle
" git clone https://github.com/ycm-core/YouCompleteMe.git
" cd YouCompleteMe
" git submodule update --init --recursive
" sudo apt install build-essential cmake vim-gtk3 python3.11-dev python3.11-full
" sudo apt install mono-complete golang nodejs openjdk-17-jdk openjdk-17-jre npm
" python3.11 install.py --all
" ==============================================================================

imap <silent> <C-l> <Plug>(YCMToggleSignatureHelp)
let g:ycm_enable_semantic_highlighting=1


" ==============================================================================
" REMOVED PLUGINS
" ==============================================================================


" ==============================================================================
" Conque-Shell: Run interactive commands inside a Vim buffer
" cd ~/.vim/bundle
" CURL -O https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/conque/conque_2.3.tar.gz
" tar -xzf conque_2.3.tar.gz && mv -f conque_2.3 Conque-Shell && rm -f conque_2.3.tar.gz
" ==============================================================================


" ==============================================================================
" vim-shell
" cd ~/.vim/bundle
" GIT clone https://github.com/xolox/vim-shell.git
" ==============================================================================

" let g:shell_mappings_enabled = 0
" inoremap <Leader><F11> <C-o>:Fullscreen<CR>
" nnoremap <Leader><F11> :Fullscreen<CR>
" inoremap <Leader><F12> <C-o>:Open<CR>
" nnoremap <Leader><F12> :Open<CR>


" ==============================================================================
" Updated javacomplete plugin for vim.
" cd ~/.vim/bundle
" GIT clone https://github.com/artur-shaik/vim-javacomplete2.git
" ==============================================================================

" autocmd FileType java setlocal omnifunc=javacomplete#Complete

" To enable smart (trying to guess import option) inserting class imports
" with CTRL + F4, add:
" nmap <C-F4> <Plug>(JavaComplete-Imports-AddSmart)
" imap <C-F4> <Plug>(JavaComplete-Imports-AddSmart)

" To enable usual (will ask for import option) inserting class imports
" with CTRL + F5, add:
" nmap <C-F5> <Plug>(JavaComplete-Imports-Add)
" imap <C-F5> <Plug>(JavaComplete-Imports-Add)

" To add all missing imports with CTRL + F6:
" nmap <C-F6> <Plug>(JavaComplete-Imports-AddMissing)
" imap <C-F6> <Plug>(JavaComplete-Imports-AddMissing)

" To remove all missing imports with CTRL + F7:
" nmap <C-F7> <Plug>(JavaComplete-Imports-RemoveUnused)
" imap <C-F7> <Plug>(JavaComplete-Imports-RemoveUnused)

" F10/C-F10 compile/run default file.
" F12/C-F12 compile/run alternate file.
" map <F10> :set makeprg=javac\ %<CR>:make<CR>
" map <C-F10> :!echo %\|awk -F. '{print $1}'\|xargs java<CR>
" map <F12> :set makeprg=javac\ #<CR>:make<CR>
" map <C-F12> :!echo #\|awk -F. '{print $1}'\|xargs java<CR>
" map! <F10> <Esc>:set makeprg=javac\ %<CR>:make<CR>
" map! <C-F10> <Esc>:!echo %\|awk -F. '{print $1}'\|xargs java<CR>
" map! <F12> <Esc>set makeprg=javac\ #<CR>:make<CR>
" map! <C-F12> <Esc>!echo #\|awk -F. '{print $1}'\|xargs java<CR>

" Tip: load a file into the default buffer, and its driver
" into the alternate buffer, then use F10/F12 to build/run.
" Note: # (alternate filename) isn't set until you :next to it!
" Tip2: You can make then run without hitting ENTER to continue. F10-F12

" With these you can cl/cn/cp (quickfix commands) to browse the errors
" after you compile it with :make
" set makeprg=javac\ %
" set errorformat=%A:%f:%l:\ %m,%-Z%p^,%-C%.%#

" Javac defaults to printing output on stderr and no options can convert,
" so we have to set 'shellpipe'
" set shellpipe=2>
" 2> works on Win NT and UNIX

" If two files are loaded, switch to the alternate file, then back.
" That sets # (the alternate file).
" if argc() == 2
"   n
"   e #
" endif


" ==============================================================================
" The Maven plugin for VIM
" cd ~/.vim/bundle
" GIT clone https://github.com/mikelue/vim-maven-plugin.git
" ==============================================================================


" ==============================================================================
" OmniCppComplete => C/C++ omni-completion with ctags database
" cd ~/.vim/bundle
" GIT clone https://github.com/vim-scripts/OmniCppComplete.git
" ==============================================================================


" ==============================================================================
" SQLComplete.vim => SQLComplete is a SQL code completion system using the omnifunc framework
" cd ~/.vim/bundle
" GIT clone https://github.com/vim-scripts/SQLComplete.vim.git
" ==============================================================================


" ==============================================================================
" clang_complete => Vim plugin that use clang for completing C/C++ code.
" cd ~/.vim/bundle
" GIT clone https://github.com/Rip-Rip/clang_complete.git
" ==============================================================================

" path to directory where library can be found
" let g:clang_library_path='/usr/lib'
" or path directly to the library file
" let g:clang_library_path='/usr/lib/llvm-3.5/lib/libclang.so.1'
" let g:clang_library_path='/usr/lib/llvm-10/lib/libclang.so.1'
" path do clang.exe
" let g:clang_exec = '/usr/bin/clang'
" options for clang
" let g:clang_user_options = '2> /dev/null || exit 0'


" ============================================================================= 
" jedi-vim
" cd ~/.vim/bundle
" GIT clone --recursive https://github.com/davidhalter/jedi-vim.git
" pip2 install --force-reinstall -U jedi
" ============================================================================= 

" let g:jedi#use_tabs_not_buffers = 1
" let g:jedi#use_splits_not_buffers = "bottom"
" let g:jedi#show_call_signatures = "1"
" let g:jedi#goto_command = "<leader>d"
" let g:jedi#goto_assignments_command = "<leader>g"
" let g:jedi#goto_definitions_command = ""
" let g:jedi#documentation_command = "K"
" let g:jedi#usages_command = "<leader>n"
" let g:jedi#completions_command = "<C-Space>"
" let g:jedi#rename_command = "<leader>r"
" let g:jedi#popup_on_dot = 1
" let g:jedi#popup_select_first = 1
" let g:jedi#completions_enabled = 1


" ==============================================================================
" Supertab => Perform all your vim insert mode completions with Tab
" cd ~/.vim/bundle
" GIT clone https://github.com/ervandew/supertab.git
" ==============================================================================

" let g:SuperTabDefaultCompletionType = "context"
" let g:SuperTabContextDefaultCompletionType = "<c-n>"


" ==============================================================================
" Python-mode, a Python IDE for Vim
" cd ~/.vim/bundle
" GIT clone --recurse-submodules https://github.com/python-mode/python-mode.git
" ==============================================================================


" ============================================================================= 
" vim-pyunit
" cd ~/.vim/bundle
" GIT CLONE https://github.com/nvie/vim-pyunit.git
" pip3 install --force-reinstall -U nose vim_bridge mock
" cd ~/src
" GIT CLONE https://github.com/mcrute/nose-machineout.git
" cd nose-machineout
" sudo python3 ./setup.py install
" ============================================================================= 

" let g:no_pyunit_maps = 1
" noremap <Leader><C-p> :call PyUnitRunTests()<CR>
" noremap! <Leader><C-p> <Esc>:call PyUnitRunTests()<CR>


" ==============================================================================
" Vim plugin for working with python virtualenvs
" cd ~/.vim/bundle
" GIT clone https://github.com/jmcantrell/vim-virtualenv.git
" ==============================================================================

"let g:virtualenv_directory = '~/.local/venvs'


" ==============================================================================
" vim-django run commands, create apps, and beyond
" cd ~/.vim/bundle
" GIT clone https://github.com/cwood/vim-django.git
" ==============================================================================

"let g:django_projects = '~/Dropbox/Public/Projetos/Python/Django/' "Sets all projects under project
"let g:django_activate_virtualenv = 1 "Try to activate the associated virtualenv
"let g:django_activate_nerdtree = 1 "Try to open nerdtree at the project root.
"let g:last_relative_dir = '' "Initial Directory for Django App
"
"fun! SetAppDir()
"    "This is to check that the directory looks djangoish
"    if filereadable(expand("%:h") . '/models.py') || isdirectory(expand("%:h") . "/templatetags/")
"        let g:last_relative_dir = expand("%:h") . '/'
"        return ''
"    endif
"endfun

"fun! RelatedFile(file)
"    "This is to check that the directory looks djangoish
"    "if filereadable(expand("%:h") . '/models.py') || isdirectory(expand("%:h") . "/templatetags/")
"    "    exec "edit %:h/" . a:file
"    "    let g:last_relative_dir = expand("%:h") . '/'
"    "    return ''
"    "endif
"    if g:last_relative_dir != ''
"        exec "edit " . g:last_relative_dir . a:file
"        return ''
"    endif
"    echo "Cant determine where relative file is : " . a:file
"    return ''
"endfun

"autocmd BufEnter *.py call SetAppDir()
"nnoremap <leader>1 :call RelatedFile ("models.py")<cr>
"nnoremap <leader>2 :call RelatedFile ("views.py")<cr>
"nnoremap <leader>3 :call RelatedFile ("urls.py")<cr>
"nnoremap <leader>4 :call RelatedFile ("admin.py")<cr>
"nnoremap <leader>5 :call RelatedFile ("tests.py")<cr>
"nnoremap <leader>6 :call RelatedFile ("templates/")<cr>
"nnoremap <leader>7 :call RelatedFile ("templatetags/")<cr>
"nnoremap <leader>8 :call RelatedFile ("management/")<cr>
"nnoremap <leader>0 :e settings.py<cr>
"nnoremap <leader>9 :e urls.py<cr>


" ==============================================================================
" Vim-JDE -> Just a Development Environment for VIM. (VJDE)
" cd ~/.vim/bundle
" GIT clone https://github.com/jmanoel7/Vim-JDE.git
" chmod a+x ~/.vim/bundle/Vim-JDE/plugin/vjde/readtags
" ==============================================================================

" use <c-space> as the Code completion key!
" change it by
"let g:vjde_completion_key='<c-space>'


" ==============================================================================
" Settings for python-mode
" Note: I'm no longer using this. Leave this commented out
" and uncomment the part about jedi-vim instead
" cd ~/.vim/bundle
" GIT clone https://github.com/klen/python-mode
" ==============================================================================

"" map <Leader>g :call RopeGotoDefinition()<CR>
"" let ropevim_enable_shortcuts = 1
"" let g:pymode_rope_goto_def_newwin = "vnew"
"" let g:pymode_rope_extended_complete = 1
"" let g:pymode_breakpoint = 0
"" let g:pymode_syntax = 1
"" let g:pymode_syntax_builtin_objs = 0
"" let g:pymode_syntax_builtin_funcs = 0
"" map <Leader>b Oimport ipdb; ipdb.set_trace() # BREAKPOINT<C-c>


" ==============================================================================
" On the fly Python checking in Vim with PyFlakes
" cd ~/.vim/bundle
" GIT clone https://github.com/kevinw/pyflakes-vim.git
" ==============================================================================

"let g:pyflakes_use_quickfix = 0


" ==============================================================================
" vim-pep8: just checks if your python code is pep-8 compliant
" cd ~/.vim/bundle
" mkdir -p vim-pep8/ftplugin/python
" CURL -o vim-pep8/ftplugin/python/pep8.vim http://www.vim.org/scripts/download_script.php?src_id=14366
" pip install --upgrade pep8
" ==============================================================================

"let g:pep8_map='<F8>'


" ==============================================================================
" vim-flake8: Flake8 plugin for Vim
" cd ~/.vim/bundle
" GIT clone https://github.com/nvie/vim-flake8.git
" pip install --upgrade flake8
" ==============================================================================


" ==============================================================================
" YouCompleteMe
" cd ~/.vim/bundle
" GIT clone https://github.com/Valloric/YouCompleteMe.git
" GIT submodule update --init --recursive
" ./install.py --clang-completer --system-libclang --system-boost --omnisharp-completer --gocode-completer --tern-completer
" ==============================================================================


" ============================================================================= 
" MiniBufferExplorer
" cd ~/.vim/bundle
" GIT clone https://github.com/fholgado/minibufexpl.vim.git
" ============================================================================= 

" MiniBufExpl Colors 1
"hi MBENormal               guifg=#808080 guibg=fg
"hi MBEChanged              guifg=#CD5907 guibg=fg
"hi MBEVisibleNormal        guifg=#5DC2D6 guibg=fg
"hi MBEVisibleChanged       guifg=#F1266F guibg=fg
"hi MBEVisibleActiveNormal  guifg=#A6DB29 guibg=fg
"hi MBEVisibleActiveChanged guifg=#F1266F guibg=fg

" MiniBufExpl Colors 2
"hi MBENormal guifg=Blue                                        " for buffers that have NOT CHANGED and are NOT VISIBLE.
"hi MBEChanged guifg=Red                                        " for buffers that HAVE CHANGED and are NOT VISIBLE
"hi MBEVisibleNormal term=bold cterm=bold gui=bold guifg=Green  " buffers that have NOT CHANGED and are VISIBLE
"hi MBEVisibleChanged term=bold cterm=bold gui=bold guifg=Green " buffers that have CHANGED and are VISIBLE

" Taken from http://dotfiles.org/~joaoTrindade/.vimrc
" Minibuffer

" Show the miniBufExplorer from the start
"let g:miniBufExplorerMoreThanOne = 0

" Use a vertical windows
"let g:miniBufExplVSplit = 5

" Put the miniBufExplorer windows at the right
"let g:miniBufExplSplitBelow = 1

"Maximum size of the mini buffer explorer window
"let g:miniBufExplMaxSize = 15

"Still haven't discovered what it does
"let g:miniBufExplMapWindowNavArrows = 1
"let g:miniBufExplMapCTabSwitchBufs = 1
"let g:miniBufExplMapWindowNavVim = 1

" make tabs show complete (no broken on two lines)
"let g:miniBufExplTabWrap = 1

" If you use other explorers like TagList you can (As of 6.2.8) set it at 1:
"let g:miniBufExplModSelTarget = 1

" If you would like to single click on tabs rather than double clicking on them to goto the selected buffer.
"let g:miniBufExplUseSingleClick = 1

"let g:bufExplorerSortBy = "name"

"autocmd BufRead,BufNew :call UMiniBufExplorer


