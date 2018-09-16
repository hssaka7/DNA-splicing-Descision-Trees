import csv
import pandas as panda

import math
from collections import Counter;
from pprint import pprint


from structures import Node,Gene


def main ():

    readCsvFile("data/training.csv")

def entropy(listOfProbability):
    total = 0
    for probability in listOfProbability :
        total = total + (- probability * math.log(probability,2))
   # print(total)
    return total

def informationGain(dataList,splitFeature,targetList):
    totalEntropy = entropy(getListOfProbability(dataList))
    #print(totalEntropy)
    #print(dataList[1999].geneCode[58])
    totalDataLen = len(dataList)
    #print(len(dataList))


    splitList = {}
    probabOfFeatures ={}
    entropySplit = {}


    for x in targetList:

        splitList [x] = [ val for val in dataList if val.geneCode[splitFeature] == x]
        #print("the list with target  " + x + "  with length  " )
        #print(len(splitList[x]))
        #print(splitList[x])
        entropySplit[x] = entropy(getListOfProbability(splitList[x]))

        probabOfFeatures[x] = len(splitList[x]) / totalDataLen
    #print ("the list of probability features is " )
    #print( probabOfFeatures)
    #print("the list of entropy features is ")
    #print(entropySplit)
    total = 0
    for x in targetList:
        total = total + probabOfFeatures[x] * entropySplit[x]

    infoGain = totalEntropy - total
    #print("the Information Gain  is ")
    #print(infoGain)



    return infoGain









def getListOfProbability(dataList):
    #tempL = dataList.iloc[:, 2:3].values.tolist()
    labelDataSet = [data.label for data in dataList]
    cnt = Counter();

    for label in labelDataSet:
        cnt[label] += 1

    total = len(labelDataSet)

    probList = [count / total for count in cnt.values()]

    #print(probList)


    return probList



def readCsvFile(location):
    dataset = panda.read_csv('data/training.csv', header=None,index_col=False)

    with open(location,'r') as csvFileObject:
        csvReader = csv.reader(csvFileObject)


        originalDataList = [Gene(line[1],line[2]) for line in csvReader]




    newtemp = ID3Algorithm(originalDataList, list(range(0,60)) , ["IE","EI","N"], "N" ,['A','G','C','T'])

    query = originalDataList[11].geneCode

    prediction = predict(query,newtemp)


    location2 = "data/testing.csv"
    testingDataList = []
    with open(location2,'r') as csvFileObject:
        csvReader = csv.reader(csvFileObject)


        testingDataList = [line[1] for line in csvReader]





    tempint = 2001
    for genecode in testingDataList:
        prediction = predict(genecode,newtemp)
        print( str (tempint)+','+ prediction)
        tempint += 1






def predict(query,tree):
    for feature in list(range(0,60)):
        if feature in list(tree.keys()):

            try:
                temp = tree[feature][query[feature]]
            except:
                return 'N'

            temp = tree[feature][query[feature]]

            if isinstance(temp,dict):
                return predict(query,temp)
            else:
                return temp

def ID3Algorithm(dataList,features,labels, maxProbValue,targetList):
    print("The original DataSet is : ")
    print(dataList)
    print (len(dataList))
    boxes = Counter();
    tempboxes =Counter();
    cnt = Counter();
    for label in labels:
        tempboxes[label] = [x for x in dataList if x.label == label]
        cnt[label] += 1


        if len(tempboxes[label]) != 0:
            boxes[label] = tempboxes[label]
        print("the box label is  ::  " + label)
        print(boxes[label])
        #print(len(boxes[label]))






    #check for homogenity

    if len(boxes) == 1 :

        return list( boxes.keys())[0]

    elif len(dataList) == 0 or len(features) == 0:
        return maxProbValue

    else:

        infoGain = [informationGain(dataList,x,targetList) for x in features]
        maxInfoGain = max(infoGain)
        indexMaxInfoGain = infoGain.index(maxInfoGain)
        bestFeature = features[indexMaxInfoGain]
        bestDefaultLabel = max(cnt)


        tree = {bestFeature:{}}
        newFeatures = [n for n in features if n != bestFeature]

        splitList = {}

        for x in targetList:
            splitList[x] = (x,[val for val in dataList if val.geneCode[bestFeature] == x])



        for newDataList in splitList:

            print("new Data List haruuu ")
            print(splitList[newDataList][1])
            print (len(splitList[newDataList][1]))

            newTree = ID3Algorithm(splitList[newDataList][1],newFeatures,labels,bestDefaultLabel,targetList)



            tree[bestFeature][splitList[newDataList][0]] = newTree
    return tree





main()