#!/bin/bash

rm -iv /uscms_data/d3/rsyarif/Brown2018/TT_BB_SSDL_LJMet_2017data/ljmet.tar 

#TESTS
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_TEST.txt --inputFile Samples_TEST.txt
# python TT_SSDL_Submit_Data.py --prefixFile Prefix_TESTDATA.txt --inputFile Samples_TESTDATA.txt
# python TT_SSDL_Submit_FakeRate_Data_2017dataset.py --prefixFile Prefix_TESTDATA.txt --inputFile Samples_TESTDATA.txt


### Mar 15, 2019 -- 1 file per job. After BUG fix in DilepEventSelector.cc 
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveTT.txt --inputFile Samples_InclusiveTT.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveBB.txt --inputFile Samples_InclusiveBB.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_BackgroundMC.txt --inputFile Samples_BackgroundMC.txt
# python TT_SSDL_Submit_Data.py --prefixFile Prefix_Data2017.txt --inputFile Samples_Data2017.txt
python TT_SSDL_Submit_FakeRate_Data_2017dataset.py --prefixFile Prefix_Data_FakeRate_2017dataset.py --inputFile Samples_Data_FakeRate_2017dataset.txt


### Mar 8, 2019 -- 1 file per job. 

# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveTT.txt --inputFile Samples_InclusiveTT.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveBB.txt --inputFile Samples_InclusiveBB.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_BackgroundMC.txt --inputFile Samples_BackgroundMC.txt
# python TT_SSDL_Submit_Data.py --prefixFile Prefix_Data2017.txt --inputFile Samples_Data2017.txt


### Feb 28, 2019 -- More Triggers, including HT mu, elV2 ! 

# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveTT.txt --inputFile Samples_InclusiveTT.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_InclusiveBB.txt --inputFile Samples_InclusiveBB.txt
# python TT_SSDL_Submit_MC.py --prefixFile Prefix_BackgroundMC.txt --inputFile Samples_BackgroundMC.txt
# python TT_SSDL_Submit_Data.py --prefixFile Prefix_Data2017.txt --inputFile Samples_Data2017.txt
# python TT_SSDL_Submit_FakeRate_Data_2017dataset.py --prefixFile Prefix_Data_FakeRate_2017dataset.py --inputFile Samples_Data_FakeRate_2017dataset.txt




