# MachineLearningBook

## How to run code (example)
1. Navigate to directory, eg cd path/recommendations
2. python
3. from mockdelicious import *
4. get_popular('devops')
5. exit()

## Notes

### User based or item based filtering

Item-based filtering is significantly faster than user-based when getting a list of rec- ommendations for a large dataset, but it does have the additional overhead of main- taining the item similarity table. Also, there is a difference in accuracy that depends on how “sparse” the dataset is. In the movie example, since every critic has rated nearly every movie, the dataset is dense (not sparse). On the other hand, it would be unlikely to find two people with the same set of del.icio.us bookmarks—most book- marks are saved by a small group of people, leading to a sparse dataset. Item-based filtering usually outperforms user-based filtering in sparse datasets, and the two per- form about equally in dense datasets.

## Source code for book
https://github.com/arthur-e/Programming-Collective-Intelligence

## Upto

Upto page 51

Exercises