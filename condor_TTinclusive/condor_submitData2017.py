import os,sys,datetime

shift = sys.argv[1]

cernList=[

	# SHOULD BE AT CERN, USE eoscms.cern.ch in condor_submit.py
	# MOVE THINGS HERE TO REMIND YOURSELF WHAT IS AT CERN

	#### TTbar

	]

externalList = [
	# USE cmsxrootd.fnal.gov in condor_submit.py UNLESS YOU CHECK THE LIST LOG FOR CERN PRESENCE
	'SingleElectron_31Mar18.txt',
	'SingleMuon_31Mar18.txt'
]
	
print '====== LJMET SUBMISSION ======'
	
relBase = os.environ['CMSSW_BASE']
print 'Relbase:',relBase

thisDir = relBase+'/src/LJMet/Com/condor_TTinclusive/' 
tarfile = relBase+'.tar'
print 'Making tar:'
if os.path.exists(tarfile):
	print 'tar already exists! Will not re-tar!'
else: 
	os.chdir(relBase)
	# os.chdir('../')
	# YOU NEED TO EXCLUDE ANYTHING ELSE THAT MIGHT LIVE IN THE SAME CMSSW RELEASE, MY LIST IS SUPER LONG
	print 'tar --exclude=".SCRAM" --exclude="src/LJMet/Com/.git" --exclude="src/.git" --exclude="src/LJMet-Slimmer" --exclude="src/singleLepAnalyzer" --exclude="tmp" -zcf '+tarfile+' ./*'
	os.system('tar --exclude=".SCRAM" --exclude="src/LJMet/Com/.git" --exclude="src/.git" --exclude="src/LJMet-Slimmer" --exclude="src/singleLepAnalyzer" --exclude="tmp" -zcf '+tarfile+' ./*')
	os.chdir(thisDir)

for sample in cernList:
	accessor = 'eoscms.cern.ch'
	os.system('python condor_submitDeepAK8.py --useMC False --sample '+sample.split('.')[0]+' --json Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt --fileList '+thisDir+'fileLists2017/'+sample+' --submit True --inputTar '+tarfile+' --outDir /eos/uscms/store/user/lpcljm/2018/LJMet94X_1lep_013019 --shift '+shift+' --accessor '+accessor)

for sample in externalList:
	accessor = 'cmsxrootd.fnal.gov'
	os.system('python condor_submitDeepAK8.py --useMC False --sample '+sample.split('.')[0]+' --json Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt --fileList '+thisDir+'fileLists2017/'+sample+' --submit True --inputTar '+tarfile+' --outDir /eos/uscms/store/user/lpcljm/2018/LJMet94X_1lep_013019 --shift '+shift+' --accessor '+accessor)

## shift should be (one at a time): nominal, JECup, JECdown, JERup, JERdown
## If you want to use different directory names, edit lines 144 - 147 in condor_submit.py so the config is edited correctly
