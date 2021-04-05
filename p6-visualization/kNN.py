
"""Implementation of k-nearest neighbours"""

import numpy as np

def k_nearest(dataset, k):
    """Takes a numpy array with each row being a datapoint,
    returns a matrix with pairwise squared distances.
    Will only keep the k shortest distances for each datapoint.
    Keep in mind it is not symmetric.
    result[i][j] is non-0 iff j is among the k nearest to i"""

    numpoints = len(dataset)

    # The squared distances
    dist = ((dataset[:, :, None] - dataset[:, :, None].T) ** 2).sum(1)
    # dist = np.sqrt(((dataset[:, :, None] - dataset[:, :, None].T) ** 2).sum(1))
    assert dist.shape == (numpoints,numpoints)

    # for i in range(numpoints):
    #     shortest = [(dist[i][j], j) for j in range(numpoints)]
    #     shortest.sort() # The k shortest come first, the rest will be set to 0
    #     # The shortest array also contains the distance from i to i, so increase k by one
    #     for _,j in shortest[(k+1):]:
    #         dist[i][j] = 0

    # return np.sqrt(dist)

    neighbors = np.zeros_like(dist)
    sort_distances = np.argsort(dist, axis=1)[:, 1:k+1]
    for k,i in enumerate(sort_distances):
        neighbors[k,i] = dist[k,i]
    return np.sqrt(neighbors)

def symmetric_binary_k_nearest(dataset, k):
    """Makes a comutative neighbour matrix where
    result[i][j]=True iff j is among the k nearest neighbours of i, or vice versa"""

    dist = k_nearest(dataset, k)
    dist = dist != 0 # Make the matrix binary
    dist |= dist.T # Make the matrix symmetric
    return dist
