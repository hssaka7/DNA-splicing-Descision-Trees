import numpy as np
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
        temp = self.functions.copy()
        gis = [self.splitNode(func) for func in temp]
        gi = max(gis,key=lambda item:item[1])
        #gi = max([self.splitNode(func)[1] for func in self.functions],key=lambda item:item[1])
        self.nodes = gi[0]
        self.giniIndex = gi[1]
        temp.pop(gis.index(gi))
        for key in self.nodes:
            self.nodes[key].functions = temp




    def calculateLables(self):
        for gene in self.genes:
            self.subTotal[gene.label]+=1


    def calculateIndex(self):
        temp = np.fromiter(self.subTotal.values(),dtype=float)
        index = 1 - ((np.square(temp/temp.sum())).sum())
        self.index = index



class Gene:

    def __init__(self,geneCode,label):
        self.geneCode = geneCode
        self.label = label
