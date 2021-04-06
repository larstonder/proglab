
"""Implementation of k-nearest neighbours"""

import numpy as np

def k_nearest(dataset, k):
    """Takes a numpy array with each row being a datapoint,
    returns a matrix with pairwise distances.
    Will only keep the k shortest distances for each datapoint.
    Keep in mind it is not symmetric.
    result[i][j] is non-0 iff j is among the k nearest to i"""

    numpoints = len(dataset)

    # The squared distances, taken from piazza
    X = dataset
    XX = np.square(X)
    V = np.sum(XX, axis=1, keepdims=True)
    D_2 = V.T + V - 2*(X @ X.T)
    D_2 = np.abs(D_2)
    dist = np.sqrt(D_2)
    assert dist.shape == (numpoints,numpoints)

    for i in range(numpoints):
        shortest = [(dist[i][j], j) for j in range(numpoints)]
        shortest.sort() # The k shortest come first, the rest will be set to 0
        # The shortest array also contains the distance from i to i, so increase k by one
        for _,j in shortest[(k+1):]:
            dist[i][j] = 0

    return dist

def symmetric_binary_k_nearest(dataset, k):
    """Makes a comutative neighbour matrix where
    result[i][j]=True iff j is among the k nearest neighbours of i, or vice versa"""

    dist = k_nearest(dataset, k)
    dist = dist != 0 # Make the matrix binary
    dist |= dist.T # Make the matrix symmetric
    return dist
