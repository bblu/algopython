#################################################  
# kmeans: k-means cluster  
# Author : bblu
# Date   : 2016-03-29  
# HomePage : http://www.bblu.club
# Email  : gmwblu@gmail.cm 
#################################################
#DDS-QSW-D-G-16-WT105
#DDS-LTHF-D-H-31-ST173

from numpy import *
import time
import matplotlib.pyplot as plt

#calc distance^2
def distance2(vec1,vec2):
    return sum(power(vec2-vec1,2))

#init centroids
def initCentroids(dataSet, k):
    numSamples, dim = dataSet.shape
    centroids = zeros((k,dim))
    for i in range(k):
        index = int(random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids


#k-means cluster
def kmeans(dataSet, k):
    numSamples = dataSet.shape[0]
    clusterAssment = mat(zeros((numSamples, 2)))
    clusterChanged = True

    centroids = initCentroids(dataSet,k)

    while clusterChanged:
        clusterChanged = False

        for i in xrange(numSamples):
            minDist = 999999999999.9
            minIndex = 0

            for j in range(k):
                dist = distance2(centroids[j, :], dataSet[i, :])
                if dist < minDist:
                    minDist = dist
                    minIndex = j
            if clusterAssment[i, 0] !=minIndex:
                print "change index [%d]->[%d]" %(clusterAssment[i, 0],minIndex)
                clusterChanged = True
                clusterAssment[i, :] = minIndex, minDist
        for j in range(k):
            ptsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            centroids[j, :] = mean(ptsInCluster, axis = 0)

    print "cluster over!"
    return centroids, clusterAssment

#show cluster result
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print "sorry! dimension is not 2!"
        return 1
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']

    if k > len(mark):
        print "k is too large!"
        return 1

    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']

    for i in range(k):
        plt.plot(centroids[i,0], centroids[i, 1], mark[i], markersize = 12)

    plt.show()
    
                        

print 'step 1: load data...'

dataSet = []

fileIn = open('/home/bblu/python/algorithm/k-means.dat')
for line in fileIn.readlines():
    pt = line.strip().split(' ')
    dataSet.append([float(pt[0]), float(pt[1])])


print 'step 2: clustering data...'

dataSet = mat(dataSet)
k = 5
centroids, clusterAssment = kmeans(dataSet, k)

showCluster(dataSet, k, centroids, clusterAssment)
