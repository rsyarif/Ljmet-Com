#!/bin/bash

SECONDS=0
echo '----------------'
echo 'Start timing'
echo '----------------'
echo

cmsRun test_producer_MC.py

let "hrs=$SECONDS/60/60"
let "min=$SECONDS/60 - hrs*60"
let "sec=$SECONDS - $hrs*60*60 - $min*60"
echo
echo '--------------CMSRUN DONE---------------------'
echo 'time elapsed : '$hrs' hrs '$min' min '$sec' sec'
echo '----------------------------------------------'

# ljmet testMC.py
# 
# let "hrs=$SECONDS/60/60"
# let "min=$SECONDS/60 - hrs*60"
# let "sec=$SECONDS - $hrs*60*60 - $min*60"
# echo
# echo '--------------LJMET DONE----------------------'
# echo 'time elapsed : '$hrs' hrs '$min' min '$sec' sec'
# echo '----------------------------------------------'
