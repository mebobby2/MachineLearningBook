from pylab import *
from xml.dom.minidom import parseString
from urllib2 import urlopen, quote

class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]
        self.match = int(row[len(row) - 1])

# import advancedclassify
# agesonly=advancedclassify.loadmatch('agesonly.csv',allnum=True)
# matchmaker=advancedclassify.loadmatch('matchmaker.csv')
# advancedclassify.plotagematches(agesonly)
# avgs = advancedclassify.lineartrain(agesonly)
# advancedclassify.dpclassify([30,30],avgs)
def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','), allnum))
    return rows

def plotagematches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1],\
               [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0],\
               [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, 'bo')
    plot(xdn, ydn, 'b+')

    show()

def lineartrain(rows):
    averages={}
    counts={}

    for row in rows:
        # Get the class of this point
        cl=row.match

        averages.setdefault(cl,[0.0]*(len(row.data)))
        counts.setdefault(cl,0)

        # Add this point to the averages
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])

        # Keep track of how many points in each class
        counts[cl]+=1

    # Divide sums by counts to get the averages
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[cl]

    return averages

def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])

def dpclassify(point,avgs):
    b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b

    if y>0: return 0
    else: return 1

def yesno(v):
    if v == 'yes': return 1
    elif v == 'no': return -1
    else: return 0

def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x += 1
    return x

googlekey = 'AIzaSyBP-oqiisRzBpHEj7GMDov_yHLlsUzrdf4'
loc_cache = {}
def getlocation(address):
    if address in loc_cache: return loc_cache[address]
    data = urlopen('https://maps.googleapis.com/maps/api/geocode/xml?address=%s&key=%s' % (quote(address), googlekey)).read()
    doc = parseString(data)
    lat = doc.getElementsByTagName('lat')[0].firstChild.nodeValue
    long = doc.getElementsByTagName('lng')[0].firstChild.nodeValue
    loc_cache[address] = (float(lat), float(long))
    return loc_cache[address]


def milesdistance(a1, a2):
    lat1, long1 = getlocation(a1)
    lat2, long2 = getlocation(a2)
    latdif = 69.1 * (lat2 - lat1)
    longdif = 53.0 * (long2 - long1)
    return (latdif ** 2 + longdif ** 2) ** .5

def loadnumerical():
    oldrows = loadmatch('matchmaker.csv')
    newrows = []
    for row in oldrows:
        d = row.data
        data=[float(d[0]),yesno(d[1]),yesno(d[2]),
              float(d[5]),yesno(d[6]),yesno(d[7]),
              matchcount(d[3],d[8]),
              milesdistance(d[4],d[9]),
              row.match]
        newrows.append(matchrow(data))
    return newrows

def scaledata(rows):
    low = [999999999.0] * len(rows[0].data)
    high = [-999999999.0] * len(rows[0].data)

    # Find the lowest and highest values
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i] < low[i]: low[i] = d[i]
            if d[i] > high[i]: high[i] = d[i]

    # Create a function that scales data
    def scaleinput(d):
        # finds the lowest value and subtracts that amount from
        # all the values to bring the range to a 0 starting point.
        # It then divides the values by the difference between the
        # lowest and highest values to convert them all to values
        # between 0 and 1
        return [(d[i] - low[i]) / (high[i] - low[i])
                 for i in range(len(low))]

    # Scale all the data
    newrows = [matchrow(scaleinput(row.data) + [row.match])
               for row in rows]

    # Return the new data and the function
    return newrows, scaleinput
