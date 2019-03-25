#!/bin/bash

#copy:

#dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_2_5_rizki
#dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_2_18_rizki
dir=hadd_jobs_LJMet94x_2lepTT_2017datasets_2019_3_15_rizki

for dataset in ZZ_part2
do
    for split_num in 1 2 3 4 5 6 7 8 9 10
    do
	for ftype in condor csh
	do
	    cp -v $dir/${dataset}.${ftype} $dir/${dataset}_${split_num}.${ftype}
	done
    done
done


#replace:

sed -i 's/part2/part2_1/' ${dir}/ZZ_part2_1.condor
sed -i 's/part2/part2_2/' ${dir}/ZZ_part2_2.condor
sed -i 's/part2/part2_3/' ${dir}/ZZ_part2_3.condor
sed -i 's/part2/part2_4/' ${dir}/ZZ_part2_4.condor
sed -i 's/part2/part2_5/' ${dir}/ZZ_part2_5.condor
sed -i 's/part2/part2_6/' ${dir}/ZZ_part2_6.condor
sed -i 's/part2/part2_7/' ${dir}/ZZ_part2_7.condor
sed -i 's/part2/part2_8/' ${dir}/ZZ_part2_8.condor
sed -i 's/part2/part2_9/' ${dir}/ZZ_part2_9.condor
sed -i 's/part2/part2_10/' ${dir}/ZZ_part2_10.condor

#1s
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep -v "part2_18." | grep -v "part2_17." | grep -v "part2_16." | grep -v "part2_15." | grep -v "part2_14."/g'  ${dir}/ZZ_part2_1.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep -v "part2_18." | grep -v "part2_17." | grep -v "part2_16." | grep -v "part2_15." | grep    "part2_14."/g'  ${dir}/ZZ_part2_2.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep -v "part2_18." | grep -v "part2_17." | grep -v "part2_16." | grep    "part2_15."/g'  ${dir}/ZZ_part2_3.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep -v "part2_18." | grep -v "part2_17." | grep    "part2_16."/g'  ${dir}/ZZ_part2_4.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep -v "part2_18." | grep    "part2_17."/g'  ${dir}/ZZ_part2_5.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep -v "part2_19." | grep    "part2_18."/g'  ${dir}/ZZ_part2_6.csh #
sed -i 's/".root"/".root" | grep    "part2_1." | grep "part2_19."/g'  ${dir}/ZZ_part2_7.csh #
# #not 1s
sed -i 's/".root"/".root" | grep -v "part2_1." | grep -v "part2_9." | grep -v "part2_8."/g' ${dir}/ZZ_part2_8.csh #
sed -i 's/".root"/".root" | grep -v "part2_1." | grep -v "part2_9." | grep    "part2_8."/g' ${dir}/ZZ_part2_9.csh #
sed -i 's/".root"/".root" | grep -v "part2_1." | grep    "part2_9."/g' ${dir}/ZZ_part2_10.csh #

sed -i 's/part2.root/part2_1.root/g' ${dir}/ZZ_part2_1.csh
sed -i 's/part2.root/part2_2.root/g' ${dir}/ZZ_part2_2.csh
sed -i 's/part2.root/part2_3.root/g' ${dir}/ZZ_part2_3.csh
sed -i 's/part2.root/part2_4.root/g' ${dir}/ZZ_part2_4.csh
sed -i 's/part2.root/part2_5.root/g' ${dir}/ZZ_part2_5.csh
sed -i 's/part2.root/part2_6.root/g' ${dir}/ZZ_part2_6.csh
sed -i 's/part2.root/part2_7.root/g' ${dir}/ZZ_part2_7.csh
sed -i 's/part2.root/part2_8.root/g' ${dir}/ZZ_part2_8.csh
sed -i 's/part2.root/part2_9.root/g' ${dir}/ZZ_part2_9.csh
sed -i 's/part2.root/part2_10.root/g' ${dir}/ZZ_part2_10.csh

#submit jobs:

for dataset in ZZ_part2
do
    for split_num in 1 2 3 4 5 6 7 8 9 10
    do
       condor_submit ${dir}/${dataset}_${split_num}.condor
    done
done