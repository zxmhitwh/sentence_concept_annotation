from tag_train import *
def feature_generate(traindic,datadic,trainfile):
    clusterdic,total_clusternumber = get_Totalwords_Cluster()
    total_words = word_extraction(datadic)
    outfile = open(trainfile,"w")
    total_vector = []
    num = 0
    for sentence in traindic.keys():
        num += 1
        print num
        if len(traindic[sentence]) != len(datadic[sentence]):
            print sentence,len(traindic[sentence]),len(datadic[sentence])
        tagresult = datadic[sentence]
        keys = set(clusterdic.keys())
        for i in range(len(tagresult)):
            vectorlist = []
            word = tagresult[i].split()[0][::-1].split("_",1)[1][::-1]
            vectorlist.append(word)
            word_num = tagresult[i].split()[0].split('_')[-1].split('/')[0]
            pos = tagresult[i].split()[0].split('_')[-1].split('/')[1]
            vectorlist.append(pos)
            parentedge = get_parentedge(word_num,tagresult)
            #childedges = get_childedge(word_num,tagresult)
            if word in keys:
                vectorlist.append(str(clusterdic[word]))
            else:
                vectorlist.append(str(500))
            vectorlist.append(parentedge)
            vectorlist.append(str(traindic[sentence][i][1]))
            for item in vectorlist:
                outfile.write(item+"\t")
            outfile.write("\n")
        outfile.write("\n")

if __name__ == "__main__":
    traindic = get_trainset("datadata_test")
    datadic = get_corpus("datadata_corpus")
    feature_generate(traindic,datadic,"datadata_crf_test")
