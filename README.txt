There are two files, structure.py and predictLables.py

struture.py contains the outline and functions used by the node. Gene class is also defined here.
predictLabels.py initializes a node, trains it and also tests the data is testing location is provided

to run the program, please use the following example to run it with python3

format:
python3 predictLabels.py trainingLocation testingLocation choice_of_Function confidenceLevel chiSquare

 trainingLocation : where the training data is located (required)
 testingLocation  :  where the testing data is located
 choice_of_Function : "ig" for informationGain or "gi" for gini-index , defualt = "ig"
 confidenceLevel : confidence level to calculate threshold in chisquare , defualt = 0
 chiSquare : if split stopping using chi-square will be used or not(0,"" is false, anything else is true). defualt = "" (false)

 example :
 python3 predictLabels.py data/training.csv  data/testing.csv ig 0.95 true
 python3 predictLabels.py data/training.csv
