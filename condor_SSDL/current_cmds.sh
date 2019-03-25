#!/bin/bash

# dir="/uscms_data/d3/rsyarif/Brown2018/TT_BB_SSDL_LJMet_2017data/LJMet94x_2lepTT_2017datasets_2019_2_28_rizki/"
dir="/uscms_data/d3/rsyarif/Brown2018/TT_BB_SSDL_LJMet_2017data/LJMet94x_2lepTT_2017datasets_2019_3_15_rizki/"

# cmd="python CheckErrors.py "${dir}"  --verbose 1 --resub_num -1 --resubmit "$1
cmd="python CheckErrors_v2.py "${dir}"  --verbose 1 --resub_num -1 --resubmit "$1

echo $cmd
$cmd
