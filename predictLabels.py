import csv
import numpy as np
from structure import Node,Gene
import sys


def dataToNode(location):
    """converts the data into array of genes"""
    genes = [];
    with open(location,'r') as csvFileObject:
         csvReader = csv.reader(csvFileObject)
         for line in csvReader:
             genes.append(Gene(line[1],line[2]))
    return genes

def createFun(pos):
    """creates a list of function that returns character at certain positions"""
    def fuctionToReturn(label):
        return label[pos]
    return fuctionToReturn

def compareAccuracy(prediction,actual):
    """compares the answers between two files
       created to test answers with previous predictions"""
    correct = 0
    incorrect = 0
    with open(prediction,'r') as predictionObject,open(actual,'r') as actualObject:
         predReader = list(csv.reader(predictionObject))
         actReader = list(csv.reader(actualObject))
         for i in (range(len(actReader))):
             #checks the prediction
             prefline = predReader[i]
             actline = actReader[i]
             if (prefline[1]==actline[1]):
                correct+=1
             else:
                incorrect +=1
    return correct,incorrect



def main():

    ##default values
    parameter = []
    parameter.append("")     #input file location
    parameter.append("")     #test file location
    parameter.append("ig")   #information gain "ig" or gini indes "gi"
    parameter.append("0")    # confidenceLevel
    parameter.append("")     # want to use chisquare, 0 or "" for false, everything else true
    count = 0


    ##maps the arguments provided
    for arg in sys.argv[1:]:
        parameter[count] = arg
        count+=1

    parameter[3] = float(parameter[3])
    parameter[4] = bool(parameter[4])


    genes = dataToNode(parameter[0])
    functions = [createFun(x) for x in range(0,60)]

    #created a node with the genes, function and input values for choice of function, confidenceLevel and chisquare
    mainNode = Node(genes,functions,parameter[2],parameter[4],parameter[3])
    mainNode.calculateLables()


    nodes = [mainNode] #list of nodes thats need to be splitted
    while (nodes):
        node = nodes.pop(0) #node at the top is chosen and splitted
        node.split()
        nodes+=list(node.nodes.values()) #the splitted nodes are added to the queue
    print ("done")

    #exports the prediction to predict.csv file
    if (parameter[1]!=""):
         mainNode.getPrediction(parameter[1])



if __name__ == "__main__":
    main()
