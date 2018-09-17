import numpy as np
import csv
import math
from scipy.stats import chi2
from random import randint

"""class contains basic structure of Node
   Functions to calculate information gain, gini index, chisquare are implemented in in this class"""
class Node:

    def __init__(self, genes, functions, mode, chi, confidenceLevel):
        # ID
        # IELabel
        # EIlabel
        # Nlabel
        # parent
        # children
        # IE entropy
        # EI entropy
        # N entropy

        self.genes = genes
        self.func = None
        self.functions=functions
        self.nodes = {}
        self.index = 0
        self.giniIndex = 0
        self.subTotal = {'EI':0,'IE':0,'N':0}
        self.total = len(genes)
        self.terminal = False
        self.entropy = 0
        self.iG = 0
        self.mode = mode.lower()
        self.chi = chi
        self.confidenceLevel = confidenceLevel
        self.calculateLables()

    def calculateGiniIndex(self, nodes):
        """calculates the gini index based on the values in the node parameter
           loops through all the nodes, calculates index of each node and returns the weighted sum"""
        acc = 0
        for key in nodes:
            node = nodes[key]
            node.calculateIndex()
            acc = acc + (node.index * node.total / self.total)
        return acc


    def calculateIndex(self):
        """acts like a helper function to calculate gini index of sub nodes"""
        temp = np.fromiter(self.subTotal.values(),dtype=float)
        index = 1 - ((np.square(temp/temp.sum())).sum())
        self.index = index


    def calculateEntropy(self):
        """calculates the entropy of the node based on the gene values contained by it"""
        temp = np.fromiter(self.subTotal.values(),dtype=float)/self.total
        entropy = sum([(-1*x*(math.log(x+0.0001))) for x in temp])
        self.entropy = entropy

    def calculateIG(self,nodes):
        """calculates the information gain based on the values in the node parameter
           loops through all the nodes, accumulates entropy and finds the difference from entropy of parent node"""
        for key in nodes:
            node = nodes[key]
            node.calculateEntropy()
        acc = self.entropy - sum([node.entropy for node in nodes.values()])
        return acc

    def calculateChiSquare(self):
        """finds out the chi-square value, calculates the degree of freedom, proportion of each class
           loops through each nodes and accumulates the overall values"""

        df = (1-len(self.subTotal))*(1-len(self.subTotal))
        proportion = np.fromiter(self.subTotal.values(),dtype=float)/self.total
        acc = 0
        for node in self.nodes.values():
            acc += node.getChiIndex(proportion)
        self.chiSquare = acc
        if (acc < chi2.ppf(self.confidenceLevel, df)):
            self.terminal = True

    def getChiIndex(self,proportion):
        """acts like a helper function to calculate chiSquare,
           Is used to calculate the chisqaure value of each sub-node"""
        expected = self.total * proportion
        with np.errstate(invalid='ignore'):
            observation = np.fromiter(self.subTotal.values(),dtype=float)
            chiSquare = np.nan_to_num(np.square(observation - expected)/expected)
        return sum(chiSquare)


    def splitNode(self,func):
        """splits the node in based on the function provided which takes genescode as input,
            the value returned from the function is the dictionary key for the splitted nodes"""
        val =  {}
        nodes =  {}
        for gene in self.genes:
            #gets the answer to the function, which is the key to the dictionary
            temp = (func(gene.geneCode))
            if temp in val :
                val[temp].append(gene)
            else:
                val[temp]=[gene]
        for key in val:
            #initializes a new node with required values
            nodes[key]=Node(val[key],[],self.mode,self.chi,0)
        toReturn = 0

        #chooses appropriate function
        if (self.mode == "ig"):
            toReturn = self.calculateIG(nodes)
        else:
            toReturn = self.calculateGiniIndex(nodes)
        return nodes,toReturn

    def split(self):
        """splits the current node based on either gini index or information gain
           for each possible function, it finds out the function with best split"""
        if (self.terminal):
            return
        temp = self.functions.copy()
        #creates a tuple of node and its "ig" or "gi" value for all functions
        gis = [self.splitNode(func) for func in temp]
        if (self.mode == "ig"):
            gi = max(gis,key=lambda item:item[1])
        else:
            gi = min(gis,key=lambda item:item[1])

        #adds the current node down to the tree
        self.nodes = gi[0]
        self.giniIndex = gi[1]

        #removes the current functions and adds rest to the children
        self.func = temp[gis.index(gi)]
        temp.pop(gis.index(gi))
        for key in self.nodes:
            self.nodes[key].functions = temp
            self.nodes[key].checkTerminal()
            self.nodes[key].calculateNodeLabel()
        if (self.chi) :
            self.calculateChiSquare()


    def calculateLables(self):
        """calculates the total number of each class present in the node"""
        for gene in self.genes:
            if gene.label in self.subTotal:
                self.subTotal[gene.label]+=1
            else:
                self.subTotal[gene.label]=1



    def checkTerminal(self):
        """checks for terminal condition among these rul:es
           if the number of functon reaches 0
           if a pure node is found
           if an empty node is encountered"""

        if (len(self.functions) == 0):
            self.terminal = True
        if (self.total==0):
            self.termial = True
        #checks if any of classes have total number of nodes
        pure = any(map(lambda x:True if x==self.total else False,list(self.subTotal.values())))
        if (pure):
            self.terminal = True


    def calculateNodeLabel(self):
        """calculates the final prediction label for the node"""
        self.nodeLabel = max(self.subTotal, key = self.subTotal.get)

    def getPrediction(self,location):
        data = [['id','class']]
        with open(location,'r') as csvFileObject:
            csvReader = csv.reader(csvFileObject)
            for line in csvReader:
                #creates a list of data which is written at the end as a csv file
                data.append([line[0],self.predict(line[1])])
        prediction = open('predict.csv','w')
        with prediction:
            writer = csv.writer(prediction)
            writer.writerows(data)


    def predict(self,geneCode):
        """predicts the class given a genecode by applying all the functions"""
        node = self
        while (not node.terminal):
            if (node.func(geneCode) not in node.nodes):
                break #if any new unseen character is seen the current node  labels predict
            node = node.nodes[node.func(geneCode)]
        return node.nodeLabel


"""stores the Gene data"""
class Gene:

    def __init__(self,geneCode,label):
        self.geneCode = geneCode
        self.label = label
