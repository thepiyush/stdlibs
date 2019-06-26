;
; File name: template.il
;
; Author: Piyush
;
; Description: Frequently used functions template
; 		Eg usages:
; 			load("/.../template.il")
; 			template("lib1" "block1" "/.../inputfile")
; 
; Chanage log:
; 2019/06/23 : Initial version. (Piyush)
;

procedure( template(lib block inputfile @optional ( askuser "" ) )
	let( (terms cmd pyipc bbX bbY)
		abstract = dbOpenCellViewByType(lib block "abstract" "" "r")
		if(abstract then
			scriptname = #.get_filename(piport)
			;Get list & sort it
			excludeNetNames = nil ;append(append(append(GetSupplyNames() GetGroundNames()) GetClockNames()) nil)
			terms = setof(trm abstract~>terminals if(member(trm~>name excludeNetNames) nil t)) ;(trm~>net~>sigType == "signal")
			terms = sort(terms lambda((a b) if((car(parseString(car(a~>pins~>term~>name) "<>"))!=car(parseString(car(b~>pins~>term~>name) "<>")) \
								|| length(parseString(car(a~>pins~>term~>name) "<>"))<2 || length(parseString(car(b~>pins~>term~>name) "<>"))<2) \
					alphalessp(car(parseString(car(a~>pins~>term~>name) "<>")) car(parseString(car(b~>pins~>term~>name) "<>"))) \
					lessp(aelNumber(cadr(parseString(car(a~>pins~>term~>name) "<>"))) aelNumber(cadr(parseString(car(b~>pins~>term~>name) "<>"))))))) ;natural sort
			;Create temp file
			tmpfile_io = makeTempFileName(strcat(getTempDir() "/ipc_io"))
			;##Update it...
			sprintf(bbX "%.3f"  caadr(abstract~>prBoundary~>bBox))
			sprintf(bbY "%.3f" cadadr(abstract~>prBoundary~>bBox))
			f = outfile(tmpfile_io "w")
			foreach(term terms
				fprintf(f "name: \"%s\" tech: \"%s\"\n" car(term~>pins~>term~>name) case(getShellEnvVar("USER") ("t1" "1") ("t2" "2") (t "0")))
			)
			close(f)
			if(!isFile(tmpfile_io) then 
				printf("Tmp file could not created!!")
			else
				printf("Tmp file created.")
			)
			;Call python script to update tmpfile_io in background
			cmd = strcat("python " substring(scriptname 1 length(scriptname)-2) "py -p '" inputfile \
					"' -i '" tmpfile_io "' -o '" tmpfile_io "' -t " getShellEnvVar("USER"))
			if(fileLength(tmpfile_io)!=0 then
				if(fileLength(inputfile)!=0 then
					if((askuser != "") then 
						printf("\nCommand: %s\npath of inputfile : %s\nEnter \"y\" ('y' with double quotes) to run above command:\n" cmd inputfile)
						askuser = if(enterString(?prompts list("do this"))=="y" "" "no")
					)
					if((askuser == "") then
						pyipc = ipcBeginProcess(cmd "" 'ipc_dataHandler 'ipc_errHandler 'ipc_postFunc)
						printf("\nStarted command execution: %s\n at %s with %L \nPlease wait ...\n" cmd getCurrentTime() pyipc)
					else
						delete_tmpfiles()
						printf("\nWARNING: Run aborted by user input at %s\n" getCurrentTime())
					)
				else
					delete_tmpfiles()
					printf("\nERROR: It could not find any data in inputfile: '%s' \n" inputfile)
				)
			else
				delete_tmpfiles()
				printf("\nERROR: It could not find any signal shape in abstract for lib: '%s' & block: '%s' \n" lib block)
			)
		else
			printf("\nERROR: It could not find abstract for lib: '%s' & block: '%s' \n" lib block)
		)
	)
)
procedure( delete_tmpfiles()
	foreach(file list(tmpfile_io)
		if(file then
			if(isFile(file) then
				deleteFile(file)
				unless(isFile(file) printf("A temporary file has been deleted:'%s'\n" file))
			)
		)
	)
)
procedure( unique(lst)
	let(((uniq makeTable('uniq)))
		foreach(elem lst
			uniq[elem]=t
		)
		uniq->?
	)
)
procedure( ipc_dataHandler(pyipc data)
	printf("%s" data)
)
procedure( ipc_errHandler(pyipc data)
	printf("ERROR: %s\n" data)
)
procedure( ipc_postFunc(pyipc data)
	let((exitStatus)
		exitStatus = ipcGetExitStatus(pyipc)
		if(exitStatus==0 then
			printf("\n")
			;##Read data from tmpfile_io file to update cellview
			dbSave(abstract)
			dbClose(abstract)
			delete_tmpfiles()
			printf("\nFinished successfully at %s: %L %L, Return code = %L \n\n" getCurrentTime() pyipc data exitStatus)
		else
			printf("\nERROR: Finished Unsuccessfully at %s: %L %L, Return code = %L \n\n" getCurrentTime() pyipc data exitStatus)
		)
	)
)
