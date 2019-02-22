#!/bin/bash
#
# Template of the c-shell script for submitting a CONDOR job
#
# Need to be submitted as arguments from condor .jdl file:
#    - CMSSWBASE       - local release base ($CMSSW_BASE)
#    - OUTPUT_DIR      - condor work and output dir
#    - PREFIX          - some generic name for the set of jobs (like ttbar, wjets)
#    - CONDOR_PROCESS  - condor job number (ranges from 0 to N-1 jobs)
#    - CONDOR_CLUSTER  - condor cluster (for recordkeeping)
# Arguments = INPUTTAR OUTPUT_DIR PREFIX $(process)
TARDIR=$1
INPUTTAR=$2
OUTPUT_DIR=$3
PREFIX=$4
JOBID=$5

uname -n
source /cvmfs/cms.cern.ch/cmsset_default.sh

xrdcp ${TARDIR}/${INPUTTAR}.tar . 2>&1
XRDEXIT=$?
if [[ $XRDEXIT -ne 0 ]]; then
    echo "exit code $XRDEXIT, failure in xrdcp of tarball"
    exit $XRDEXIT
fi

#setup scram architecture
export SCRAM_ARCH=slc6_amd64_gcc630

echo "make new scram area 'cmsrel'"
scramv1 project CMSSW ${INPUTTAR}

#move tar to newly created scram area
mv -v ${INPUTTAR}.tar ${INPUTTAR}/src/

#cd to scram area
cd ${INPUTTAR}/src

#Untar file, move, and clean. untar file: CMSSW_9_4_X/src/LJMet. (and one more folder). Right now it is quick and dirty. Probably there is a better way.
tar -xf ${INPUTTAR}.tar 
mv  -v ${INPUTTAR}/src/* .
rm -rvf ${INPUTTAR}

echo "compiling 'scram b'"
scram b 


echo "executing 'cmsenv'"
eval `scramv1 runtime -sh`

cd -

SECONDS=0
echo '----------------'
echo 'Start timing'
echo '----------------'
echo


echo "Running producer"
cmsRun producer_${PREFIX}_${JOBID}.py

let "hrs=$SECONDS/60/60"
let "min=$SECONDS/60 - $hrs*60"
let "sec=$SECONDS - $hrs*60*60 - $min*60"
echo
echo '--------------CMSRUN DONE---------------------'
echo 'time elapsed : '$hrs' hrs '$min' min '$sec' sec'
echo '----------------------------------------------'


echo "Sleeping for one minute..."
sleep 60


sed -i "s|CONDOR_RELBASE|$PWD/$INPUTTAR|" ${PREFIX}_${JOBID}.py
ljmet ${PREFIX}_${JOBID}.py

let "hrs=$SECONDS/60/60"
let "min=$SECONDS/60 - $hrs*60"
let "sec=$SECONDS - $hrs*60*60 - $min*60"
echo
echo '--------------LJMET DONE----------------------'
echo 'time elapsed : '$hrs' hrs '$min' min '$sec' sec'
echo '----------------------------------------------'


echo
echo "Deleting the mediator MiniAOD file"
rm mediator*.root


# copy output to eos
echo "xrdcp .root output for condor"
for FILE in *.root
do
  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}"
  xrdcp -f ${FILE} ${OUTPUT_DIR}/${FILE} 2>&1
  XRDEXIT=$?
  if [[ $XRDEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $XRDEXIT, failure in xrdcp"
    exit $XRDEXIT
  fi
  rm ${FILE}
done

echo "removing tar from condor"
rm -f ${INPUTTAR}.tar
