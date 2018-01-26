from random import random, randint
import math
from pylab import *

weightdomain = [(0,20)] * 4

def wineset1():
    rows=[]
    for i in range(300):
        # Create a random age and rating
        rating = random()*50+50
        age = random()*50

        # Get reference price
        price = wineprice(rating,age)

        # Add some noise
        price *= (random()*0.2+0.9)

        # Add to the dataset
        rows.append({'input': (rating,age), 'result': price})
    return rows

def wineset2():
    rows = []
    for i in range(300):
        rating = random()*50+50
        age = random()*50
        aisle = float(randint(1,20))
        bottlesize = [375.0,750.0,1500.0][randint(0,2)]
        price = wineprice(rating,age)
        price *= (bottlesize/750)
        price *= (random()*0.2+0.9)
        rows.append({'input':(rating,age,aisle,bottlesize),
                    'result':price})
    return rows

def wineset3():
    rows = wineset1()
    for row in rows:
        if random() < 0.5:
            # Wine was bought at a discount store
            row['result'] *= 0.6
    return rows

def rescale(data,scale):
    scaleddata = []
    for row in data:
        scaled = [scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddata.append({'input':scaled,'result':row['result']})
    return scaleddata

def wineprice(rating, age):
    peak_age = rating - 50

    # Calculate price based on rating
    price = rating/2
    if age > peak_age:
        # Past its peak, goes bad in 5 years
        price = price * (5 - (age - peak_age)/2)
    else:
        # Increases to 5x original value as it approaches peak
        price = price * (5 * ((age + 1)/peak_age))
    if price < 0: price = 0
    return price

def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i] - v2[i]) ** 2
    return math.sqrt(d)

def getdistances(data, vec1):
    distancelist = []

    # Loop over every item in the dataset
    for i in range(len(data)):
        vec2 = data[i]['input']

        # Add the distance and the index
        distancelist.append((euclidean(vec1, vec2), i))

    # Sort by distance
    distancelist.sort()
    return distancelist

# numpredict.knnestimate(data,(95.0,3.0))
# numpredict.knnestimate(data,(99.0,5.0),k=1)
def knnestimate(data,vec1,k = 5):
    # Get sorted distances
    dlist = getdistances(data,vec1)
    avg = 0.0

    # Take the average of the top k results
    for i in range(k):
        idx = dlist[i][1]
        avg += data[idx]['result']
    avg = avg/k
    return avg

def knn1(d,v): return knnestimate(d,v,k = 1)
def knn3(d,v): return knnestimate(d,v,k = 3)

def inverseweight(dist, num = 1.0, const = 0.1):
    return num / (dist + const)

def subtractweight(dist, const = 1.0):
    if dist > const:
        return 0
    else:
        return const - dist

def gaussian(dist,sigma = 5.0):
    return math.e ** (-dist ** 2 / (2 * sigma ** 2))

def weightedknn(data, vec1, k = 5, weightf = gaussian):
    # Get distances
    dlist = getdistances(data, vec1)
    avg = 0.0
    totalweight = 0.0

    # Get the weighted average
    for i in range(k):
        dist = dlist[i][0]
        idx = dlist[i][1]
        weight = weightf(dist)
        avg += weight * data[idx]['result']
        totalweight += weight
    avg = avg / totalweight
    return avg

def knninverse(d,v):
    return weightedknn(d,v, weightf = inverseweight)

def dividedata(data,test = 0.05):
    trainset = []
    testset = []
    for row in data:
        if random() < test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset

def testalgorithm(algf,trainset,testset):
    error = 0.0
    for row in testset:
        guess = algf(trainset,row['input'])
        error += (row['result']-guess)**2
    return error / len(testset)

# numpredict.crossvalidate(numpredict.knnestimate,data)
# numpredict.crossvalidate(knn3,data)
# numpredict.crossvalidate(knn1,data)
# numpredict.crossvalidate(numpredict.weightedknn,data)
def crossvalidate(algf,data,trials = 100,test = 0.1):
    error = 0.0
    for i in range(trials):
        trainset,testset = dividedata(data,test)
        error += testalgorithm(algf,trainset,testset)
    return error / trials

# import optimization
# import numpredict
# data = numpredict.wineset2()
# costf=numpredict.createcostfunction(numpredict.knnestimate,data
# optimization.annealingoptimize(numpredict.weightdomain,costf,step=4)
# optimization.geneticoptimize(numpredict.weightdomain,costf,popsize=5)
def createcostfunction(algf, data):
    def costf(scale):
        sdata = rescale(data, scale)
        return crossvalidate(algf, sdata, trials = 10)
    return costf

# data = numpredict.wineset3()
# numpredict.probguess(data,[99,20],40,80)
# numpredict.probguess(data,[99,20],80,120)
def probguess(data, vec1, low, high, k = 5, weightf = gaussian):
    dlist = getdistances(data, vec1)
    nweight = 0.0
    tweight = 0.0

    for i in range(k):
        dist = dlist[i][0]
        idx = dlist[i][1]
        weight = weightf(dist)
        v = data[idx]['result']

        # Is this point in the range?
        if v >= low and v <= high:
            nweight += weight
        tweight += weight
    if tweight == 0: return 0

    # The probability is the weights in the range divided by all the weights
    return nweight/tweight

# data = numpredict.wineset3()
# numpredict.cumulativegraph(data,(1,1),6)
def cumulativegraph(data,vec1,high,k = 5,weightf = gaussian):
    t1 = arange(0.0,high,0.1)
    cprob = array([probguess(data,vec1,0,v,k,weightf) for v in t1])
    plot(t1, cprob)
    show()
