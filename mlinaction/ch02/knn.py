from numpy import *
import operator
import time
from os import listdir

def classify(inputPoint, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inputPoint, (dataSetSize,1)) - dataSet
    sqDiffmat = diffmat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    
