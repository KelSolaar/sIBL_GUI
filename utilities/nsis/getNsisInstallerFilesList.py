"""
This script generates 2 lists of nsis commands (install & uninstall)for all files in a given directory.

Usage:
	getNsisInstallerFilesList.py <source directory> <installation list name> <uninstallation list name>
Where
	<Source Directory>	  : Source directory.
	<Installation List name>	: List of files to install. (NSIS syntax)
	<UnInstallation List name> : List of files to uninstall. (NSIS syntax)
"""

import sys, os, glob

# global settings
just_print_flag = 0 # turn to 1 for debugging

# templates for the output
inst_dir_tpl = ' SetOutPath "$instdir%s"'
inst_file_tpl = ' File "%s"'
uninst_file_tpl = ' Delete "$instdir%s"'
uninst_dir_tpl = ' RMDir "$instdir%s"'

# check args
if len(sys.argv) != 4:
	print __doc__
	sys.exit(1)
source_dir = sys.argv[1]
if not os.path.isdir(source_dir):
	print __doc__
	sys.exit(1)

def open_file_for_writting(filename):
	try:
		h = file(filename, "w")
	except:
		print "Problem opening file %s for writting!" % filename
		print __doc__
		sys.exit(1)
	return h

inst_list = sys.argv[2]
uninst_list = sys.argv[3]
if not just_print_flag:
	ih = open_file_for_writting(inst_list)
	uh = open_file_for_writting(uninst_list)

stack_of_visited = []
counter_files = 0
counter_dirs = 0

print "Generating install & uninstall list of files"
print " For directory", source_dir
print >> ih, " ; Files to install\n"
print >> uh, " ; Files and directories to remove\n"

def my_visitor(my_stack, cur_dir, files_and_dirs):
	global counter_dirs, counter_files, stack_of_visited
	counter_dirs += 1

	if just_print_flag:
		print "Here", my_dir
		return

	# first separate files
	my_files = [x for x in files_and_dirs if os.path.isfile(cur_dir + os.sep + x)]
	# and truncate dir name
	my_dir = cur_dir[len(source_dir):]
	#if my_dir == "": my_dir = "\\."

	# save it for uninstall
	stack_of_visited.append((my_files, my_dir))

	# build install list
	if len(my_files):
		print >> ih, inst_dir_tpl % (my_dir)
		for f in my_files:
			print >> ih, inst_file_tpl % (os.path.abspath(cur_dir) + os.sep + f)
			counter_files += 1
		print >> ih, " "

os.path.walk(source_dir, my_visitor, stack_of_visited)
ih.close()
print "Install list done!"
print " ", counter_files, "Files in", counter_dirs, "Directories"

stack_of_visited.reverse()
# Now build the uninstall list
for (my_files, my_dir) in stack_of_visited:
		for f in my_files:
			print >> uh, uninst_file_tpl % (my_dir + os.sep + f)
		if my_dir:
			print >> uh, uninst_dir_tpl % my_dir
			print >> uh, " "

print >> uh, " "
print >> uh, " RMDir /r \"$instdir\\support\\\""
print >> uh, " RMDir \"$instdir\\\""

# now close everything
uh.close()
print "Uninstall list done!\n"
