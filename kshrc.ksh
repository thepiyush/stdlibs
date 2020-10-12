#
# File name: kshrc.txt
#
# Author: Piyush
#
# Description: Modified .kshrc (Korn Shell Run Commands)
# 
# Chanage log:
# 2017/06/26 : Initial version. (Piyush)
#
#
#-----------------------------Modifications start------------------------------
#For MacOS: ~/.bash_profile
alias gvim='/Applications/MacVim.app/Contents/MacOS/Vim -g'
#For Linux: ~/.kshrc
#Press Ctrl+v and then press key to know key-code (@Csh: bind `"^[u":"\n"`) OR
#@shell>od [-cx] then press key(s) and to terminate command press: Ctrl+d
#Keybinds: Arrow keys and Home & End keys:
set -o emacs
alias __A=$(print "\020") # ^[[A = ^p = up = previous command
alias __B=$(print "\016") # ^[[B = ^n = down = next command
alias __C=$(print "\006") # ^[[C = ^f = right = forward a character
alias __D=$(print "\002") # ^[[D = ^b = left = back a character
alias __H=$(print "\001") # ^[OH = ^a = home = beginning of line
alias __W=$(print "\005") # ^[OF = ^e = end = end of line
#Keybinds for Alt+<key>:
alias _q=$(print "\015") # ^[q = Alt+q = <Enter>
alias j='cd ..'
alias _j=$(print "j\015") #Keybinds: Alt+j = j + Enter Key
alias k='cd -'
alias _k=$(print "k\015") #Keybinds: Alt+k = k + Enter Key
alias h='cd $HOME'
alias _h=$(print "h\015") #Keybinds: Alt+h = h + Enter Key
alias _m=$(print "h\015") #Keybinds: Alt+m = h + Enter Key
alias t='ls --color=always'
alias _e=$(print "t\015") #Keybinds: Alt+e = t + Enter Key
alias _t=$(print "t\015") #Keybinds: Alt+t = t + Enter Key
alias n='ls -ltrh --color=always'
alias _o=$(print "n\015") #Keybinds: Alt+o = n + Enter Key
alias _n=$(print "n\015") #Keybinds: Alt+n = n + Enter Key
alias G='gvim -p .'
alias _g=$(print "G\015") #Keybinds: Alt+g = G + Enter Key

alias l='ls -ltrh --color=always'
alias I='set -o viraw' 	#vim mode with autocompletion
alias i='set -o vi' 	#vim mode
alias E='set -o emacs' 	#emacs mode = unset vim mode
#alias s='screen'	#screen mode to copy text from previous output
#alias x='exit'
alias c='clear'
alias p='pwd'
alias g='gvim -p'
alias gr='gvim -pR'
alias gd='gvimdiff'
alias gt='gnome-terminal --maximize'
function nt {
	nut "$@" &
}
##GitHub
alias gh='eval $(ssh-agent -s) && ssh -T git@github.com'
#### Git-lab ssh key setup
##cat ~/.ssh/id_rsa.pub
##ssh-keygen -t rsa -C <your email address>
##cat ~/.ssh/config
##echo "AFSTokenPassing no" >> ~/.ssh/config
##chmod 755 ~/.ssh/config
alias gl='eval $(ssh-agent -s) && ssh -T git@gitlab.com'

#Interactive Shell options
TTY=$(tty|cut -f3-4 -d/)
HISTFILE=$HOME/.sh_hist
PWD=$(pwd)
HOSTNAME=$(hostname)
HOSTNAME=`hostname | awk -F. '{print $1}'`
PS1='${LOGNAME}@${HOSTNAME}: ${PWD}
$'
#ver vxpedit editor
export VXP_EDITOR=gedit

##To call interpreter.py script from Korn shell(~/.kshrc) (Eg. u arg1 arg2 arg3 ...)
#function u {
#	echo "Input Arguments: $0 $@"
#	echo "shell start time = `date +%H:%M:%S.%N`"
####	python /.../interpreter.py 'shell' "$@";
####	if [[ $? == 10 ]];then 
####		#pyscriptout=$(python /.../interpreter.py 'shell' "$@");
####		pyscriptout=`python /.../interpreter.py 'shell' "$@"`;
####		eval ${pyscriptout#*@shell>}
####	fi
###	export PYOUT_INTERPRETER=''
###	echo $PYOUT_INTERPRETER
##	pyscript="python /.../interpreter.py shell $@";
##	set -f; $pyscript; if [[ $? == 10 ]]; then pyscriptout=`$pyscript`; set +f; eval "${pyscriptout#*@shell>}"; fi; set +f;
##	pyscript="python /.../interpreter.py shell";
##	set -f; $pyscript "$@"; if [[ $? == 10 ]]; then pyscriptout=`$pyscript "$@"`; set +f; eval "${pyscriptout#*@shell>}"; fi; set +f;
#	tmpfile=$(mktemp);trap "rm $tmpfile" 0 2 3 15;echo "Created temporary file: "$tmpfile;
#	python /.../interpreter.py 'tmpfile='$tmpfile "$@";
#	if [[ $? == 10 ]];then eval "$(cat "$tmpfile")"; fi;
#	echo "shell stop  time = `date +%H:%M:%S.%N`"
#}
#alias _u=$(print "u\015") #Keybinds: Alt+u = u + Enter Key
#
#function rptlogin { #Auto repeated login tasks
#	print -n "Please Enter Password:"
#	stty -echo
#	read pswd
#	stty echo
#	print -n "\nLogin in ..."
#	#<Commands with password( $pswd )>
#	pswd=""
#	unset pswd
#	#print confirmations
#}
#-----------------------------Modifications end------------------------------

