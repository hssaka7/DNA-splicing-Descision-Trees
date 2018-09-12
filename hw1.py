import csv
from structure import Node,Gene


def dataToNode(location):
    genes = [];
    with open(location,'r') as csvFileObject:
         csvReader = csv.reader(csvFileObject)
         for line in csvReader:
             genes.append(Gene(line[1],line[2]))
    return genes

def createFun(pos):
    def fuctionToReturn(label):
        return label[pos]
    return fuctionToReturn



def main():
    genes = dataToNode("data/training.csv")
    functions = [createFun(x) for x in range(1,60)]
    node = Node(genes,functions)
    node.split()


if __name__== "__main__":
  main()
