import numpy as np
# import scipy.sparse.linalg as sp
# import scipy.linalg as sp
import sklearn.utils.graph_shortest_path as sg
from dimred import DimRed
from kNN import k_nearest
from scipy.linalg import eigh
from scipy.sparse.linalg import eigs

class IsoMap(DimRed):

    k = 50
    m = 2

    def get_description(self):
        """A Description of the dimensionality reduction algorithm"""
        return """Nonlinear reduction algoritm which computes the datasets geodesics and 
        performs multidimensional scaling to reduce dimensons"""

    def reduce_dimensions(self, dataset):
        """Reduces the dimensions of the dataset"""
        geodesics = self.__compute_geodesics(dataset)
        result = self.__MDS(geodesics)
        return(result)

    def __compute_geodesics(self, dataset):
        """Takes high-dimensional data and a user specified parameter k as input, and returns a distance
        matrix D, where D_ij is the shortest-path distance between x_i and x_j along the manifold"""
        distance_matrix = k_nearest(dataset, self.k)
        return sg.graph_shortest_path(distance_matrix)
    
    def __MDS(self, dataset):
        """Applies classical multidimensional scaling over a geodesic distance matrix, and returns
        the coordinates of the low-dimensional mapped points y_1 ... y_n"""
        numpoints = np.size(dataset, 0)
        squared_proximity_matrix = np.square(dataset)
        double_centered = self.__double_centering(squared_proximity_matrix, numpoints)
        # eigenvalues, eigenvectors = eigh(double_centered, eigvals=(numpoints-self.m, numpoints-1))
        eigenvalues, eigenvectors = eigs(double_centered, k=self.m)
        l = np.diag(eigenvalues)
        y = eigenvectors @ np.sqrt(l)
        return np.real(y)
    
    def __double_centering(self, squared, n):
        """Performs double centering using centering matrix j, where n is the number of datapoints"""
        identity_matrix = np.identity(n)
        ones = np.ones(squared.shape)
        j = identity_matrix - (1/n) * ones
        b = -(1/2) * j @ squared @ j
        return b