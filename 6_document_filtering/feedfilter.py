import feedparser
import re

# import feedfilter
# import docclass
# cl=docclass.fisherclassifier(docclass.getwords)
# cl.setdb('python_feed.db')
# feedfilter.read('python_search.xml',cl)


# Takes a filename of URL of a blog feed and classifies the entries
def read(feed, classifier):
    # Get the feed entries and loop over them
    f = feedparser.parse(feed)
    for entry in f['entries']:
        print
        print '-----'
        # Print the contents of the entry
        print 'Title:     '+entry['title'].encode('utf-8')
        print 'Publisher: '+entry['publisher'].encode('utf-8')
        print
        print entry['summary'].encode('utf-8')

        # Combine all the text to create one item for the classifier
        fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

        # Print the best guess at the current category
        print 'Guess: '+str(classifier.classify(entry))

        # Ask the user to specify the correct category and train on that
        cl = raw_input('Enter category: ')
        classifier.train(entry, cl)

# import feedfilter
# import docclass
# cl=docclass.fisherclassifier(feedfilter.entryfeatures)
# cl.setdb('python_feed.db')
# feedfilter.read('python_search.xml',cl)
def entryfeatures(entry):
    splitter = re.compile('\\W*')
    f = {}

    # Extract the title words and annotate
    titlewords = [s.lower() for s in splitter.split(entry['title'])if len(s) > 2 and len(s) < 20]
    for w in titlewords: f['Title:'+w] = 1

    # Extract the summary words
    summarywords = [s.lower() for s in splitter.split(entry['summary'])if len(s) > 2 and len(s) < 20]

    # Count the uppercase words
    uc = 0
    for i in range(len(summarywords)):
        w = summarywords[i]
        f[w] = 1
        if w.isupper(): uc += 1

        # Get words pairs in summary as features
        if i > len(summarywords) - 1:
            twowords = ' '.join(summarywords[i:i+1])
            f[twowords] = 1

    # Kepp creator and publisher whole
    f['Publisher:'+entry['publisher']] = 1

    # UPPSERCASE is a virtual word flagging too much shouting
    if float(uc)/len(summarywords) > 0.3: f['UPPERCASE'] = 1

    return f


