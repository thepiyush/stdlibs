#
# File name: stdlib.py
#
# Author: Piyush
#
# Description: Frequently used functions/defs
# 
# Chanage log:
# 2017/06/26 : Initial version. (Piyush)
#
#

import sys
import os
import subprocess
import time
import difflib
import itertools
import re
import numpy as np
import inspect
import datetime
#from optparse import OptionParser

def verify_Python_version():
	"""Check and verify current version of Python"""
	if sys.version_info != (2, 6, 6, 'final', 0):
		userexit('ask',"Script may not run properly due to different Python versions:\n" + \
			"\tScript is written for Python 2.6.6 and current Python version is " + str(sys.version_info) + ".")

def get_parsedarguments(args):
	"""Return parsed arguments and return2shell info"""
	#Read arguments
	#parser = OptionParser()
	#parser.add_option("-d","--datafile", dest='datafile',help='Help for datafile argument.')
	#(options, args) = parser.parse_args()
	#arg1 = str(options.datafile)
	#if(arg1 == 'None'):
	#	print("\nDatafile does not found.\n")
	#	sys.exit(0)
	args = []
	for i in range(2+10):
		args.append(('' if(str(sys.argv[i]) == ',')else str(sys.argv[i])) if(len(sys.argv) > i)else '')
	#print("List of real system arguments:\n  "+"\n  ".join([str(idx) + "." + ag for idx,ag in enumerate(args)]))
	return2shell = False
	if(args[1] == 'shell'):
		args.pop(1)
		args.append('')
		return2shell = True
	if(args[1].strip() != '' and '.' in args[1]):
		infofile = args[1].replace(',','\n').replace('.',' ') + '\n'
		args[1] = '--'
	else:
		infofile = 'file'
	return return2shell,infofile,args

def userexit(status = 'ask',errormsg = ''):
	"""Confirmation with user before termination of script"""
	if(status == 'ask'):
		if(errormsg):
			print(errormsg)
		allow = raw_input("Press \"y\" to continue or other character to terminate script :")
		if allow != "y" and allow != "Y" and allow != "yes" and allow != "Yes":
			print("\nExecution Aborted.\n")
			sys.exit(0)
	else:
		if(errormsg):
			print("ERROR: " + errormsg + "\n\nExecution Aborted.\n")
		sys.exit(0)
	return 0

def userselect(datalist=[]):
	"""Return index of user selected element from given data list"""
	while True:
		print("")
		for idx,ele in enumerate(datalist[::-1]):
			print(str(len(datalist)-idx) + ". " + ele)
		print("0. Exit")
		idx = raw_input("To select one element from above list, Please Enter Sequence Number :")
		if(idx.isdigit() and 0<(int(idx))<=len(datalist)):
			break
		else:
			if(idx.isdigit() and int(idx)==0):
				userexit('exit',"User Exit.")
			print("\nInvalid Sequence Number. Please valid Sequence Number." if(idx.isdigit())else "\nInvalid user input. Please Enter Numbers only.")
	return int(idx)-1

def userinput(usermsg):
	"""Return user input for given message"""
	inputstr = raw_input(usermsg)
	return inputstr

def cmd(cmdstr,shellcmd = False):
	"""Run system command and wait until completion of it"""
	try:
		if(shellcmd == True):
			process = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Start command
		else:
			process = subprocess.Popen(cmdstr.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False) #Start command
		return process.communicate()[0] #Wait until completion of command and return output
	except:
		userexit('exit',"\'" + cmdstr + "\' command cannot be executed.")
		return -1

def get_expandedpath(path):
	"""Return 'home director' and 'environment variables' expanded path"""
	return os.path.expandvars(os.path.expanduser(path))

def issamepath(dirpath1,dirpath2):
	"""Return True if dirpath1 and dirpath2 are same."""
	return (get_expandedpath(dirpath1) == get_expandedpath(dirpath2))

def isdirpath(dirpath):
	"""Return True if dirpath exist else False"""
	return os.path.isdir(get_expandedpath(dirpath))

def islinkpath(linkpath):
	"""Return True if linkpath exists else False"""
	return os.path.islink(get_expandedpath(linkpath))

def isfilepath(filepath):
	"""Return True if filepath exists else False"""
	return os.path.isfile(get_expandedpath(filepath))

def ispathexists(path):
	"""Return True if path exists else False"""
	return os.path.exists(get_expandedpath(path))

def makedir(dirpath):
	"""Delete existing directory and Make/Create new directory"""
	if(isdirpath(dirpath)):
		cmd("rm -rf " + dirpath)
		if(not isdirpath(dirpath)):
			print("\'" + dirpath + "\' directory has been deleted.")
		else:
			userexit('exit',"\'" + dirpath + "\' directory cannot be deleted.")
	os.makedirs(get_expandedpath(dirpath))
	if(isdirpath(dirpath)):
		print("\'" + dirpath + "\' directory has been created.")
	else:
		userexit('exit',"\'" + dirpath + "\' directory has not been created.")

def copydir(sourcedirpath,destinationdirpath):
	"""Delete existing directory and Copy source directory to destination directory"""
	if(isdirpath(destinationdirpath)):
		cmd("rm -rf " + destinationdirpath)
		if(not isdirpath(destinationdirpath)):
			print("\'" + destinationdirpath + "\' directory has been deleted.")
		else:
			userexit('exit',"\'" + destinationdirpath + "\' directory cannot be deleted.")
	cmd("cp -rf " + sourcedirpath + " " + destinationdirpath)
	if(isdirpath(destinationdirpath)):
		print("\'" + destinationdirpath + "\' directory has been copied from \'" + sourcedirpath + "\'")
	else:
		userexit('exit',"\'" + destinationdirpath + "\' directory has not been copied.")

def linkdir(sourcedirpath,destinationdirpath):
	"""Delete existing directory and Link destination directory to source directory"""
	if(isdirpath(destinationdirpath)):
		cmd("rm -rf " + destinationdirpath)
		if(not isdirpath(destinationdirpath)):
			print("\'" + destinationdirpath + "\' directory has been deleted.")
		else:
			userexit('exit',"\'" + destinationdirpath + "\' directory cannot be deleted.")
	cmd("ln -nfs " + sourcedirpath + " " + destinationdirpath)
	if(islinkpath(destinationdirpath)):
		print("\'" + destinationdirpath + "\' directory has been linked to \'" + sourcedirpath + "\'")
	else:
		userexit('exit',"\'" + destinationdirpath + "\' directory has not been linked.")

def makefile(filepath,filelines):
	"""Delete existing file and Create & Update new file"""
	fileexist = isfilepath(filepath)
	try:
		with open(get_expandedpath(filepath), 'w+') as f:
			f.writelines(filelines)
		if(isfilepath(filepath)):
			print("\'" + filepath + "\' file has been " + ("created and " if(not fileexist) else "") + "updated.\n")
		else:
			userexit('exit',"\'" + filepath + "\' file has not been created.")
	except:
		userexit('exit',"\'" + filepath + "\' file cannot create/open in writemode.")

def copyfile(sourcefilepath,destinationdirpath):
	"""Create destination directory if not exist and Copy source file to destination directory"""
	if(not isdirpath(destinationdirpath)):
		makedir(destinationdirpath)
	cmd("cp " + sourcefilepath + " " + destinationdirpath)
	if(isfilepath(destinationdirpath  + "/" + sourcefilepath.split('/')[-1])):
		print("\'" + destinationdirpath + "/" + sourcefilepath.split('/')[-1] + "\' file has been copied from \'" + sourcefilepath + "\'")
	else:
		userexit('exit',"\'" + destinationdirpath+"/"+sourcefilepath.split('/')[-1] + "\' file has not been copied.")

def readfile(filepath):
	"""Return all filelines"""
	if(not isfilepath(filepath)):
		userexit('exit',"\'" + filepath + "\' file does not exist.\n")
	try:
		with open(get_expandedpath(filepath), 'r') as f:
			filelines = f.readlines()
	except:
		userexit('exit',"\'" + filepath + "\' file cannot open in readmode.")
	return filelines

def get_unique_list(normal_list):
	"""Return list with deleted duplicate elements"""
	unique_list = []
	[unique_list.append(l) for l in normal_list if not unique_list.count(l)]
	return unique_list

def get_matchindices(file,pattern):
	"""Return match indices in file/filelist (format:[[[line number, start of match, end of match],...],[...],...])"""
	lineno = 0
	if type(pattern) is str:
		pl = [re.compile(pattern)]
	elif type(pattern) is list:
		pl = [re.compile(p) for p in pattern]
	else:
		userexit('exit',"Unsupported 'type' of object pattern:\'" + pattern + "\'.")
	matchindices = [[] for i in range(len(pl))]
	if type(file) is str:
		filepath = file
		if(not isfilepath(filepath)):
			userexit('exit',"\'" + filepath + "\' file does not exist.\n")
		try:
			with open(get_expandedpath(filepath), 'r') as f:
				for line in f:
					for i,p in enumerate(pl):
						for m in p.finditer(line):
							matchindices[i].append([lineno]+list(m.span()))
					lineno = lineno + 1
		except:
			userexit('exit',"\'" + filepath + "\' file cannot open in readmode.")
	elif type(file) is list:
		filelines = file
		for line in filelines:
			for i,p in enumerate(pl):
				for m in p.finditer(line):
					matchindices[i].append([lineno]+list(m.span()))
			lineno = lineno + 1
	else:
		userexit('exit',"Unsupported 'type' of object 'file':\'" + file + "\'.")
	return matchindices if(type(pattern) is list) else matchindices[0]

def get_matchsections(filepath,startpattern,endpattern):
	"""Return start and end line numbers of match section in file"""
	matchsections = []
	matchlines = get_matchindices(filepath,[startpattern,endpattern])
	matchlinesstart = get_unique_list([i[0] for i in matchlines[0]])
	matchlinesend = get_unique_list([i[0] for i in matchlines[1]])
	for matchstart in matchlinesstart:
		matchend = next(itertools.ifilter(lambda x:(x>matchstart), matchlinesend), -1)
		if(matchend != -1):
			matchsections.append([matchstart,matchend])
	return matchsections

def get_matchsectionlines(filepath,startpattern,endpattern,sectionno=0):
	"""Return file lines between start pattern and end pattern of given section"""
	lineno = 0
	matchsectionlines = []
	matchsections = get_matchsections(filepath,startpattern,endpattern)
	if(sectionno < len(matchsections)):
		section = matchsections[sectionno]
		try:
			with open(get_expandedpath(filepath), 'r') as f:
				for line in f:
					if(lineno >= section[0] and lineno <= section[1]):
						matchsectionlines.append(line)
					lineno = lineno + 1
		except:
			userexit('exit',"\'" + filepath + "\' file cannot open in readmode.")
		return matchsectionlines[1:-1]
	else:
		userexit('exit',"'" + startpattern + "' and/or '" + endpattern + "' patterns does not exist for section number:" + str(sectionno) + " in file:\n" + filepath)
		return []

def add_matchsectionline(filepath,startpattern,endpattern,line,sectionno=0):
	"""Add 'line' at end part of given section number define by start pattern and end pattern"""
	matchsections = get_matchsections(filepath,startpattern,endpattern)
	if(sectionno < len(matchsections)):
		section = matchsections[sectionno]
		filelines = readfile(filepath)
		filelines.insert(section[1],line)
		makefile(filepath,filelines)
	else:
		userexit('exit',"'" + startpattern + "' and/or '" + endpattern + "' patterns does not exist for section number:" + str(sectionno) + " in file:\n" + filepath)

def get_nearest_match(word,wordlist):
	"""Find nearest matching element from list"""
	if word != '':
		matched_init_words = [wordlist[i] for i,v in enumerate([l.find(word) for l in wordlist]) if v>=0]
		if matched_init_words:
			return difflib.get_close_matches(word,matched_init_words,1,0)[0]
		else:
			return difflib.get_close_matches(word,wordlist,1,0)[0]
	else:
		return ''

def get_diffcnol(diffout):
	"""Return Change Number of Line in output of 'diff' command (Eg. diff -iEbwBsI '^\s*--\|^\s*$' <file1> <file2>)"""
	if(len(diffout.split('\n'))!=2 or diffout.split()[-1]!='identical'):
		diffadd = diffdelete = diffcnol = 0
		for d in diffout.split('\n'):
			if(d):
				if(d[0]=='>'):
					diffadd = diffadd + 1
				elif(d[0]=='<'):
					diffdelete = diffdelete + 1
				elif(d[0] in ['0','1','2','3','4','5','6','7','8','9']):
					diffcnol = diffcnol + max(diffadd,diffdelete)
					diffadd = diffdelete = 0
		diffcnol = diffcnol + max(diffadd,diffdelete)
	else:
		diffcnol = 0
	return diffcnol

def get_logiccomponents(logicdir,toplogic):
	"""Return all subcomponents of given toplevel component from logicdir"""
	logiccompall = [toplogic.lower()]
	i = 0
	while(i < len(logiccompall)):
		logiccomps = cmd("grep -ohiE '^.*entity\s+[0-9A-Za-z_.]+|^.*component\s+[0-9A-Za-z_]+' " + logicdir+'/vhdl/'+logiccompall[i]+'.vhdl',True).split('\n')[:-1]
		logiccompall.extend(get_unique_list([lc.split()[-1].split('.')[-1].lower() for lc in logiccomps if('--' not in lc)] if(len(logiccomps))else []))
		logiccompall = get_unique_list(logiccompall)
		i = i + 1
	if('is' in logiccompall):
		logiccompall.remove('is')
	return logiccompall

def get_logicdiff(logicdir1,logicdir2,toplogic):
	"""Return all subcomponets of toplevel component with compare code (-3=Does not exit in both,-2=Does not exit in dir2,-1=Does not exit in dir1,0=Same in both,>0=CNoL)"""
	if(not isdirpath(logicdir1) or not isdirpath(logicdir2)):
		userexit('exit',"Invalid Argument. Please provide valid logic version information.")
	logicdiff = []
	for logiccomp in get_unique_list(get_logiccomponents(logicdir1,toplogic) + get_logiccomponents(logicdir2,toplogic)):
		if(logiccomp):
			logicdir1comptype = ('vhdl' if(isfilepath(logicdir1+'/vhdl/'+logiccomp+'.vhdl'))else '')
			logicdir2comptype = ('vhdl' if(isfilepath(logicdir2+'/vhdl/'+logiccomp+'.vhdl'))else '')
			if(logicdir1comptype == 'vhdl' == logicdir2comptype):
				diff = cmd("diff -iEbwBsI '^\s*--\|^\s*$' " + logicdir1+'/vhdl/'+logiccomp+'.vhdl ' + logicdir2+'/vhdl/'+logiccomp+'.vhdl',True)
				logicdiff.append([logiccomp+'.vhdl',get_diffcnol(diff)])
			else:
				logicdiff.append([logiccomp,(-1 if(logicdir1comptype == '')else 0) + (-2 if(logicdir2comptype == '')else 0)])
	return logicdiff

def get_logicdifftxt(logicdir1,logicdir2,toplogic):
	"""Print logic components informations and Return differ logic components list"""
	logicdiff = get_logicdiff(logicdir1,logicdir2,toplogic)
	if(sum(ld[1]>0 for ld in logicdiff)):
		print("Following components have difference between two release (with Changed No of Lines):\n" + ', '.join([ld[0]+'(CNoL='+str(ld[1])+')' for ld in logicdiff if(ld[1]>0)]) + "\n")
	if(sum(ld[1]==-1 for ld in logicdiff)):
		print("Following components does not exist for " + logicdir1 + " release:\n" + ', '.join([ld[0] for ld in logicdiff if(ld[1]==-1)]) + "\n")
	if(sum(ld[1]==-2 for ld in logicdiff)):
		print("Following components does not exist for " + logicdir2 + " release:\n" + ', '.join([ld[0] for ld in logicdiff if(ld[1]==-2)]) + "\n")
	if(sum(ld[1]==0 for ld in logicdiff)):
		print("Following components are identical for both release:\n" + ', '.join([ld[0] for ld in logicdiff if(ld[1]==0)]) + "\n")
	if(sum(ld[1]==-3 for ld in logicdiff)):
		print("Following components does not exist for both release:\n" + ', '.join([ld[0] for ld in logicdiff if(ld[1]==-3)]) + "\n")
	return [ld[0] for ld in logicdiff if(ld[1]>0)]

def get_environ(envvar):
	"""Return value of environment variable"""
	envvarvalue = os.getenv(envvar) #to get start-up envvar: os.environ.get(envvar)
	if(envvarvalue == None):
		userexit('exit',"'" + envvar + "' environment variable is NOT defined. Please define it and re-run.")
	return envvarvalue

def get_pwd():
	"""Get present working directory"""
	return os.getenv('PWD') #will return referenced symbolic link
	#return os.getcwd() #will return dereferenced symbolic link

def get_datetime_str():
	"""Return current data and time string"""
	return time.strftime("%Y%m%d%H%M%S")

def get_commandlist(*commandtypes):
	"""Get list of available commands based on type"""
	commandlist = { 
			'editor'	: ['gvim','gvimr','emacs','emacsr','kate','gedit','nedit'],
			'diffeditor'	: ['gvimdiff','tkdiff'],
			'imageviewer'	: ['eog ','display'],
			'command'	: ['cd','cdls','cdlsltr','ls','lsltr ','cat','grep ','awk']
		}
		#Adjusted spaces to get following output:
		#>print([c+" = "+get_commandname(c,'command','editor') for c in ['g','r','gp','l','lt']])
		# ['g = gvim', 'r = gvimr', 'gp = grep', 'l = ls', 'lt = lsltr']
	cmdlist = []
	for ct in commandtypes:
		cmdlist.extend(commandlist[get_nearest_match(ct,commandlist.keys())])
	return get_unique_list(cmdlist)

def get_commandname(cmdstr,*commandtypes):
	"""Get exact command name based on command string and command types"""
	return get_nearest_match(cmdstr.lower(),get_commandlist(*commandtypes)).strip()

def sendcmd2shell(cmdstr):
	"""Print shell command and return to parent script"""
	#os.environ['PYOUT_INTERPRETER'] = "@shell>" + cmdstr
	#os.putenv('PYOUT_INTERPRETER',"@shell>" + cmdstr)
	#cmd("export PYOUT_INTERPRETER='@shell>'",True)
	#print 'PYOUT_INTERPRETER:'+str(get_environ('PYOUT_INTERPRETER'))
	print("@shell>" + cmdstr)
	sys.exit(10)

def get_pathlist(pathmatrix,pathtype = 'file',filestr='',lsltrpickup = 0):
	"""Generate available file(s)/directory(-ies) path list from given absolute pathmatrix"""
	if type(pathmatrix) is str:
		pathmatrix = [pathmatrix]
	if(sum(map(lambda i: (1 if(type(i) is list)else 0),pathmatrix))/float(len(pathmatrix)) == 1):
		pathlist = [''.join(map(str,i)) for i in map(list,itertools.product(*filter(None,pathmatrix)))]
	elif(sum(map(lambda i: (1 if(type(i) is list)else 0),pathmatrix))/float(len(pathmatrix)) == 0):
		pathlist = pathmatrix
	else:
		userexit('exit',"Invalid structure found for pathmatrix in '" + sys._getframe().f_code.co_name + "' function.")
	pathlist = [get_expandedpath(path) for path in pathlist]
	availablepathlist = []
	if(pathlist == []):
		print("Empty 'path list' found. Provide valid 'path matrix' to generate path list.")
	else:
		if(pathtype != 'file' or (pathtype == 'file' and filestr != '')):
			dirpathlist = []
			[dirpathlist.append('/'.join(p.split('/')[:-1])) for p in pathlist if not dirpathlist.count('/'.join(p.split('/')[:-1]))]
			pathlist = [p+'/'+filestr for p in dirpathlist] if(pathtype == 'file' and filestr != '')else dirpathlist
		for path in pathlist:
			if('*' not in list(path) and '{' not in list(path) and '}' not in list(path)):
				if(ispathexists(path)):
					availablepathlist.append(path)
				else:
					print("'" + path + "' path does not exist.")
			else:
				#path can be define using wildcard pattern (for more info >man 7 glob)
				listedpaths = cmd("ls -trd " + path, True)
				listedpaths = listedpaths.split()[-lsltrpickup:]
				for lp in listedpaths:
					if(lp[-1] == '~'): #To avoid gvim swap file.
						listedpaths.remove(lp)
				if(listedpaths):
					availablepathlist.extend(listedpaths)
				else:
					print(("Directory" if(pathtype!='file')else "File") + " not found for '" + path + "' path search.")
	return availablepathlist

def openpath(pathmatrix,editor='',searchstr='',filestr='',lsltrpickup=0,return2shell=False):
	"""Open file or dir path with given constraint like editor,searchstr,filestr,lsltrpickup,etc."""
	editor = get_commandname(editor,'command','editor') if(type(editor) is str)else get_commandname(*editor)
	lsltrpickup = (int(lsltrpickup) if(lsltrpickup.isdigit())else 0) if(type(lsltrpickup) is str)else lsltrpickup
	pathlist = get_pathlist(pathmatrix,'dir' if(editor in ['cd','cdls','cdlsltr','ls','lsltr'])else 'file',filestr,lsltrpickup)
	pathliststr = (" ".join(pathlist)).strip()
	if(len(pathlist) > 10 and editor not in ['ls','lsltr','grep']):
		userexit('ask',"This command will open " + str(len(pathlist)) + (" directories(terminals)." if(editor in ['cd','cdls','cdlsltr'])else " files(editors)."))
	if(pathliststr):
		#Editors
		if(editor == 'gvim'):
			os.system("gvim -p " + ((" -c \"/" + searchstr + "\" ") if(searchstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'gvimr'):
			os.system("gvim -pR " + ((" -c \"/" + searchstr + "\" ") if(searchstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'emacs'):
			for fpl in pathlist:
				os.system("emacs " + fpl + " &")
				print("Opened " + editor + " with file: " + fpl)
		elif(editor == 'emacsr'):
			for fpl in pathlist:
				os.system("emacs " + fpl + " --eval \'(setq buffer-read-only t)\' &")
				print("Opened " + editor + " with file: " + fpl)
		elif(editor == 'kate'):
			os.system("kate -u " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'gedit'):
			os.system("gedit " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'nedit'):
			os.system("nedit " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		#Diff Editors
		elif(editor == 'gvimdiff'):
			os.system("gvimdiff " + ((" -c \"/" + searchstr + "\" ") if(searchstr != '')else "") + pathliststr + " &")
			print("Opened " + editor + " with files: " + pathliststr)
		elif(editor == 'tkdiff'):
			os.system("tkdiff " + pathliststr + " &")
			print("Opened " + editor + " with files: " + pathliststr)
		#Image Viewer
		elif(editor == 'eog'):
			os.system("eog -n " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'display'):
			for fpl in pathlist:
				os.system("display " + fpl + " &")
				print("Opened " + editor + " with file: " + fpl)
		#Commands
		elif(editor == 'cd' or editor == 'cdls' or editor == 'cdlsltr'):
			for idx,dir in enumerate(pathlist):
				if(return2shell == True and (idx == 0 and len(pathlist) == 1 and dir != get_pwd())):
					if(editor == 'cd'):
						sendcmd2shell("cd " + dir)
					elif(editor == 'cdls'):
						sendcmd2shell("cd " + dir + " && ls --color=always " + filestr)
					else:
						sendcmd2shell("cd " + dir + " && ls -ltrh --color=always " + filestr)
				else:
					if(editor == 'cd'):
						os.system("gnome-terminal --window --maximize --working-directory=\"" + dir + "\"")
					elif(editor == 'cdls'):
						os.system("gnome-terminal --window --maximize --working-directory=\"" + dir + "\" -e \"ksh -c 'ls --color=always "+searchstr+" "+filestr+"';ksh\"")
					else:
						os.system("gnome-terminal --window --maximize --working-directory=\"" + dir + "\" -e \"ksh -c 'ls -ltrh --color=always "+searchstr+" "+filestr+"';ksh\"")
					print("Opened gnome-terminal with dir: " + dir)
		elif(editor == 'ls'):
			print("ls --color=always " + (" ".join([dir + "/" + filestr for dir in pathlist])) + " :")
			os.system("ls --color=always " + (" ".join([dir + "/" + filestr for dir in pathlist])))
		elif(editor == 'lsltr'):
			print("ls -ltrh --color=always " + (" ".join([dir + "/" + filestr for dir in pathlist])) + " :")
			os.system("ls -ltrh --color=always " + (" ".join([dir + "/" + filestr for dir in pathlist])))
		elif(editor == 'cat'):
				print("cat " + pathliststr + " :")
				os.system("cat " + pathliststr)
				print("")
		elif(editor == 'grep'):
			if(searchstr != ''):
				print("zgrep --color=always -e " + searchstr + " " + pathliststr + " :")
				os.system("zgrep --color=always -e " + searchstr + " " + pathliststr)
			else:
				print(" ".join(pathlist) + "\nEnter one more argument for 'PATTERN' to 'grep' in file(s).")
		elif(editor == 'awk'):
			if(searchstr != ''):
				print("awk '" + searchstr + "' " + pathliststr + " :")
				os.system("awk '" + searchstr + "' " + pathliststr)
			else:
				print(" ".join(pathlist) + "\nEnter one more argument for 'PATTERN'/'ACTION' to 'awk' in file(s).")
		#Default
		else:
			os.system("gvim -p " + ((" -c \"/" + searchstr + "\" ") if(searchstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))

def get_aliaslist(datalist):
	"""Return alias(unique keyword/alphanumeric) for each element of list"""
	aliaslist = []
	for i in range(len(datalist)):
		matchidx = np.array([0]*len(datalist[i]))
		for j in range(len(datalist)):
			if(j != i):
				for sm in difflib.SequenceMatcher(None, datalist[i], datalist[j]).get_matching_blocks()[:-1]:
					matchidx[sm[0]:sm[0]+sm[2]] += 1
		matchidx_sorted4value = [ele[0] for ele in sorted(enumerate(matchidx.tolist()), key=lambda x:x[1])]
		for idx,j in enumerate(matchidx_sorted4value):
			if(datalist[i][j].isalpha()):
				if(datalist[i][j].lower() not in aliaslist):
					aliaslist.append(datalist[i][j].lower())
				else:
					for k in matchidx_sorted4value[idx+1:]:
						ma = (datalist[i][j]+datalist[i][k]).lower()
						if(ma not in aliaslist and ma.isalnum()):
							aliaslist.append(ma)
							break
					else:
						continue
			else:
				continue
			break
		if(len(aliaslist)-1 != i):
			aliaslist.append('a'+str(i+1))
	return aliaslist

def get_selectedindex(inputstr,datalist,aliaslist,sequencelist):
	"""Return selected index using data or alias or sequence number"""
	inputstr = inputstr.strip()
	if(inputstr.isdigit()):
		selectionlist = sequencelist
	elif(inputstr.replace('-','').isalnum()):
		selectionlist = aliaslist
	else:
		selectionlist = datalist
	selectedinput = get_nearest_match(inputstr,selectionlist)
	if(selectedinput != ''):
		return selectionlist.index(selectedinput),sequencelist[selectionlist.index(selectedinput)]
	else:
		return '',''

def get_selectedindices(inputstr,datalist,aliaslist=[],sequencelist=[]):
	"""Return selected indices using data/alias/sequence separated by ',' and/or range limit separated by '-' or all (data) with '--'"""
	if(not datalist):
		userexit('exit',"No data fonud for selection. Please provide data list for selection.")
	if(not aliaslist):
		aliaslist = get_aliaslist(datalist)
	if(not sequencelist):
		sequencelist = map(str,range(1,1+len(datalist)))
	selectedindices = []
	if ('--' in inputstr):
		selectedindices = range(len(datalist))
	else:
		for mn in inputstr.split(','):
			if(mn.strip() == ''):
				continue
			elif('-' in list(mn)):
				m_start_mn , m_stop_mn = '' , ''
				if(mn.strip().split('-')[0].strip() != ''):
					m_start_i,m_start_mn = get_selectedindex(mn.strip().split('-')[0].strip(),datalist,aliaslist,sequencelist)
				if(mn.strip().split('-')[1].strip() != ''):
					m_stop_i,m_stop_mn = get_selectedindex(mn.strip().split('-')[1].strip(),datalist,aliaslist,sequencelist)
				if(m_start_mn == '' and m_stop_mn == ''):
					continue
				elif(m_start_mn != '' and m_stop_mn == ''):
					selectedindices.append(m_start_i)
				elif(m_start_mn == '' and m_stop_mn != ''):
					selectedindices.append(m_stop_i)
				else:
					if(int(m_stop_mn) > int(m_start_mn)):
						for m_ss in range(int(m_start_mn),int(m_stop_mn)+1):
							selectedindices.append(get_selectedindex(str(m_ss),datalist,aliaslist,sequencelist)[0])
					elif(int(m_stop_mn) < int(m_start_mn)):
						for m_ss in range(int(m_start_mn),int(m_stop_mn)-1,-1):
							selectedindices.append(get_selectedindex(str(m_ss),datalist,aliaslist,sequencelist)[0])
					else:
						selectedindices.append(m_start_i)
			else:
				selectedindices.append(get_selectedindex(mn,datalist,aliaslist,sequencelist)[0])
	return selectedindices

def get_dir_relevanceindex(dir,matchparameters):
	"""Return most relevance (row) index of match parameters(=[[p11,p12,...][p21,p22,...][...]) for given dir"""
	parameter_matching_weight = [0]*len(matchparameters)
	for idx,row in enumerate(matchparameters):
		for p in row:
			if(p in dir):
				parameter_matching_weight[idx] += (1+(len(p)/float(len(dir))))
	return parameter_matching_weight.index(max(parameter_matching_weight)),max(parameter_matching_weight)

def get_dirs_updated(dir,matchparameters,setparameters):
	"""Return updated dir(s) for given set parameters(=[[p11,p12,...][p21,p22,...][...]) accordingly to match parameters relevance"""
	matched_parameters_index,matched_parameters_value = get_dir_relevanceindex(dir,matchparameters)
	matched_parameters = matchparameters[matched_parameters_index]
	updated_dirpathlist = []
	if(matched_parameters_value > 0):
		for row in setparameters:
			updated_dir = dir
			for idx,p in enumerate(row):
				updated_dir = updated_dir.replace(matched_parameters[idx],p)
			updated_dirpathlist.append(updated_dir)
	return [d for d in get_unique_list(updated_dirpathlist) if(dir!=d)]

def get_indented_list(normal_list,noofcolumn):
	"""Return list with Added Tab(s)('\t') to the elements of list to indent columns"""
	maxcolumnlenlist = [(8*(1 + (len(max(normal_list[r::noofcolumn],key=len))/8))) for r in range(noofcolumn)]
	indentedlist = []
	for index,value in enumerate(normal_list):
		indentedlist.append(value + ('\n' if(not ((index+1)%noofcolumn))else "".join((1 + (((maxcolumnlenlist[index%noofcolumn]-len(value))-1)/8))*['\t'])))
	return indentedlist

def list_dir(dirpath,list_type = 'lsltr'):
	"""List(Print) file names of given absolute directory path"""
	print(dirpath + "/:")
	if(list_type == 'ls'):
		print(cmd("ls --color=always " + dirpath + "/"))
	else:
		print(cmd("ls -ltrh --color=always " + dirpath + "/"))

