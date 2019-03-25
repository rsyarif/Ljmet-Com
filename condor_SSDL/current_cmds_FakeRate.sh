#!/bin/bash


cmd="python CheckErrors_v2.py /uscms_data/d3/rsyarif/Brown2018/TT_BB_SSDL_LJMet_2017data/LJMet94x_2lepTT_2017datasets_FakeRate_2019_3_15_rizki/ --verbose 1 --resub_num -1 --resubmit "$1

echo $cmd
$cmd

cmd="rm -v /uscms_data/d3/rsyarif/Brown2018/TT_BB_SSDL_LJMet_2017data/LJMet94x_2lepTT_2017datasets_FakeRate_2019_3_15_rizki/*/core*"

echo $cmd
$cmd