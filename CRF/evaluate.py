#!/usr/bin/python
#-*- coding:UTF-8 -*-
#########################################################################
# File Name: evaluate.py
# Author: MT_NLP_Team
# Mail: tne.nlp@meituan.com
# Created Time: 15:20:39 2016-08-15
#########################################################################
import sys

infile = open("datadata_result").readlines()
TP = 0
FN = 0
FP = 0
TN = 0
for line in infile:
    m = line.split()
    print len(m)
    if len(m)==0:
        continue
    if m[-2]=="1" and m[-1]=="1":
        TP += 1
    elif m[-2]=="1" and m[-1]=="0":
        FN += 1
    elif m[-2]=="0" and m[-1]=="1":
        FP += 1
    else:
        TN += 1
precision = float(TP)/(TP+FP)
recall = float(TP)/(TP+FN)
f1 = 2*precision*recall/(precision+recall)
print precision,recall,f1
