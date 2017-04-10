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

### User based or item based filtering

Item-based filtering is significantly faster than user-based when getting a list of recommendations for a large dataset, but it does have the additional overhead of main- taining the item similarity table. Also, there is a difference in accuracy that depends on how “sparse” the dataset is. In the movie example, since every critic has rated nearly every movie, the dataset is dense (not sparse). On the other hand, it would be unlikely to find two people with the same set of del.icio.us bookmarks—most book- marks are saved by a small group of people, leading to a sparse dataset. Item-based filtering usually outperforms user-based filtering in sparse datasets, and the two per- form about equally in dense datasets.

### Supervised vs Unsupervised Learning

Techniques that use example inputs and outputs to learn how to make predictions are known as supervised learning methods. Examples of supervised learning methods include neural networks, decision trees, support-vector machines, and Bayesian filtering.

Clustering is an example of unsupervised learning. Unlike a neural network or a decision tree, unsupervised learning algorithms are not trained with examples of correct answers. Their purpose is to find structure within a set of data where no one piece of data is the answer. In the fashion example where fashion islands are generated from user purchasing data for a retail shop, the clusters don’t tell the retailers what an individual is likely to buy, nor do they make predictions about which fashion island a new person fits into. The goal of clustering algorithms is to take the data and find the distinct groups that exist within it.

### Hierarchical clustering

Hierarchical clustering builds up a hierarchy of groups by continuously merging the two most similar groups. Each of these groups starts as a single item. In each iteration this method calculates the distances between every pair of groups, and the closest ones are merged together to form a new group. This is repeated until there is only one group.

A dendrogram is a visualization of hierarchical clustering

## Source code for book
https://github.com/arthur-e/Programming-Collective-Intelligence

## Upto

Upto page 63
Column Clustering

