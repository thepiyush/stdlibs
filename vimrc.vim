"
" File name: .vimrc
"
" Author: Piyush
"
" Description: Modified .vimrc (Vim Run Commands)
" 
" Chanage log:
" 2017/06/26 : Initial version. (Piyush)
"
"

"--------------------Modifications start--------------------
"Type ':set guifont?' to get current guifont
if has("macunix") "(for MacOS)
	set guifont=Menlo-Regular:h18
elseif has("unix") "(for Linux)
	set guifont=Monospace\ 17
else "(for Window)
	set guifont=Lucida_Console:h10
endif
"set linespace=1		"Spacing between lines
set guioptions+=b	"Enable Bottom (horizontal) scrollbar
set number			"Display Line number
"set relativenumber		"Display Relative Line number (available only from version 7.3)
set cursorline		"Highlight Cursor line
set hlsearch		"Highlight Current Search
set incsearch		"Enable Incremental Search
set tabpagemax=100	"Number of Tabs Limit
set tildeop			"Tilde command '~'
set nowrap			"Disable text wraping
set textwidth=0		"Disable automatic text wrapping"
"set diffopt+=iwhite	"To ignore white space difference in gvimdiff
"set cindent			"C style indentation
set autoindent		"Auto copy indentation from current line to new line
set noexpandtab		"Do not expand tab to spaces
set tabstop=4		"Size of tab display in characters
set shiftwidth=4	"Size of indentation in characters
set softtabstop=0	"Non-zero/non-tabstop value will simulate tab with spaces


"solarized colorscheme from http://ethanschoonover.com/solarized/vim-colors-solarized 
"Downloaded from https://github.com/altercation/vim-colors-solarized/blob/master/colors/solarized.vim to ~/.vim/colors/solarized.vim
syntax enable
"set background=dark
"colorscheme solarized

""To save swap/backup/undo files in fixed location, not in current dir
"set directory=~/.vim/swapdir//
"set backupdir=~/.vim/backupdir//
"set undodir=~/.vim/undodir//
"""To turn-off swap/backup files creation, recovery is impossible!
""set noswapfile
""set nobackup

"nnoremap <esc> :noh<return><esc>
"Alternative to Ctrl+'u'
nmap <C-k> <C-u>
"Alternative to Ctrl+'d'
nmap <C-j> <C-d>

"To map <leader> key to space-bar
let mapleader = " "
"Alternative to re-source .vimrc
nmap <leader>. :source ~/.vimrc<CR>
"Alternative to character ':'
nmap <leader><leader> :
"Alternative to character '"'
map <leader>u "
"To set (dark or light) solarized colorscheme
if has("macunix") "(for MacOS)
	nmap <leader>c :set guifont=Menlo-Bold:h18<CR>:let &background=(&background=="dark"?"light":"dark")<BAR>set background?<CR>:colorscheme solarized<CR>
elseif has("unix") "(for Linux)
	nmap <leader>c :set guifont=Monospace\ Bold\ 17<CR>:let &background=(&background=="dark"?"light":"dark")<BAR>set background?<CR>:colorscheme solarized<CR>
else "(for Window)
	nmap <leader>c :set guifont=Lucida_Console:h10:b<CR>:let &background=(&background=="dark"?"light":"dark")<BAR>set background?<CR>:colorscheme solarized<CR>
endif
"To set default colorscheme
if has("macunix") "(for MacOS)
	nmap <leader>C :set guifont=Menlo-Regular:h18<CR>:set background=light<CR>:colorscheme default<CR>
elseif has("unix") "(for Linux)
	nmap <leader>C :set guifont=Monospace\ 17<CR>:set background=light<CR>:colorscheme default<CR>
else "(for Window)
	nmap <leader>C :set guifont=Lucida_Console:h10<CR>:set background=light<CR>:colorscheme default<CR>
endif
"To avoid adding linebreak after default textwidth 78 (optional>:set wrapmargin=0<CR>:set formatoptions-=t<CR>)
nmap <leader>l :set textwidth=0<CR>
"To highlight/unhighlight current line
nmap <leader>L :set cursorline!<CR>
"To set relative line-number (available only from version 7.3)
nmap <leader>r :set relativenumber!<CR>
"To unhighlight previous search
nmap <leader>h :nohlsearch<CR>
"To highlight syntax as shell file
nmap <leader>H :set syntax=sh<CR>
"To run command in all open tabs
nmap <leader>t :tabdo 
"To open see all search matched line in quickfix window
nmap <leader>T :vimgrep /<C-r>//g%<CR>:copen<CR>f\|zs
"To move cursor regardless of available characters
nmap <leader>v :let &virtualedit=(&virtualedit==""?"all":"")<BAR>set virtualedit?<CR>
"To cut
vmap <leader>x "*x
"To copy
vmap <leader>y "*y
"To paste before cursor
nmap <leader>P "*P
"To paste after cursor
nmap <leader>p "*p
"To select all
nmap <leader>a ggVG
"To save current file
nmap <leader>s :w<CR>
"To exit
nmap <leader>q :q<CR>
"Alternative to Ctrl+'w'
nmap <leader>w <C-w>
"To open current file directory in gvim file explorer
nmap <leader>e :e %:p:h<CR>
"To open recently opened file/directory
nmap <leader>b <C-^>
"To open file from recently opened file list
nmap <leader>B :browse oldfiles!<CR>
"To open file in new tab from filepath under cursor
nmap <leader>f "zyiW :tabedit <C-r>z*<CR>
"To open file in new tab from filename under cursor
nmap <leader>F "zyiw :tabedit %:p:h/<C-r>z*<CR>
"To highlight GPA grades with color
function! GPAhighlight()
	set nowrap
	set guioptions+=b
	set virtualedit=all
	highlight CursorLine gui=bold guibg=NONE
	set cursorline
	syntax match Grade_A_NA_4 "\( A  \| NA \|4\...\%[ ]\)"
	highlight Grade_A_NA_4 guibg=green guifg=black
	syn match Grade_B_C_L4 "\( B  \| C  \|[0-3]\...\%[ ]\)" 
	hi Grade_B_C_L4 guibg=yellow guifg=black
	syn match Grade_Px / P. /
	hi Grade_Px guibg=gray guifg=black
	syn match Grade_D " D  "
	hi Grade_D guibg=red guifg=black
	syn match Grade_F " F  "
	hi Grade_F guibg=white guifg=black
	vertical diffsplit
	vertical resize 30
"	set scrollopt-=hor
"	diffupdate
	set scrollbind scrollopt-=hor
	execute "normal! gg\<C-w>\<C-w>gg"
	set nohlsearch
	execute "normal! /VIM \<CR>zs"
	echom "Grades has been highlighted"
endfunction
nmap <leader>g :call GPAhighlight()<CR>

"gvim Informations:
":so ~/.vimrc					"To load ~/.vimrc without closing file
".								"To repeat last normal mode command
"@:								"To repeat last command-line command/changes
":%s/word/willreplace/gc		"To replace beginning
":.,$s/word/willreplace/gc		"To replace from current cursor position
":%s/\(.*\) \(.*\)/\=printf('%3d %s %s',line('.'),submatch(2),submatch(1))/gc "To print with current line no with swap words
"/start\_.\{-}\_$				"To search
"/start\_.\{-}end				"Between 'start' and 'end_of_line','\_.\{-}\_$' search any character or including line break upto any first match of 'end'
"/Word\c						"For case insensitive
"/word\C						"For case sensitive
"/word/e+1						"For 1 offset of cursor position from matched word end
"/4\...\%[ ]					"To search 4. + any 2 character + space if next char is space
"/"[^"]*"						"To search " + any character other than " + "
":sort[!] rn //					"To sort last searched pattern,n=numerical sort,r=for matched pattern,!=reverse sort
":%!column -t -s ','			"To reformat column of csv separated by ',' (',' will replace by spaces)
"/^[A-Z]\?\s\+\d\+				"To find pattern like:(' 1' or'N   2')
"/\d\{2,4}						"To find pattern like:'23' or '345' or '4567' but not '1' or '56789'
":%s/^\(.*\)\(\n\1\)\+$/\1/gc	"To delete consecutive duplicates lines
":g/pattern/d					"To delete all lines that match a pattern
":v/pattern/d					"To delete all lines that does NOT match a pattern
"Ctrl+v <select_lines> Shift+i	"To enter in insert mode to add text at selected multiple lines
"Ctrl+r <Register>				"To paste from register(eg.*,",a) in insert mode
":w !python						"To run Python script from Vim
":w !python - [arg1] ... [argn]	"To run Python script with arguments from Vim

":set iskeyword="@,@-@,(,),*"	"To use word which includes [alpha,@,(,),*] for search with '*'/'#'/word

"--------------------Modifications end--------------------

