import numpy as np
import csv
class Node:

    def __init__(self, genes, functions):
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
        self.subTotal = {
                      "EI":0,
                      "IE":0,
                      "N":0,
        }
        self.total = len(genes)
        self.terminal = False

    def calculateGiniIndex(self, nodes):
        acc = 0
        for key in nodes:
            node = nodes[key]
            node.calculateLables()
            node.calculateIndex()
            acc = acc + (node.index * node.total / self.total)
        return acc


    def splitNode(self,func):
        val =  {}
        nodes =  {}
        for gene in self.genes:
            temp = func(gene.geneCode)
            if temp in val :
                val[temp].append(gene)
            else:
                val[temp]=[gene]
        for key in val:
            nodes[key]=Node(val[key],[])
        return nodes,self.calculateGiniIndex(nodes)

    def split(self):
        if (self.terminal):
            return
        temp = self.functions.copy()
        gis = [self.splitNode(func) for func in temp]
        gi = min(gis,key=lambda item:item[1])
        #gi = max([self.splitNode(func)[1] for func in self.functions],key=lambda item:item[1])
        self.nodes = gi[0]
        self.giniIndex = gi[1]
        self.func = temp[gis.index(gi)]
        temp.pop(gis.index(gi))
        for key in self.nodes:
            self.nodes[key].functions = temp
            self.nodes[key].checkTerminal()
            self.nodes[key].calculateNodeLabel()


    def calculateLables(self):
        for gene in self.genes:
            self.subTotal[gene.label]+=1


    def calculateIndex(self):
        temp = np.fromiter(self.subTotal.values(),dtype=float)
        index = 1 - ((np.square(temp/temp.sum())).sum())
        self.index = index

    def checkTerminal(self):
        if (len(self.functions) == 0):
            self.terminal = True
        if (self.total==0):
            self.termial = True
        pure = any(map(lambda x:True if x==self.total else False,list(self.subTotal.values())))
        if (pure):
            self.terminal = True


    def calculateNodeLabel(self):
        self.nodeLabel = max(self.subTotal, key = self.subTotal.get)
        


    def getPrediction(self,location):
        data = [['id','class']]
        with open(location,'r') as csvFileObject:
            csvReader = csv.reader(csvFileObject)
            for line in csvReader:
                data.append([line[0],self.predict(line[1])])
        prediction = open('predict.csv','w')
        with prediction:
            writer = csv.writer(prediction)
            writer.writerows(data)

    def predict(self,geneCode):
        node = self
        while (not node.terminal):
            if (node.func(geneCode) not in node.nodes):
                break
            node = node.nodes[node.func(geneCode)]
        return node.nodeLabel












class Gene:

    def __init__(self,geneCode,label):
        self.geneCode = geneCode
        self.label = label
