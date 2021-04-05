import numpy as np
import scipy.linalg as sp
import sklearn.utils.graph_shortest_path as sg
from dimred import DimRed
from kNN import k_nearest

class IsoMap2(DimRed):

    k = 25
    m = 2

    def get_description(self):
        """A Description of the dimensionality reduction algorithm"""
        return """Nonlinear reduction algoritm which computes the datasets geodesics and 
        performs multidimensional scaling to reduce dimensons"""

    def reduce_dimensions(self, dataset):
        """Reduces the dimensions of the dataset"""
        numpoints = len(dataset)
        geodesics = self.__compute_geodesics(dataset, self.k)
        result = self.__MDS(geodesics, numpoints)
        # result = self.__MDS(geodesics, numpoints)
        return(result)

    def __compute_geodesics(self, dataset, k):
        """Takes high-dimensional data and a user specified parameter k as input, and returns a distance
        matrix D, where D_ij is the shortest-path distance between x_i and x_j along the manifold"""
        distance_matrix = k_nearest(dataset, k)
        return sg.graph_shortest_path(distance_matrix)
    
    def __MDS(self, dataset, n):
        """Applies classical multidimensional scaling over a geodesic distance matrix, and returns
        the coordinates of the low-dimensional mapped points y_1 ... y_n"""
        squared_proximity_matrix = np.square(dataset)
        centered = self.__double_centering(squared_proximity_matrix, n)
        eigenvalues, eigenvectors = sp.eigh(centered, eigvals=(n-self.m, n-1))
        l = np.diag(eigenvalues)
        y = np.dot(eigenvectors, l**(1/2))
        return y
    
    def __double_centering(self, squared, n):
        """Performs double centering using centering matrix j, where n is the number of datapoints"""
        identity_matrix = np.identity(n)
        one_vector = np.ones((1, n))
        ones = one_vector.dot(one_vector.T)
        # j = identity_matrix - (1/n) * ones
        j = np.subtract(identity_matrix, np.multiply(1/n, ones))
        # b = -(1/2) * j * squared
        b = np.dot(np.multiply(-(1/2),j), squared)
        return b