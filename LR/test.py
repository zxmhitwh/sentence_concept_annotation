'''
infile1 = open("foodcomment_foodtag").readlines()
infile2 = open("food_comment_0_10000").readlines()
outfile = open("tag","w")
for i in range(len(infile1)):
	outfile.write(infile2[i].strip()+"||#||"+infile1[i])
'''
from tag_train import *
datadic = [1,2,3]
print datadic.find(1)