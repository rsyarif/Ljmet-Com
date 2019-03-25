#!/bin/bash

for sch in lpcschedd1 lpcschedd2 lpcschedd3;
do
    condor_rm -name $sch rsyarif;
done
