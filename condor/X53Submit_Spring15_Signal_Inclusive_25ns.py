#!/usr/bin/python

import os
import re
import fileinput

files_per_job = 1

rel_base = os.environ['CMSSW_BASE']
cmssw = 'CMSSW_7_6_3_patch2'
logdir = 'Feb20'
outdir = '/eos/uscms/store/user/lpctlbsm/clint/Spring15/25ns/'+logdir+'/'

### What is the name of your FWLite Analyzer
FWLiteAnalyzer = 'ljmet'

### Which Systematics to do
DONOMINAL = 'True'
DOJES = 'False'
DOJER = 'False'
DOBTAG = 'False'
DOQCDMC = 'False'
DOTTBARSYS = 'False'

### JSON file to use
MYJSON = "''"

### Systematics flags
BTAGUNCERTUP = 'False'
BTAGUNCERTDOWN = 'False'
JECUNCERTUP = 'False'
JECUNCERTDOWN = 'False'
JERUNCERTUP = 'False'
JERUNCERTDOWN = 'False'


#################################################
### Names to give to your output root files
#################################################

prefix = []

if DONOMINAL=='True':
    prefix.extend([
            'X53X53_LH_700',
#            'X53X53_RH_700',
#            'X53X53_LH_800',
#            'X53X53_RH_800',
#            'X53X53_LH_900',
#            'X53X53_RH_900',
#            'X53X53_LH_1000',
#            'X53X53_RH_1000',
#            'X53X53_LH_1100',
#            'X53X53_RH_1100',
#            'X53X53_LH_1200',
#            'X53X53_RH_1200',
#            'X53X53_LH_1300',
#            'X53X53_RH_1300',
#            'X53X53_LH_1400',
#            'X53X53_RH_1400',
#            'X53X53_LH_1500',
#            'X53X53_RH_1500',
#            'X53X53_LH_1600',
#            'X53X53_RH_1600',
    ])


###########################################
### Where to save your output root files to
###########################################
dir = []
for i in prefix:
    outdiri = outdir+i
    dir.extend([outdiri])

################################################
### Where is your list of root files to run over
################################################
list = [] 

listnom = [
'Samples_Spring15MC/X53X53_M-700_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2.txt',
#'Samples_Spring15MC/X53X53_M-700_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-900_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2.txt',
#'Samples_Spring15MC/X53X53_M-900_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1100_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1100_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1300_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1300_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1500_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1500_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
#'Samples_Spring15MC/X53X53_M-1600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1.txt',
    ]

if DONOMINAL=='True':
    list.extend(listnom)
   

for i in range(len(prefix)):
    print i,' ',prefix[i],' ',dir[i],' ',list[i]

### Write the files you wish to run over for each job    
def get_input(num, list):
    result = '' 
    file_list = open(rel_base+"/src/LJMet/Com/python/"+list)
    file_count = 0
    for line in file_list:
        if line.find('root')>0:
            file_count=file_count+1
            if file_count>(num-1) and file_count<(num+files_per_job):
                f_name=line.split('.root')[0]
                f_name=f_name+'.root'
                #result=result+'                 \'' + f_name.group(1)+'\',\n'
                #result=result+'                 \'dcap:///pnfs/cms/WAX/11' + f_name.group(1)+'\',\n'
                result=result+'                 \'root://cmsxrootd.fnal.gov/' + f_name +'\',\n'
    file_list.close()
    #result = result + '                 )\n'
    return result


print str(files_per_job)+' files per job...'

#make tarball and move to eos
os.system('tar -cvf ljmet.tar ../bin/* ../src/* ../interface/* ../data/* ../python/* ../tools/* ../BuildFile.xml ../setup.sh')
os.system('xrdcp -f ljmet.tar root://cmseos.fnal.gov//store/user/clint/ljmet.tar')

for i in range(len(prefix)):

    j = 1
    nfiles = 1

    #make local directory
    locdir = logdir+'/'+prefix[i]
    os.system('mkdir -p  %s' %locdir)

        
    FLAGTAG = 'TriggerResults::PAT'
    
    print 'CONDOR work dir: '+dir[i]
    #os.system('rm -rf '+dir[i])
    #os.system('mkdir -p '+dir[i])

    file_list = open(rel_base+"/src/LJMet/Com/python/"+list[i])
    count = 0
    for line in file_list:
        if line.find('root')>0:
            count = count + 1
    file_list.close()
    #count = count - 1

    print 'File prefix: '+prefix[i]
    print 'Number of input files: '+str(count)

    while ( nfiles <= count ):    

        py_templ_file = open(rel_base+"/src/LJMet/Com/condor/Dilepton_Spring15MC_25ns_python.templ")
        condor_templ_file = open(rel_base+"/src/LJMet/Com/condor/X53condor.templ")
        csh_templ_file    = open(rel_base+"/src/LJMet/Com/condor/X53csh.templ")

        #open local version of file
        localfile=locdir+'/'+prefix[i]+"_"+str(j)+".py"
        py_file = open(localfile,"w")
        for line in py_templ_file:
            line=line.replace('DIRECTORY',dir[i])
            line=line.replace('PREFIX',prefix[i])
            line=line.replace('JOBID',str(j))
            line=line.replace('INFILES',get_input(nfiles, list[i]))
            line=line.replace('BTAGUNCERTUP',BTAGUNCERTUP)
            line=line.replace('BTAGUNCERTDOWN',BTAGUNCERTDOWN)
            line=line.replace('JECUNCERTUP',JECUNCERTUP)
            line=line.replace('JECUNCERTDOWN',JECUNCERTDOWN)
            line=line.replace('JERUNCERTUP',JERUNCERTUP)
            line=line.replace('JERUNCERTDOWN',JERUNCERTDOWN)
            line=line.replace('EVENTSTOPROCESS',str(-1))
            line=line.replace('FLAGTAG',FLAGTAG)
            line=line.replace('JSONFILE',MYJSON)
            py_file.write(line)
        py_file.close()

        #copy file to eos
        eosfile =   "root://cmseos.fnal.gov/"+dir[i]+"/"+prefix[i]+"_"+str(j)+".py"
        os.system("xrdcp -f %s %s"  % (localfile,eosfile))
        #remove local version
        os.system('rm %s' % localfile)

        localcondor = locdir+'/'+prefix[i]+"_"+str(j)+".condor"
        eoscondor = "root://cmseos.fnal.gov/"+dir[i]+"/"+prefix[i]+"_"+str(j)+".condor"
        condor_file = open(localcondor,"w")
        for line in condor_templ_file:
            line=line.replace('DIRECTORY',locdir)
            line=line.replace('PREFIX',prefix[i])
            line=line.replace('JOBID',str(j))
            condor_file.write(line)
        condor_file.close()

        #copy local to eos
        #os.system('xrdcp -f %s %s' % (localcondor,eoscondor))
        #remove local copy
        #os.system('rm %s' % localcondor)

        eoscsh="root://cmseos.fnal.gov/"+dir[i]+"/"+prefix[i]+"_"+str(j)+".csh"
        localcsh=locdir+'/'+prefix[i]+"_"+str(j)+".csh"
        eosoutput="root://cmseos.fnal.gov/"+dir[i]+"/"+prefix[i]+'_'+str(j)+'.root'
        locoutput = prefix[i]+'_'+str(j)+'.root'
        csh_file = open(localcsh,"w")
        for line in csh_templ_file:
            line=line.replace('CMSSWBASE',rel_base)
            line=line.replace('DIRECTORY',dir[i])
            line=line.replace('PREFIX',prefix[i])
            line=line.replace('JOBID',str(j))
            line=line.replace('CMSSWVERSION',cmssw)
            line=line.replace('FWLITEANALYZER',FWLiteAnalyzer)
            line=line.replace('EOSPY',eosfile)
            line=line.replace('LOCPY',localfile)
            line=line.replace('EOSOUT',eosoutput)
            line=line.replace('LOCOUT',locoutput)
            csh_file.write(line)
        csh_file.close()

        #os.system('xrdcp -f %s %s' % (localcsh,eoscsh))
        #os.system('rm %s' %localcsh)

        os.system('chmod u+x '+locdir+'/'+prefix[i]+'_'+str(j)+'.csh')
        print 'condor file is: '+locdir+'/'+prefix[i]+'_'+str(j)+'.condor;'
        os.system(' condor_submit %s' % localcondor)
        #os.system('cd '+dir[i]+'; condor_submit '+prefix[i]+'_'+str(j)+'.condor; cd -')
        j = j + 1
        nfiles = nfiles + files_per_job
        py_templ_file.close()
        condor_templ_file.close()
        csh_templ_file.close()

    #print  str(j-1)+' jobs submitted'
    
