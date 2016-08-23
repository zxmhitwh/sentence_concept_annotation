#!/usr/bin/python
#-*- coding:UTF-8 -*-
#########################################################################
# File Name: tag_train.py
# Author: MT_NLP_Team
# Mail: tne.nlp@meituan.com
# Created Time: 11:11:00 2016-08-08
#########################################################################
import sys

from sklearn.linear_model.logistic import logistic_regression_path
from sklearn import linear_model

def pre_process(datadic):
    '''
    处理对于词为''的形式
    '''
    num = 0
    for key in datadic.keys():
        for i in range(len(datadic[key])):
            #print datadic[key][i].split()[0].split('_')[-1].split('/')[0]
            if  i == int(datadic[key][i].split()[0].split('_')[-1].split('/')[0]):
                pass
            else:
                num += 1
                word = datadic[key][i].split()[0].split('_')[0]
                pos = datadic[key][i].split()[0].split('_')[-1].split('/')[1]
                yulai2 = word + "_" + datadic[key][i].split()[0].split('_')[-1].split('/')[0]
                replace2 = word + "_" + str(i)
                for i in range(len(datadic[key])):
                    datadic[key][i] = datadic[key][i].replace(yulai2,replace2)
    print "不符合规则的句子个数:" + str(num)

def get_corpus(corpus):
    infile = open(corpus).readlines()
    datadic = {}
    ins = []
    for line in infile:
        if len(line.split()) == 3 and '_' in line.split()[0] and "/" in line.split()[0]:
            if line.startswith(" "):
                pass
            else:
                ins.append(line)
        else:
            datadic[line.strip('\n')] = ins
            ins = []
    pre_process(datadic)
    return datadic

def get_trainset(trainset):
    infile = open(trainset).readlines()
    traindic = {}
    for line in infile:
        items = line.split("||#||")
        traindic[items[0]] = []
        positems = items[1].split()
        for positem in positems:
            if positem.endswith("/food"):
                inverse = positem[::-1]
                nPos = inverse.find(':')
                n = len(positem) - 1 - nPos
                traindic[items[0]].append([positem[0:n],1])
            else:
                traindic[items[0]].append([positem,0])
    return traindic

def get_Totalwords_Cluster():
    infile = open("sample_label").readlines()
    clusterdic = {}
    total_clusternumber = []
    #total_words = []
    for line in infile:
        items = line.split()
        total_clusternumber.append(int(items[1]))
        #total_words.append(items[0])
        clusterdic[items[0]] = int(items[1])
    total_clusternumber = list(set(total_clusternumber))
    total_clusternumber = sorted(total_clusternumber)
    return clusterdic,total_clusternumber

def word_extraction(datadic):
    totalwords = []
    for key in datadic.keys():
        for item in datadic[key]:
            item1 = item.split()[0]
            inverse = item1[::-1]
            nPos = inverse.find('_')
            n = len(item1) - 1 - nPos
            totalwords.append(item1[0:n])
    totalwords = list(set(totalwords))
    print "totalwords:",len(totalwords)
    return totalwords

def get_childedge(num,tagresult):
    childedges = []
    for tag in tagresult:
        if tag.split()[1] == 'Root':
            continue
        elif tag.split()[1].split('_')[-1]==num:
            childedges.append(tag.split()[-1])
    childedges = set(childedges)
    return childedges

def get_parentedge(num,tagresult):
    return tagresult[int(num)].split()[-1]

def get_parentnode(num,tagresult):
    if tagresult[int(num)].split()[1] == "Root":
        return "Root"
    else:
        return tagresult[int(num)].split()[1].split("_")[-1]

def get_feature(traindic,datadic,threshold):#设置考虑位置前后两个词还是一个词
    clusterdic,total_clusternumber = get_Totalwords_Cluster()
    keys = set(clusterdic.keys())
    total_words = word_extraction(datadic)
    labels = []
    total_vector = []
    target = ""
    total_pos = ['nh', 'ni', 'nl', 'nd', 'nz', 'ns', 'nt', 'ws', 'wp', 'a', 'c', 'b', 'e', 'd', 'i', 'k', 'j', 'm', 'o', 'n', 'q', 'p', 'r', 'u', 't', 'v', 'z']
    total_dp = ['ADV', 'RAD', 'SBV', 'DBL', 'VOB', 'LAD', 'HED', 'ATT', 'FOB', 'WP', 'POB', 'IOB', 'COO', 'CMP']
    num = 0
    for sentence in traindic.keys():
        num += 1
        print num,sentence
        if len(traindic[sentence]) != len(datadic[sentence]):
            print sentence
        feature_vector = []
        tagresult = datadic[sentence]
        for m in traindic[sentence]:
            labels.append(m[1])
        #print labels
        feature_list = [] #记录这个句子中的每个特征词
        for tag in tagresult:
            vectorlist = []
            word = tag.split()[0][::-1].split("_",1)[1][::-1]
            word_num = tag.split()[0].split('_')[-1].split('/')[0]
            pos = tag.split()[0].split('_')[-1].split('/')[1]
            parentedge = get_parentedge(word_num,tagresult)
            childedges = get_childedge(word_num,tagresult)
            word_vector = [0 for x in total_words]
            pos_vector = [0 for x in total_pos]
            clusternumber_vector = [0 for x in total_clusternumber]
            parent_vector = [0 for x in total_dp]
            child_vector = [0 for x in total_dp]
            for i in range(len(total_words)):
                if total_words[i] == word:
                    word_vector[i] = 1
                    break
            for i in range(len(total_pos)):
                if total_pos[i] == pos:
                    pos_vector[i] = 1
                    break
            if word in keys:
                clusternumber_vector[clusterdic[word]] = 1
            for i in range(len(total_dp)):
                if total_dp[i] == parentedge:
                    parent_vector[i] = 1
                    break
            for i in range(len(total_dp)):
                if total_dp[i] in childedges:
                    child_vector[i] = 1
            parentnode = get_parentnode(word_num,tagresult)
            if parentnode!="Root" and int(parentnode)>=len(datadic[sentence]):
                parentnode = str(len(datadic[sentence])-1)
            feature_list.append([word_vector+pos_vector+clusternumber_vector,parent_vector+child_vector,parentnode])

        parentnode_vector = []
        for i in range(len(feature_list)):
            each_feature_vector = []
            word_pos_cls,parent_child,parentnode = feature_list[i]
            if threshold == 1:
                if i == 0 and i == len(feature_list)-1:
                    prevectorlist = [0 for x in word_pos_cls]
                    nextvectorlist = [0 for x in word_pos_cls]
                elif i == 0:
                    prevectorlist = [0 for x in word_pos_cls]
                    nextvectorlist = feature_list[i+1][0]
                elif i == len(feature_list)-1:
                    prevectorlist = feature_list[i-1][0]
                    nextvectorlist = [0 for x in word_pos_cls]
                else:
                    prevectorlist = feature_list[i-1][0]
                    nextvectorlist = feature_list[i+1][0]
                each_feature_vector = word_pos_cls+prevectorlist+nextvectorlist
            elif threshold == 2:
                prevectorlist_2 = [0 for x in word_pos_cls]
                prevectorlist_1 = [0 for x in word_pos_cls]
                nextvectorlist_1 = [0 for x in word_pos_cls]
                nextvectorlist_2 = [0 for x in word_pos_cls]
                if i ==0 and i ==len(feature_list)-1:
                    pass
                elif i==0 and len(feature_list)==2:
                    nextvectorlist_1 = feature_list[i+1][0]
                elif i==1 and len(feature_list)==2:
                    prevectorlist_1 = feature_list[i-1][0]
                elif i==0 and len(feature_list)==3:
                    nextvectorlist_1 = feature_list[i+1][0]
                    nextvectorlist_2 = feature_list[i+2][0]
                elif i==1 and len(feature_list)==3:
                    prevectorlist_1 = feature_list[i-1][0]
                    nextvectorlist_1 = feature_list[i+1][0]
                elif i==2 and len(feature_list)==3:
                    prevectorlist_2 = feature_list[i-2][0]
                    prevectorlist_1 = feature_list[i-1][0]
                elif i==0:
                    nextvectorlist_1 = feature_list[i+1][0]
                    nextvectorlist_2 = feature_list[i+2][0]
                elif i==1:
                    prevectorlist_1 = feature_list[i-1][0]
                    nextvectorlist_1 = feature_list[i+1][0]
                    nextvectorlist_2 = feature_list[i+2][0]
                elif i==len(feature_list)-2:
                    prevectorlist_2 = feature_list[i-2][0]
                    prevectorlist_1 = feature_list[i-1][0]
                    nextvectorlist_1 = feature_list[i+1][0]
                elif i==len(feature_list)-1:
                    prevectorlist_2 = feature_list[i-2][0]
                    prevectorlist_1 = feature_list[i-1][0]
                else:
                    prevectorlist_2 = feature_list[i-2][0]
                    prevectorlist_1 = feature_list[i-1][0]
                    nextvectorlist_1 = feature_list[i+1][0]
                    nextvectorlist_2 = feature_list[i+2][0]
                each_feature_vector = word_pos_cls+prevectorlist_2+prevectorlist_1+nextvectorlist_1+nextvectorlist_2
            else:
                print "input error!"
            feature_vector.append(each_feature_vector)
            if parentnode == "Root":
                parentnode_vector.append([0 for x in word_pos_cls]+[0 for x in parent_child])
            else:
                parentnode_vector.append(feature_list[int(parentnode)][1]+feature_list[int(parentnode)][0])
        for i in range(len(parentnode_vector)):
            if i == 0 and i == len(parentnode_vector)-1:
                preparentvector = [0 for x in parentnode_vector[i]]
                nextparentvector = [0 for x in parentnode_vector[i]]
            elif i == 0:
                preparentvector = [0 for x in parentnode_vector[i]]
                nextparentvector = parentnode_vector[i+1]
            elif i == len(parentnode_vector)-1:
                preparentvector = parentnode_vector[i-1]
                nextparentvector = [0 for x in parentnode_vector[i]]
            else:
                preparentvector = parentnode_vector[i-1]
                nextparentvector = parentnode_vector[i+1]
            feature_vector[i].extend(parentnode_vector[i]+preparentvector+nextparentvector)
            if len(feature_vector)!=len(traindic[sentence]):
                target = sentence
            #print len(feature_vector[i])   
        print "feature:",len(feature_vector[0])
        total_vector.extend(feature_vector)
    print "totoalvector:",len(total_vector)
    print "label:",len(labels)
    print target
    return total_vector,labels

def get_vector(traindic,datadic):
    clusterdic,total_clusternumber = get_Totalwords_Cluster()
    total_words = word_extraction(datadic)
    wordsdic = {}
    for i in range(len(total_words)):
        wordsdic[total_words[i]] = i
    labels = []
    total_vector = []
    total_pos = ['nh', 'ni', 'nl', 'nd', 'nz', 'ns', 'nt', 'ws', 'wp', 'a', 'c', 'b', 'e', 'd', 'i', 'k', 'j', 'm', 'o', 'n', 'q', 'p', 'r', 'u', 't', 'v', 'z']
    total_dp = ['ADV', 'RAD', 'SBV', 'DBL', 'VOB', 'LAD', 'HED', 'ATT', 'FOB', 'WP', 'POB', 'IOB', 'COO', 'CMP']
    num = 0
    num1 = 0
    keys = set(clusterdic.keys())
    for sentence in traindic.keys():
        num += 1
        print num,sentence
        if len(traindic[sentence]) != len(datadic[sentence]):
            print sentence
        feature_vector = []
        tagresult = datadic[sentence]
        for m in traindic[sentence]:
            labels.append(m[1])
        #print labels
        feature_list = [] #记录这个句子中的每个特征词
        for tag in tagresult:
            vectorlist = []
            word = tag.split()[0][::-1].split("_",1)[1][::-1]
            word_num = tag.split()[0].split('_')[-1].split('/')[0]
            pos = tag.split()[0].split('_')[-1].split('/')[1]
            parentedge = get_parentedge(word_num,tagresult)
            childedges = get_childedge(word_num,tagresult)
            word_vector = [0 for x in total_words]
            pos_vector = [0 for x in total_pos]
            clusternumber_vector = [0 for x in total_clusternumber]
            parent_vector = [0 for x in total_dp]
            child_vector = [0 for x in total_dp]
            word_vector[wordsdic[word]] = 1

            for i in range(len(total_pos)):
                if total_pos[i] == pos:
                    pos_vector[i] = 1
                    break
            if word in keys:
                clusternumber_vector[clusterdic[word]] = 1
            for i in range(len(total_dp)):
                if total_dp[i] == parentedge:
                    parent_vector[i] = 1
                    break   
            for i in range(len(total_dp)):
                if total_dp[i] in childedges:
                    child_vector[i] = 1
            feature_list.append(word_vector+pos_vector+clusternumber_vector+parent_vector+child_vector)
        num1 += len(feature_list)
        print num1
        total_vector.extend(feature_list)
    print num1
    return total_vector,labels


def accuracy_test(train_feature,train_labels,test_feature,test_labels):
    clf = linear_model.LogisticRegression()
    print clf.fit(train_feature,train_labels)
    predict_labels = clf.predict(test_feature)
    predict_proba = [x[0] for x in clf.predict_proba(test_feature)]
    confidence = [get_confidence(x) for x in predict_proba]
    bad_num = []
    TP = 0
    FN = 0
    FP = 0
    TN = 0
    for i in range(len(test_labels)):
        if test_labels[i] == 1 and predict_labels[i] == 1:
            TP += 1
        elif test_labels[i] == 1 and predict_labels[i] == 0:
            FN += 1
        elif test_labels[i] == 0 and predict_labels[i] == 1:
            FP += 1
        else:
            TN += 1
        if test_labels[i] != predict_labels[i]:
            bad_num.append([i,test_labels[i],predict_labels[i],predict_proba[i]])
    print TP,FP
    precision = float(TP)/(TP+FP)
    recall = float(TP)/(TP+FN)
    f1 = 2*precision*recall/(precision+recall)
    print precision,recall,f1
    return bad_num

def test():
    traindic = get_trainset("foodtag_train1")
    datadic = get_corpus("foodcomment_corpus")
    datadic1 = get_corpus("datadata_corpus")
    datadic = dict(datadic,**datadic1)
    train_feature,train_labels = get_feature(traindic,datadic,1)
    testdic = get_trainset("datadata_test")
    test_feature,test_labels = get_feature(testdic,datadic,1)
    print len(train_feature),len(train_labels)
    print len(test_feature),len(test_labels)
    bad_num = accuracy_test(train_feature,train_labels,test_feature,test_labels)
    #word_list = get_word(testdic)
    #for i,real,prec,proba in bad_num:
    #   print word_list[i],real,prec,proba

def output():
    traindic = get_trainset("foodtag_train1")
    datadic = get_corpus("foodcomment_corpus")
    datadic1 = get_corpus("datadata_corpus")
    outfile = open("datadata_predict","w")
    datadic = dict(datadic,**datadic1)
    train_feature,train_labels = get_vector(traindic,datadic)
    testdic = get_trainset("datadata_test")
    #test_feature,test_labels = get_feature(testdic,datadic,1)
    print len(train_feature),len(train_labels)
    #print len(test_feature),len(test_labels)
    clf = linear_model.LogisticRegression()
    print clf.fit(train_feature,train_labels)
    for line in open("datadata_test").readlines():
        key = line.split("||#||")[0]
        testdic1 = {}
        testdic1[key] = testdic[key]
        test_feature,testlable = get_vector(testdic1,datadic)
        predict_label = clf.predict(test_feature)
        for i in range(len(predict_label)):
            if predict_label[i] == 0:
                outfile.write(testdic1[key][i][0].strip("/food")+" ")
            elif predict_label[i] == 1:
                outfile.write(testdic1[key][i][0].strip("/food")+"/food"+" ")
        outfile.write("\n")

if __name__ == '__main__':
    #traindic = get_trainset("foodtag_train")
    '''
    train = []
    for key in traindic.keys():
        train.append(key)
    print len(train)
    print len(set(train))
    '''
    #test()
    output()
    #datadic = get_corpus("foodcomment_corpus")
    #total_vector,labels = get_feature(traindic,datadic,1)
    #print len(total_vector)
    #print len(labels)
    '''
    for key in traindic.keys(): 
        if len(datadic[key])!=len(traindic[key]):
            print key,len(datadic[key]),len(traindic[key])
    '''

