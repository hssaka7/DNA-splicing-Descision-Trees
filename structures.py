class Node:

    def __init__(self, dataSet):
        # ID
        # IELabel
        # EIlabel
        # Nlabel
        # parent
        # children
        # IE entropy
        # EI entropy
        # N entropy
        self.dataSet = dataSet

    def displayNode(self):
        print("genecode is :  " + self.geneCode + "  label : " + self.label)



class Gene:
    def __init__(self, geneCode, label):
        self.geneCode = geneCode
        self.label = label

