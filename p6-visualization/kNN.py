
"""Implementation of k-nearest neighbours"""

import numpy as np

def pairwise_squared_dist(dataset):
    """Finds the pairwise squared euclidian distances between the points in the dataset"""
    dataset_sqrd = np.square(dataset)
    sums = np.sum(dataset_sqrd, axis=1, keepdims=True)
    dist_sqrd = sums.T + sums - 2*(dataset @ dataset.T)
    return np.abs(dist_sqrd)

def k_nearest(dataset, k):
    """Takes a numpy array with each row being a datapoint,
    returns a matrix with pairwise distances.
    Will only keep the k shortest distances for each datapoint.
    Keep in mind it is not symmetric.
    result[i][j] is non-0 iff j is among the k nearest to i"""

    numpoints = len(dataset)

    # The squared distances, taken from piazza
    print("\t-kNN: Calculating all pairwise distances")
    dist = np.sqrt(pairwise_squared_dist(dataset))
    assert dist.shape == (numpoints,numpoints)

    print("\t-kNN: Keeping only the k shortest")
    # We actually keep the k+1 shortest, since we count i-i as a distance (0 of course)
    for i in range(numpoints):
        dist[i][np.argpartition(dist[i], k+1)[k+1:]]=0

    return dist

def symmetric_binary_k_nearest(dataset, k):
    """Makes a comutative neighbour matrix where
    result[i][j]=1 iff j is among the k nearest neighbours of i, or vice versa"""

    dist = k_nearest(dataset, k)
    dist = dist != 0 # Make the matrix binary
    dist |= dist.T # Make the matrix symmetric
    return np.where(dist, 1, 0) # Return numeric boolean
