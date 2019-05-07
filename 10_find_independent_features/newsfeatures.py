import feedparser
import re

# import newsfeatures
# allw,artw,artt= newsfeatures.getarticlewords()
# wordmatrix,wordvec= newsfeatures.makematrix(allw,artw)

feedlist = ['http://feeds.reuters.com/reuters/topNews',
            'http://feeds.reuters.com/Reuters/domesticNews',
            'http://feeds.reuters.com/Reuters/worldNews',
            'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
            'http://news.google.com/?output=rss',
            'http://feeds.foxnews.com/foxnews/most-popular',
            'http://feeds.foxnews.com/foxnews/national',
            'http://feeds.foxnews.com/foxnews/world',
            'http://rss.cnn.com/rss/edition.rss',
            'http://rss.cnn.com/rss/edition_world.rss',
            'http://rss.cnn.com/rss/edition_us.rss',
            'https://www.huffpost.com/section/us-news/feed',
            'https://www.huffpost.com/section/world-news/feed',
            'http://rssfeeds.usatoday.com/usatoday-NewsTopStories',
            'http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories',
            'http://rssfeeds.usatoday.com/UsatodaycomWorld-TopStories']


def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c
    return p

def separatewords(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


def getarticlewords():
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0
    # Lopp over every feed
    for feed in feedlist:
        f = feedparser.parse(feed)

        # Loop over every article
        for e in f.entries:
            # Ignore indentical articles
            if e.title in articletitles:
                continue

            # Extract the words
            txt = e.title.encode(
                'utf8')+stripHTML(e.description.encode('utf8'))
            words = separatewords(txt)
            articlewords.append({})
            articletitles.append(e.title)

            # Increase the counts for this word in allwords and in articlewords
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ec += 1
        return allwords, articlewords, articletitles


def makematrix(allw, articlew):
    wordvec = []

    # Only take words that are common but not too common
    for w, c in allw.items():
        if c > 3 and c < len(articlew) * 0.6:
            wordvec.append(w)

    # Create the word matrix
    l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1, wordvec
