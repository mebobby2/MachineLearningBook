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
