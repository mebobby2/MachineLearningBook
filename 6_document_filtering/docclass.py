import re
import math

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

    # Increase the count of a feature/category pair
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # Increase the count of a category
    def incc(self, cat):
        self.cc.setdefault(cat, 0);
        self.cc[cat] += 1

    # The number of times a feature has appeared in a category
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values());

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f, cat)

        # Increment the count for this category
        self.incc(cat)

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
        for f in features: p*self.weightedprob(f, cat, self.fprob)
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