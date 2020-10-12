# stdlibs
Frequently used commands/functions/info

### Git commands:
```
git status
git pull                                     #To fetch latest update from git repo
git add <file>                               #This added    file will be pushed  into git
git rm <file>                                #This removed  file will be removed from git
git commit -m "<msg_for_what_has_changed>"   #To commit the changes and add combine message
git push        #OR git push origin master   #To push commited data into git repo
git checkout <file>                          #To discard changes in working directory
git merge --abort                            #To undo a merge
git reset --soft HEAD~1                      #To undo local 1commit, No change in local files and No change in the index
git reset HEAD~1                             #To undo local 1commit, No change in local files and    change in the index
git reset --merge HEAD~1                     #To undo local 1commit,    change in local files and    change in the index.         Update local files which are different between current HEAD and commit, but keep files which have changes which have not been added. If these files has unstaged changes, reset is aborted.
git reset --keep HEAD~1                      #To undo local 1commit,    change in local files and    change in the index entries. Update local files which are different between current HEAD and commit. If these files has local changes, reset is aborted.
git reset --hard HEAD~1                      #To undo local 1commit,    change in local files and    change in the index. Will lose all changes. Avoid this.
```
