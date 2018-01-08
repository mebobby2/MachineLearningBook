import re
import math
import sqlite3 as sqlite

# import docclass
# cl=docclass.fisherclassifier(docclass.getwords)
# cl.setdb('test1.db')
# docclass.sampletrain(cl)
# cl2=docclass.naivebayes(docclass.getwords)
# cl2.setdb('test1.db')
# cl2.classify('quick money')

def getwords(doc):
    splitter = re.compile('\\W*')
    # Split the words by non-alpha characters
    words = [s.lower() for s in splitter.split(doc)
             if len(s) > 2 and len(s) < 20]

    # Return the unique set of words only
    return dict([(w,1) for w in words])

def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')

# import docclass
# cl=docclass.classifier(docclass.getwords)
# docclass.sampletrain(cl)
# cl.fprob('quick','good')

# Using weighted probability for better results with features (words)
# the classifier has not seen yet

# cl.weightedprob('money','good',cl.fprob)

class classifier:
    def __init__(self, getfeatures, filename=None):
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures

    def setdb(self, dbfile):
        self.con = sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature, category, count)')
        self.con.execute('create table if not exists cc(category, count)')

    # Increase the count of a feature/category pair
    def incf(self, f, cat):
        count = self.fcount(f, cat)
        if count == 0:
            self.con.execute("insert into fc values ('%s', '%s', 1)" % (f, cat))
        else:
            self.con.execute("update fc set count=%d where feature = '%s' and category = '%s'" % (count+1, f, cat))

    # Increase the count of a category
    def incc(self, cat):
        count = self.catcount(cat)
        if count == 0:
            self.con.execute("insert into cc values ('%s', 1)" % (cat))
        else:
            self.con.execute("update cc set count=%d where category = '%s'" % (count+1, cat))


    # The number of times a feature has appeared in a category
    def fcount(self, f, cat):
        res = self.con.execute('select count from fc where feature="%s" and category = "%s"' % (f, cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])

    # The number of items in a category
    def catcount(self, cat):
        res = self.con.execute('select count from cc where category = "%s"' % (cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])

    # The total number of items
    def totalcount(self):
        res = self.con.execute('select sum(count) from cc').fetchone();
        if res == None: return 0
        return res[0]

    # The list of all categories
    def categories(self):
        cur = self.con.execute('select category from cc')
        return [d[0] for d in cur]

    def train(self, item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f, cat)

        # Increment the count for this category
        self.incc(cat)

        self.con.commit()

    # This is called conditional probability, and is usually written as Pr(A | B)
    # and spoken 'the probability of A given B'. In this example, the numbers
    # you have now are Pr(word | classification); that is, for a given
    # classification you calculate the probabil- ity that a particular word
    # appears.
    def fprob(self, f, cat):
        if self.catcount(cat) == 0: return 0
        # The total number of times this feature appeared in this
        # category divided by the total number of items in this category
        return self.fcount(f, cat) / self.catcount(cat)

    # Returns a weighted average
    def weightedprob(self, f, cat, prf, weight = 1.0, ap = 0.5):
        # Calculate current probability
        basicprob = prf(f, cat)

        # Count the number of times this feature has appeared in all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])

        # Calculate the weighted average
        bp = ((weight*ap) + (totals*basicprob))/(weight+totals)
        return bp

# cl=docclass.naivebayes(docclass.getwords)
# docclass.sampletrain(cl)
# cl.prob('quick rabbit','good')
# cl.prob('quick rabbit','bad')

# cl.setthreshold('bad',3.0)
# cl.classify('quick rabbit',default='unknown')

# for i in range(10): docclass.sampletrain(cl)
# cl.classify('quick rabbit',default='unknown')

class naivebayes(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.thresholds = {}

    def docprob(self, item, cat):
        features = self.getfeatures(item)

        # Multiply the probabilites of all the features together
        p=1
        for f in features: p*=self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob*catprob

    def classify(self, item, default = None):
        probs = {}
        # Find the category with the highest probability

        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat == best: continue
            if probs[cat]*self.getthreshold(best) > probs[best]: return default
        return best


    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

# import docclass
# cl=docclass.fisherclassifier(docclass.getwords) >>> docclass.sampletrain(cl)
# docclass.sampletrain(cl)
# cl.cprob('quick','good')
# cl.cprob('money','bad')

# cl.fisherprob('quick rabbit','good')
# cl.fisherprob('quick rabbit','bad')

# cl.classify('quick rabbit')
# cl.classify('quick money')
# cl.setminimum('bad',0.8)
# cl.setminimum('good',0.4)
# cl.classify('quick money')

# To account for overestimating probabilities due to small training data set, we use the weighted probability.
# Weighted probability starts all probabilities at 0.5 and allows them to move toward other probabilities as the class is trained
# cl.weightedprob('money','bad',cl.cprob)
class fisherclassifier(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.minimums = {}

    def cprob(self, f, cat):
        # The frequency of this feature in this category
        clf = self.fprob(f, cat)
        if clf == 0: return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divided by the overall frequency
        p = clf/freqsum

        return p

    def fisherprob(self, item, cat):
        # Multiplying all the probabilities together
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))

        # Take the natural log and multiply by -2
        fscore =- 2*math.log(p)

        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore, len(features) * 2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2): # // operator is Floor division - division that results into whole number adjusted to the left in the number line
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default = None):
        # Lopp through looking for the best resutl
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            # Make sure it exceeds its minimum
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best

    def setminimum(self, cat, min):
        self.minimums[cat] = min

    def getminimum(self, cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]
