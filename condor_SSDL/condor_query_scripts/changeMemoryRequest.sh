#!/bin/bash

for sch in lpcschedd1 lpcschedd2 lpcschedd3;
do
    condor_qedit -name $sch -constraint 'JobStatus == 1' RequestMemory 2000;
done
