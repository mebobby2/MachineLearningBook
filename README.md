# MachineLearningBook

## How to run code (example)
1. Navigate to directory, eg cd path/recommendations
2. python
3. from mockdelicious import *
4. get_popular('devops')
5. exit() or CTR-D
6. To run a python script: python script.py
7. To install a packege: python -m pip install feedparser

## Run a class
1. Repeat steps 1 and 2 from above
2. import searchengine
3. crawler=searchengine.crawler('db_name')
4. crawler.crawl(pagelist)

## Installing Packages

### Use pip to install packages you need.

```which python``` on my machine gives ```/usr/local/bin/python```.
/usr/bin/python is the executable for the python that comes with OS X. /usr/local/lib is a location for user-installed programs only, possibly from Python.org or Homebrew.

When you use ```pip install package_name``` you are installing it for the /usr/bin/python version (since the default system pip is probably the one specified in your $PATH), so when you run your python script and it loads a package, you will get a load error. Since your default python is now set to ```/usr/local/bin/python```.

In order to make sure you use the pip associated with a particular python, you can run ```python -m pip install package_name```, or go look at what the pip on your path is, or is symlinked to. This will install the package into ```usr/local/lib/python2.7/site-packages``` which is then picked up by ```/usr/local/bin/python```.

### pip on new machines
stick with the default python installation at ```/usr/bin/python```. Do not install another version of python. Install pip by downloading ```wget https://bootstrap.pypa.io/get-pip.py``` and running it with ```sudo python get-pip.py```. When you install a package using pip, use the command ```sudo pip install bs4```. As long as you don't install another verison of python and use the default one that comes with the OS, you don't need any of that funky stuff in the above section.

### pysqlite

As of python version 2.5 and up, a working version of pysqlite 2, bundled as sqlite3, is available from within the language. So you don't need to install it as an external package.

## Notes

### Euclidean vs Pearson

If you are dealing with data where the actual difference in values of attributes is important, go with Euclidean Distance. If you are looking for trend or shape similarity, then go with correlation

In the blogs exercise, some blogs contain more entries or much longer entries than others, and will thus contain more words overall. The Pearson correlation will correct for this, since it really tries to determine how well two sets of data fit onto a straight line.

### Tanimoto coefficient
The Pearson correlation works well for the blog dataset where the values are actual word counts. However, this dataset just has 1s and 0s for presence or absence, and it would be more useful to define some measure of overlap between the people who want two items. For this, there is a measure called the Tanimoto coefficient, which is the ratio of the intersection set (only the items that are in both sets) to the union set (all the items in either set).

```
def tanamoto(v1,v2):
  c1,c2,shr=0,0,0
  for i in range(len(v1)):
    if v1[i]!=0: c1+=1 # in v1
    if v2[i]!=0: c2+=1 # in v2
    if v1[i]!=0 and v2[i]!=0: shr+=1 # in both
  return 1.0-(float(shr)/(c1+c2-shr))
```

This will return a value between 1.0 and 0.0. A value of 1.0 indicates that nobody who wants the first item wants the second one, and 0.0 means that exactly the same set of people want the two items.

### User based or item based filtering

Item-based filtering is significantly faster than user-based when getting a list of recommendations for a large dataset, but it does have the additional overhead of main- taining the item similarity table. Also, there is a difference in accuracy that depends on how “sparse” the dataset is. In the movie example, since every critic has rated nearly every movie, the dataset is dense (not sparse). On the other hand, it would be unlikely to find two people with the same set of del.icio.us bookmarks—most book- marks are saved by a small group of people, leading to a sparse dataset. Item-based filtering usually outperforms user-based filtering in sparse datasets, and the two per- form about equally in dense datasets.

### Supervised vs Unsupervised Learning

Techniques that use example inputs and outputs to learn how to make predictions are known as supervised learning methods. Examples of supervised learning methods include neural networks, decision trees, support-vector machines, and Bayesian filtering.

Clustering is an example of unsupervised learning. Unlike a neural network or a decision tree, unsupervised learning algorithms are not trained with examples of correct answers. Their purpose is to find structure within a set of data where no one piece of data is the answer. In the fashion example where fashion islands are generated from user purchasing data for a retail shop, the clusters don’t tell the retailers what an individual is likely to buy, nor do they make predictions about which fashion island a new person fits into. The goal of clustering algorithms is to take the data and find the distinct groups that exist within it.

### Hierarchical clustering

Hierarchical clustering builds up a hierarchy of groups by continuously merging the two most similar groups. Each of these groups starts as a single item. In each iteration this method calculates the distances between every pair of groups, and the closest ones are merged together to form a new group. This is repeated until there is only one group.

A dendrogram is a visualization of hierarchical clustering.

Some insights derivied from heirarchical clustering: It closely clustered these blogs together: Official google blog, search engine roundtable, google operating system, google blogoscoped.

### Column clustering
It’s often necessary to cluster on both the rows and the columns. In a marketing study, it can be interesting to group people to find demographics and products, or perhaps to determine shelf locations of items that are commonly bought together. In the blog dataset, the columns represent words, and it’s potentially interesting to see which words are commonly used together.

One important thing to realize about clustering is that if you have many more items than variables, the likelihood of nonsensical clusters increases. There are many more words than there are blogs, so you’ll notice more reasonable patterns in the blog clustering than in the word clustering.

Some insights derivied from column clustering: these words formed a cluster, meaning, they were mentioned the same number of times across all blogs.
1. iraq, war
2. president, bush
3. national, government, against
4. 1, 2, and 3 all formed a larger cluster

### K-Means Clustering

Hierarchical clustering gives a nice tree as a result, but it has a couple of disadvan- tages. The tree view doesn’t really break the data into distinct groups without additional work, and the algorithm is extremely computationally intensive. Because the relationship between every pair of items must be calculated and then recalculated when items are merged, the algorithm will run slowly on very large datasets.

An alternative method of clustering is K-means clustering. This type of algorithm is quite different from hierarchical clustering because it is told in advance how many distinct clusters to generate. The algorithm will determine the size of the clusters based on the structure of the data.

Some insights derived from k-means:
The blogs were all found to be in one cluster:
'Publishing 2.0', 'GigaOM', "John Battelle's Searchblog", 'Google Operating System', 'Valleywag', 'Search Engine Watch Blog', 'Techdirt', 'Official Google Blog', 'Search Engine Roundtable', 'PaulStamatiou.com', 'A Consuming Experience (full feed)', 'Matt Cutts: Gadgets, Google, and SEO', 'Google Blogoscoped', 'Read/WriteWeb'

### Multidimensional Scaling
Used to find a two-dimensional representation of the dataset. Since most real-life examples of items you would want to cluster have more than two numbers, you can’t just take the data as-is and plot it in two dimensions. However, to understand the relationship between the various items, it would be very useful to see them charted on a page with closer distances indicating similarity.

The concept of imagining items in space depending on their parameters will be a recurring theme in this book. Using multidimensional scaling is an effective way to take a dataset and actually view it in a way that’s easy to interpret. It’s important to realize that some information is lost in the process of scaling, but the result should help you understand the algorithms better.

### Content-Based Ranking for search results
A score for a search item result is calculated based on 3 metrics:
Word frequency - The number of times the words in the query appear in the document can help determine how relevant the document is.
Document location - The main subject of a document will probably appear near the beginning of the document.
Word distance - If there are multiple words in the query, they should appear close together in the document.

### Inbound Links to rank search results
Content-Based Ranking metrics have all been based on the content of the page. Although many search engines still work this way, the results can often be improved by considering information that others have provided about the page, specifically, who has linked to the page and what they have said about it. This is particularly useful when indexing pages of dubious value or pages that might have been created by spammers, as these are less likely to be linked than pages with real content.

### Stochastic Optimization
Optimization techniques are typically used in problems that have many possible solutions across many variables, and that have outcomes that can change greatly depending on the combinations of these variables.

Optimization finds the best solution to a problem by trying many different solutions and scoring them to determine their quality. Optimization is typically used in cases where there are too many possible solutions to try them all.

The cost function is the key to solving any problem using optimization, and it’s usu- ally the most difficult thing to determine.

Whether a particular optimization method will work depends very much on the problem. Simulated annealing, genetic optimization, and most other optimization methods rely on the fact that, in most problems, the best solution is close to other good solutions.

### Maths
#### Number of combinations
Let's say I have six values, A, B, C, D, E, F. And TWO of these values make a valid tuple. How many times/loops do I need to make to find the valid tuple. The formula is I^P, where P = number of possibilities and I = the number of inputs. Hence, 6^2 = 36 loops/combinations we need to look through.


## Source code for book
https://github.com/arthur-e/Programming-Collective-Intelligence

## Upto

Upto page 127

Finally, you’ll need a function that requests the results until there are no more.
