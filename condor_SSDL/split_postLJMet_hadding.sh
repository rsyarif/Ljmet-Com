#!/bin/bash

#copy:

#dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_2_5_rizki
#dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_2_18_rizki
dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_3_15_rizki

for dataset in DoubleMuon_RRF
do
    for split_num in 1 2
    do
	for ftype in condor csh
	do
	    cp -v $dir/${dataset}.${ftype} $dir/${dataset}_${split_num}.${ftype}
	done
    done
done


#replace:

sed -i 's/RRF/RRF_1/' ${dir}/DoubleMuon_RRF_1.condor
sed -i 's/RRF/RRF_2/' ${dir}/DoubleMuon_RRF_2.condor

sed -i 's/".root"/".root" | grep "RRF_1."/g' ${dir}/DoubleMuon_RRF_1.csh
sed -i 's/".root"/".root" | grep -v "RRF_1."/g' ${dir}/DoubleMuon_RRF_2.csh

sed -i 's/RRF.root/RRF_1.root/g' ${dir}/DoubleMuon_RRF_1.csh
sed -i 's/RRF.root/RRF_2.root/g' ${dir}/DoubleMuon_RRF_2.csh

#submit jobs:

for dataset in DoubleMuon_RRF
do
    for split_num in 1 2
    do
	condor_submit ${dir}/${dataset}_${split_num}.condor
    done
done