import os, sys, getopt
from eos_utils.EOSSafeUtils import *  # <--> file from "/uscms_data/d3/varun/EOSSafeUtils.py"

###Syntax:
#          CheckErrors.py /uscms_data/d3/path/to/logs/nominal/ --verbose 1 (prints) --resubmit 1 (if you want to resubmit) --resub_num -1 (resubmits all the fails it looks for)
#

dir = sys.argv[1]

print; print 'Checking', dir

try:
    opts, args = getopt.getopt(sys.argv[2:], "", ["verbose=", "resubmit=", "resub_num="])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(1)
    
verbose_level = 0
resubmit = '0'
resub_num = -2
doNoLog = False

for o, a in opts:
	print o, a
	if o == '--verbose': verbose_level = int(a)
	if o == '--resubmit': resubmit = a
	if o == '--resub_num': resub_num = int(a)

rootdir = '/store/group/lpcljm/'+dir.split('/')[-2]+'/'
rootdir = rootdir.replace('_logs','')
print 'checking ROOT files in:',rootdir
folders = [x for x in os.walk(dir).next()[1]]

def checkLogFile(dir,folder,file):

	current = open(dir + '/'+folder+'/'+file.replace('.py','.condor.log'),'r')

	sysrem = False
	overmem = False
	killed = False
	normterm = False

	sysrem_index = 0
	overmem_index = 0
	kill_index = 0
	normterm_index = 0

	iline = 0
	for line in current:
		if 'SYSTEM_PERIODIC_REMOVE' in line: 
			if 'memory' in line:
				overmem = True
				overmem_index = iline
			else:
				sysrem = True
				sysrem_index = iline						
		elif 'condor_rm' in line: 
			killed = True
			kill_index = iline
		elif 'Normal termination (return value 0)' in line: 
			normterm = True
			normterm_index = iline
		iline += 1
	
	loginfo={}
	loginfo['sysrem']={}
	loginfo['overmem']={}
	loginfo['killed']={}
	loginfo['normterm']={}

	loginfo['sysrem']['flag']=sysrem
	loginfo['sysrem']['index']=sysrem_index

	loginfo['overmem']['flag']=overmem
	loginfo['overmem']['index']=overmem_index

	loginfo['killed']['flag']=killed
	loginfo['killed']['index']=kill_index

	loginfo['normterm']['flag']=normterm
	loginfo['normterm']['index']=normterm_index
	
	return loginfo

total_total = 0
total_succeeded = 0
total_error = 0
total_running = 0
total_roots = 0

no_log = 0
empty_log = 0
err_fail = 0
copy_fail = 0
sysrem_fail = 0
mem_fail = 0 ; mem_fail_dict = {}
kill_fail = 0
All_cuts = 0

root_not_found = {}

for folder in folders:
	if 'DY' in folder: continue
# 	if 'MuonEG_RRC' not in folder: continue
#	if 'ZZ' not in folder: continue
# 	if 'Mu' not in folder and 'EG' not in folder: continue
	if verbose_level > 0:  
		print
		print folder
        rootfiles = EOSlist_root_files(rootdir+folder)
        total_roots += len(rootfiles)
        
        mem_fail_dict[folder] = [] #initialize list, for saving memory failed jobs
        root_not_found[folder] = [] #initialize list, for finished jobs with no root files


	files = [x for x in os.listdir(dir+'/'+folder) if ('.py' in x) and ('producer' not in x)]
	
	os.listdir(dir+'/'+folder)
	
	resub_index = []
	count_total = 0
	for file in files:
		#print file
		total_total+=1
		index = file[file.find('_')+1:file.find('.')]
		if '_' in index: index = index.split('_')[-1]
		count_total += 1
	
		#Check if stdout exists
		if (os.path.exists(dir+'/'+folder+'/'+file.replace('.py','.stdout'))==False):
	
			print '\tNO STDOUT:',file.replace('.py','.stdout'),' and JobIndex:',index
			no_log += 1
			#if resub_num == -1 or resub_num == 1: resub_index.append(index)

			#Check why does it not have stdout?
			try:
					
				#check log
				loginfo = checkLogFile(dir,folder,file)
										
				if loginfo['sysrem']['flag'] and loginfo['sysrem']['index'] > loginfo['normterm']['index']: 
					if verbose_level > 0: 
						print '\t\tSYSTEM REMOVE FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
					sysrem_fail+=1
					if resub_num == -1 or resub_num == 5:resub_index.append(index)
					continue

				if loginfo['overmem']['flag'] and loginfo['overmem']['index'] > loginfo['normterm']['index']: 
					if verbose_level > 0: 
						print '\t\tMEM FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
					mem_fail+=1
					if resub_num == -1 or resub_num == 3:resub_index.append(index)
					mem_fail_dict[folder].append(index)
					continue

				if loginfo['killed']['flag'] and loginfo['killed']['index'] > loginfo['normterm']['index']: 
					if verbose_level > 0: 
						print '\t\tKILL_FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
					kill_fail+=1
					if resub_num == -1 or resub_num == 4:resub_index.append(index)
					continue

			except:
				pass
			
		#if stdout exists
		else:
			current = open(dir + '/'+folder+'/'+file.replace('.py','.stdout'),'r')
			good = False
			for line in current:
				if 'All cuts' in line: 
					good = True
					All_cuts +=1
					break
				
			#check if 'All cuts' exists
			if good:
				#check if root file exists:
				if file.replace('.py','.root') not in rootfiles:
					print "\tROOT file does not exist for JobIndex:", index,'!!'
					root_not_found[folder].append(index)

					#check why doesn't root file exist?
					stderr_ = open(dir + '/'+folder+'/'+file.replace('.py','.stderr'),'r')
					for l in stderr_:
						if 'Error' in l or 'error' in l or 'ERROR' in l:
							if verbose_level > 0: 
								print '\t\t"Error" in STDERR:',file.replace('.py','.stderr'),' and JobIndex:',index
							err_fail+=1
							break
					stderr_.close()

					if resub_num == -1 or resub_num == 0:resub_index.append(index)

				#check if log is good :
				try:
					loginfo = checkLogFile(dir,folder,file)
										
					if loginfo['sysrem']['flag'] and loginfo['sysrem']['index'] > loginfo['normterm']['index']: 
						if verbose_level > 0: 
							print '\tSYSTEM REMOVE FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
						sysrem_fail+=1
						if resub_num == -1 or resub_num == 5:resub_index.append(index)
						continue

					if loginfo['overmem']['flag'] and loginfo['overmem']['index'] > loginfo['normterm']['index']: 
						if verbose_level > 0: 
							print '\tMEM FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
						mem_fail+=1
						if resub_num == -1 or resub_num == 3:resub_index.append(index)
						mem_fail_dict[folder].append(index)
						continue

					if loginfo['killed']['flag'] and loginfo['killed']['index'] > loginfo['normterm']['index']: 
						if verbose_level > 0: 
							print '\tKILL_FAIL:',file.replace('.py','.condor.log'),' and JobIndex:',index
						kill_fail+=1
						if resub_num == -1 or resub_num == 4:resub_index.append(index)
						continue
				except:
					print "problem getting condor.log file."
					pass
						

			#Check why does it not have "All Cuts" in stdout?
			else: 
				if verbose_level > 0: 
					print '\tNO "All Cuts" in STDOUT:',file.replace('.py','.stdout'),' and JobIndex:',index
					empty_log+=1

					try:
						current = open(dir + '/'+folder+'/'+file.replace('.py','.stderr'),'r')
						good = True
						for line in current:
							if 'Error' in line: good = False
						if not good: 
							if verbose_level > 0: 
								print '\t\t"Error" in STDERR:',file.replace('.py','.stderr'),' and JobIndex:',index
							err_fail+=1
					except:
						pass

					if resub_num == -1 or resub_num == 0:resub_index.append(index)

					continue
# 		except:
# 			pass
# 
# 		try:
			current = open(dir + '/'+folder+'/'+file.replace('.py','.stderr'),'r')
			good = True
			for line in current:
				if 'failure' in line: good = False
			if not good: 
				if verbose_level > 0: 
					print '\t"failure" in STDERR:',file.replace('.py','.stderr'),' and JobIndex:',index
				copy_fail+=1
				if resub_num == -1 or resub_num == 2:resub_index.append(index)
				continue
# 		except:
# 			pass

		
	if resub_index != []: 
		#Remove duplicated in resub_index
		resub_index= list(set(resub_index)) #this makes the list unordered but it doesn matter.
		print 'RESUBS:', resub_index 

	if resubmit != '1': continue


	indexind = 0
	for index in resub_index:
		os.chdir(dir + '/' + folder)

		os.system('rm -v ' + dir + '/' + folder + '/' + folder + '_' + index + '.condor.log')
		try:
			os.system('rm -v ' + dir + '/' + folder + '/' + folder + '_' + index + '.stdout')
			os.system('rm -v ' + dir + '/' + folder + '/' + folder + '_' + index + '.stderr')
		except:
			pass
		os.system('condor_submit ' + dir + '/' + folder + '/' + folder + '_' + index + '.condor')

		indexind+=1
	
print	
print '=' * 50
print
print 'TOTAL JOBS: ', total_total
print
print 'ROOT files found:', total_roots
print '\tSTDOUT prints "All Cuts":', All_cuts
print '\tSTDOUT prints no "All Cuts":', empty_log
print '\t\t"Error" in STDERR:', err_fail
#print 'DONE:', total_total - no_log - empty_log - copy_fail - mem_fail - kill_fail
print
print 'NO STDOUT:', no_log
print '\tMEMORY FAIL:', mem_fail
# for sample in mem_fail_dict:
# 	if mem_fail_dict[sample]==[]: continue
# 	print '\t\t ',sample, mem_fail_dict[sample]
print '\tKILL_FAIL:', kill_fail
print '\tProbably still running:', no_log - mem_fail - kill_fail
print
print '"failure" in STDERR:', copy_fail
print
print 'DONE (TOTAL JOBS - NO STDOUT - NO "All Cuts" - "failure" FAILS):', total_total - no_log - empty_log - copy_fail
print
print '( "All Cuts" + NO "All Cuts" + NO STDOUT + "failure" FAILS):', All_cuts + no_log + empty_log + copy_fail
print

