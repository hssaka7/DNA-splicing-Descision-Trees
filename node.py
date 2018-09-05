class Node:

    def __init__(self, geneCode,label):
        # ID
        # IELabel
        # EIlabel
        # Nlabel
        # parent
        # children
        # IE entropy
        # EI entropy
        # N entropy
        self.geneCode = geneCode
        self.label = label



    def displayNode(self):
        print("genecode is :  " + self.geneCode + "  label : " + self.label)
