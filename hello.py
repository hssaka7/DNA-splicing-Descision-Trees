
import csv
from node import Node


def main ():

    readCsvFile("data/training.csv")


def readCsvFile(location):
    with open(location,'r') as csvFileObject:

          csvReader = csv.reader(csvFileObject)
          for line in csvReader:
              tempNode = Node(line[1],line[2])

              print(line[1] + "  " + line[2])

main()