# MachineLearningBook

## How to run code (example)
1. Navigate to directory, eg cd path/recommendations
2. python
3. from mockdelicious import *
4. get_popular('devops')
5. exit() or CTR-D
6. To run a python script: python script.py
7. To install a packege: python -m pip install feedparser

## Installing Packages

Use pip to install packages you need.

```which python``` on my machine gives ```/usr/local/bin/python```.
/usr/bin/python is the executable for the python that comes with OS X. /usr/local/lib is a location for user-installed programs only, possibly from Python.org or Homebrew.

When you use ```pip install package_name``` you are installing it for the /usr/bin/python version (since the default system pip is probably the one specified in your $PATH), so when you run your python script and it loads a package, you will get a load error. Since your default python is now set to ```/usr/local/bin/python```.

In order to make sure you use the pip associated with a particular python, you can run ```python -m pip install package_name```, or go look at what the pip on your path is, or is symlinked to. This will install the package into ```usr/local/lib/python2.7/site-packages``` which is then picked up by ```/usr/local/bin/python```.

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



## Source code for book
https://github.com/arthur-e/Programming-Collective-Intelligence

## Upto

Upto page 70
