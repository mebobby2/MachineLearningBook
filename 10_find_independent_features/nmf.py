from numpy import *

# There are many ways to measure the 'difference' between matrices
# We use the sum of the squares of the differences between them in this case
def difcost(a, b):
    dif = 0
    # Loop over every row and column in the matrix
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
          # Add together the differences
          dif += pow(a[i,j] - b[i,j], 2)
    return dif
