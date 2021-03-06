#!/usr/bin/python
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
import shutil

def userinput(usermsg):
	"""Return user input for given message"""
	if(sys.version_info.major == 2):
		inputstr = raw_input(usermsg)
	else:
		inputstr = input(usermsg)
	return inputstr

def userexit(status = 'ask',errormsg = ''):
	"""Confirmation with user before termination of script"""
	if(status == 'ask'):
		if(errormsg):
			print(errormsg)
		allow = userinput("Press \"y\" to continue or other character to terminate script :")
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
		idx = userinput("To select one element from above list, Please Enter Sequence Number :")
		if(idx.isdigit() and 0<(int(idx))<=len(datalist)):
			break
		else:
			if(idx.isdigit() and int(idx)==0):
				userexit('exit',"User Exit.")
			print("\nInvalid Sequence Number. Please Enter valid Sequence Number." if(idx.isdigit())else "\nInvalid user input. Please Enter Numbers only.")
	return int(idx)-1

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

def return2shell(cmdstr, file2shell):
	"""Write/Print shell command and return to parent script"""
	if(isfilepath(file2shell)):
		makefile(file2shell,[cmdstr])
	else:
		print("@shell>" + cmdstr)
	sys.exit(10)

def get_environ(envvar):
	"""Return value of environment variable"""
	envvarvalue = os.getenv(envvar) #to get start-up envvar: os.environ.get(envvar)
	if(envvarvalue == None):
		userexit('exit',"'" + envvar + "' environment variable is NOT defined. Please define it and re-run.")
	return envvarvalue

def get_pwd():
	"""Get present working directory"""
	return os.getcwd() #will return dereferenced symbolic link
	#return os.getenv('PWD') #will return referenced symbolic link for linux

def get_expandedpath(path):
	"""Return 'home director' and 'environment variables' expanded path"""
	return os.path.expandvars(os.path.expanduser(path))

def get_realpath(path):
	"""Return expanded path with derefences symbolic links"""
	return os.path.realpath(get_expandedpath(path))

def issamepath(dirpath1,dirpath2):
	"""Return True if dirpath1 and dirpath2 are same."""
	return (os.path.realpath(get_expandedpath(dirpath1)) == os.path.realpath(get_expandedpath(dirpath2)))

def isdirpath(dirpath):
	"""Return True if dirpath exist else False"""
	return os.path.isdir(get_expandedpath(dirpath))

def isfilepath(filepath):
	"""Return True if filepath exists else False"""
	return os.path.isfile(get_expandedpath(filepath))

def islinkpath(linkpath):
	"""Return True if linkpath exists else False"""
	return os.path.islink(get_expandedpath(linkpath))

def ispathexists(path):
	"""Return True if path exists else False"""
	return os.path.exists(get_expandedpath(path))

def deletepath(path):
	"""Delete directory/file if exists"""
	if(ispathexists(path)):
		if(isfilepath(path) or islinkpath(path)):
			os.remove(get_expandedpath(path))
			if(not ispathexists(path)):
				print("\'" + path + "\' file has been deleted.")
		elif(isdirpath(path)):
			shutil.rmtree(get_expandedpath(path))
			if(not ispathexists(path)):
				print("\'" + path + "\' directory has been deleted.")
		else:
			userexit('exit',"\'" + path + "\' is not a directory or file.")
	if(ispathexists(path)):
		userexit('exit',"\'" + path + "\' path cannot be deleted.")

def linkpath(sourcepath,destinationpath):
	"""Delete existing directory/file and Link destination directory/file to source directory/file"""
	deletepath(destinationpath)
	if(isfilepath(sourcepath)):
		if(os.name == 'nt' and sys.version_info.major != 2):
			os.symlink(get_expandedpath(sourcepath),get_expandedpath(destinationpath),target_is_directory=False)
		else:
			os.symlink(get_expandedpath(sourcepath),get_expandedpath(destinationpath))
		if(islinkpath(destinationpath)):
			print("\'" + destinationpath + "\' file has been linked to \'" + sourcepath + "\'")
	elif(isdirpath(sourcepath)):
		if(os.name == 'nt' and sys.version_info.major != 2):
			os.symlink(get_expandedpath(sourcepath),get_expandedpath(destinationpath),target_is_directory=True)
		else:
			os.symlink(get_expandedpath(sourcepath),get_expandedpath(destinationpath))
		if(islinkpath(destinationpath)):
			print("\'" + destinationpath + "\' directory has been linked to \'" + sourcepath + "\'")
	else:
		userexit('exit',"\'" + sourcepath + "\' is not a directory or file.")
	if(not islinkpath(destinationpath)):
		userexit('exit',"\'" + destinationpath + "\' path cannot be linked to \'" + sourcepath + "\'")

def copypath(sourcepath,destinationpath):
	"""Delete existing directory/file and Copy source directory/file to destination directory/file"""
	deletepath(destinationpath)
	if(islinkpath(sourcepath)):
		linkpath(get_realpath(sourcepath),destinationpath)
	elif(isdirpath(sourcepath)):
		shutil.copytree(get_expandedpath(sourcepath),get_expandedpath(destinationpath),symlinks=True) #Symbolic links will be copy as a links (not cotent)
		if(isdirpath(destinationpath)):
			print("\'" + destinationpath + "\' directory has been copied from \'" + sourcepath + "\'")
	elif(isfilepath(sourcepath)):
		shutil.copy2(get_expandedpath(sourcepath),get_expandedpath(destinationpath))
		if(isfilepath(destinationpath)):
			print("\'" + destinationpath + "\' file has been copied from \'" + sourcepath + "\'")
	else:
		userexit('exit',"\'" + sourcepath + "\' is not a directory or file.")
	if(not ispathexists(destinationpath)):
		userexit('exit',"\'" + destinationpath + "\' path cannot be copied from \'" + sourcepath + "\'")

def makedir(dirpath):
	"""Delete existing directory and Make/Create new all director(ies) (including intermediate levels)"""
	deletepath(dirpath)
	os.makedirs(get_expandedpath(dirpath))
	if(isdirpath(dirpath)):
		print("\'" + dirpath + "\' directory has been created.")
	else:
		userexit('exit',"\'" + dirpath + "\' directory cannot be created.")

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

def get_matchindices(filedata,pattern):
	"""Return match indices in file/filelist (format:[[[line number, start of match, end of match],...],[...],...])"""
	lineno = 0
	if type(pattern) is str:
		pl = [re.compile(pattern)]
	elif type(pattern) is list:
		pl = [re.compile(p) for p in pattern]
	else:
		userexit('exit',"Unsupported 'type' of object pattern:\'" + pattern + "\'.")
	matchindices = [[] for i in range(len(pl))]
	if type(filedata) is str:
		filepath = get_expandedpath(filedata)
		if(not isfilepath(filepath)):
			userexit('exit',"\'" + filepath + "\' file does not exist.\n")
		try:
			with open(filepath, 'r') as f:
				for line in f:
					for i,p in enumerate(pl):
						for m in p.finditer(line):
							matchindices[i].append([lineno]+list(m.span()))
					lineno = lineno + 1
		except:
			userexit('exit',"\'" + filepath + "\' file cannot open in readmode.")
	elif type(filedata) is list:
		for line in filedata:
			for i,p in enumerate(pl):
				for m in p.finditer(line):
					matchindices[i].append([lineno]+list(m.span()))
			lineno = lineno + 1
	else:
		userexit('exit',"Unsupported 'type' of object 'file':\'" + filedata + "\'.")
	return matchindices if(type(pattern) is list) else matchindices[0]

def get_matchsections(filepath,startpattern,endpattern):
	"""Return start and end line numbers of match section in file"""
	matchsections = []
	matchlines = get_matchindices(filepath,[startpattern,endpattern])
	matchlinesstart = get_unique_list([i[0] for i in matchlines[0]])
	matchlinesend = get_unique_list([i[0] for i in matchlines[1]])
	for matchstart in matchlinesstart:
		matchend = next((x for x in matchlinesend if x>matchstart), -1)
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

def get_dir_relevanceindex(dirpath,matchparameters):
	"""Return most relevance (row) index of match parameters(=[[p11,p12,...][p21,p22,...][...]) for given dirpath"""
	parameter_matching_weight = [0]*len(matchparameters)
	for idx,row in enumerate(matchparameters):
		for p in row:
			if(p in dirpath):
				parameter_matching_weight[idx] += (1+(len(p)/float(len(dirpath))))
	return parameter_matching_weight.index(max(parameter_matching_weight)),max(parameter_matching_weight)

def get_dirs_updated(dirpath,matchparameters,setparameters):
	"""Return updated dirpath(s) for given set parameters(=[[p11,p12,...][p21,p22,...][...]) accordingly to match parameters relevance"""
	matched_parameters_index,matched_parameters_value = get_dir_relevanceindex(dirpath,matchparameters)
	matched_parameters = matchparameters[matched_parameters_index]
	updated_dirpathlist = []
	if(matched_parameters_value > 0):
		for row in setparameters:
			updated_dirpath = dirpath
			for idx,p in enumerate(row):
				updated_dirpath = updated_dirpath.replace(matched_parameters[idx],p)
				if(dirpath!=updated_dirpath and ispathexists(updated_dirpath)):
					break
			updated_dirpathlist.append(updated_dirpath)
	return [d for d in get_unique_list(updated_dirpathlist) if(dirpath!=d)]

def get_datetime_str():
	"""Return current data and time string"""
	return time.strftime("%Y%m%d%H%M%S")

def get_unique_list(normal_list):
	"""Return list with deleted duplicate elements"""
	unique_list = []
	[unique_list.append(l) for l in normal_list if not unique_list.count(l)]
	return unique_list

def get_indented_list(normal_list,noofcolumn,tabsize=8):
	"""Return list with Added Tab(s)('\t') to the elements of list to indent columns"""
	maxcolumnlenlist = [(tabsize*(1 + (len(max(normal_list[r::noofcolumn],key=len))/tabsize))) for r in range(noofcolumn)]
	indentedlist = []
	for index,value in enumerate(normal_list):
		indentedlist.append(value + ('\n' if(not ((index+1)%noofcolumn))else "".join((1 + (((maxcolumnlenlist[index%noofcolumn]-len(value))-1)/tabsize))*['\t'])))
	return indentedlist

def isfullmatch(pattern,string):
	"""Return True if (compiled)pattern match to string from start to end"""
	s = pattern.search(string)
	return ((s.start() == 0 and s.end() == len(string)) if s else False)

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

def get_natural_nearest_match(words,possibilities,dummychar='.'):
	"""Find 'natural' nearest matching pairs for 'words' list from 'possibilities' list"""
	if words and possibilities:
		get_chr = lambda wrd,dc=dummychar: ("".join((dc if(c in '0123456789')else  c ) for c in wrd))
		get_num = lambda wrd             : ("".join(( c if(c in '0123456789')else '0') for c in wrd))
		dict = {}
		for psb in possibilities:
			dict.setdefault(get_chr(psb),{})[get_num(psb)] = psb
		nwords = []
		for wrd in ([words] if(type(words) is str)else words):
			nwrd = difflib.get_close_matches(get_chr(wrd),dict.keys(),1,0)[0]
			nwords.append(dict[nwrd][min(dict[nwrd].keys(), key=lambda x:abs(int(x)-int(get_num(wrd))))])
		return (nwords[0] if(type(words) is str)else nwords)
	else:
		return ('' if(type(words) is str)else [])

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
		sequencelist = list(map(str,range(1,1+len(datalist))))
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

def openpath(pathmatrix,editor='',argstr='',filestr='',lsltrpickup=0,file2shell='',askpathcount=10):
	"""Open file or dir path with given constraint like editor,argstr,filestr,lsltrpickup,etc."""
	editor = get_commandname(editor,'command','editor') if(type(editor) is str)else get_commandname(*editor)
	lsltrpickup = (int(lsltrpickup) if(lsltrpickup.isdigit())else 0) if(type(lsltrpickup) is str)else lsltrpickup
	pathlist = get_pathlist(pathmatrix,'dir' if(editor in ['cd','cdls','cdlsltr','ls','lsltr'])else 'file',filestr,lsltrpickup)
	pathliststr = (" ".join(pathlist)).strip()
	if(len(pathlist) > int(askpathcount) and editor not in ['ls','lsltr','grep']):
		userexit('ask',"This command will open " + str(len(pathlist)) + (" directories(terminals)." if(editor in ['cd','cdls','cdlsltr'])else " files(editors)."))
	if(pathliststr):
		#Editors
		if(editor == 'gvim'):
			os.system("gvim -p " + ((" -c \"/" + argstr + "\" ") if(argstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'gvimr'):
			os.system("gvim -pR " + ((" -c \"/" + argstr + "\" ") if(argstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'emacs'):
			for fpl in pathlist:
				os.system("emacs " + argstr + " " + fpl + " &")
				print("Opened " + editor + " with file: " + fpl)
		elif(editor == 'emacsr'):
			for fpl in pathlist:
				os.system("emacs " + argstr + " " + fpl + " --eval \'(setq buffer-read-only t)\' &")
				print("Opened " + editor + " with file: " + fpl)
		elif(editor == 'kate'):
			os.system("kate -u " + argstr + " " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'gedit'):
			os.system("gedit " + argstr + " " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'nedit'):
			os.system("nedit " + argstr + " " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		#Diff Editors
		elif(editor == 'gvimdiff'):
			os.system("gvimdiff " + ((" -c \"/" + argstr + "\" ") if(argstr != '')else "") + pathliststr + " &")
			print("Opened " + editor + " with files: " + pathliststr)
		elif(editor == 'tkdiff'):
			os.system("tkdiff " + argstr + " " + pathliststr + " &")
			print("Opened " + editor + " with files: " + pathliststr)
		#Image Viewer
		elif(editor == 'eog'):
			os.system("eog -n " + argstr + " " + pathliststr + " &")
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
		elif(editor == 'display'):
			for fpl in pathlist:
				os.system("display " + argstr + " " + fpl + " &")
				print("Opened " + editor + " with file: " + fpl)
		#Commands
		elif(editor == 'cd' or editor == 'cdls' or editor == 'cdlsltr'):
			for i,d in enumerate(pathlist):
				if(file2shell != '' and (i == 0 and len(pathlist) == 1 and d != get_pwd())):
					if(editor == 'cd'):
						return2shell("cd " + d, file2shell)
					elif(editor == 'cdls'):
						return2shell("cd " + d + " && ls --color=always " + argstr + " " + filestr, file2shell)
					else:
						return2shell("cd " + d + " && ls -ltrh --color=always " + argstr + " " + filestr, file2shell)
				else:
					if(editor == 'cd'):
						os.system("gnome-terminal --window --maximize --working-directory=\"" + d + "\"")
					elif(editor == 'cdls'):
						os.system("gnome-terminal --window --maximize --working-directory=\"" + d + "\" -e \"ksh -c 'ls --color=always "+argstr+" "+filestr+"';ksh\"")
					else:
						os.system("gnome-terminal --window --maximize --working-directory=\"" + d + "\" -e \"ksh -c 'ls -ltrh --color=always "+argstr+" "+filestr+"';ksh\"")
					print("Opened gnome-terminal with dir: " + d)
		elif(editor == 'ls'):
			print("ls --color=always " + argstr + " " + (" ".join([d + "/" + filestr for d in pathlist])) + " :")
			os.system("ls --color=always " + argstr + " " + (" ".join([d + "/" + filestr for d in pathlist])))
		elif(editor == 'lsltr'):
			print("ls -ltrh --color=always " + argstr + " " + (" ".join([d + "/" + filestr for d in pathlist])) + " :")
			os.system("ls -ltrh --color=always " + argstr + " " + (" ".join([d + "/" + filestr for d in pathlist])))
		elif(editor == 'cat'):
				print("cat " + argstr + " " + pathliststr + " :")
				os.system("cat " + argstr + " " + pathliststr)
				print("")
		elif(editor == 'grep'):
			if(argstr != ''):
				print("zgrep --color=always " + argstr + " " + pathliststr + " :")
				os.system("zgrep --color=always " + argstr + " " + pathliststr)
			else:
				print(" ".join(pathlist) + "\nEnter one more argument for 'PATTERN' to 'grep' in file(s).")
		elif(editor == 'awk'):
			if(argstr != ''):
				print("awk " + argstr + " " + pathliststr + " :")
				os.system("awk " + argstr + " " + pathliststr)
			else:
				print(" ".join(pathlist) + "\nEnter one more argument for 'PATTERN'/'ACTION' to 'awk' in file(s).")
		#Default
		else:
			os.system("gvim -p " + ((" -c \"/" + argstr + "\" ") if(argstr != '')else "") + pathliststr)
			print("Opened " + editor + " with file: " + ("\nOpened " + editor + " with file: ").join(pathlist))
