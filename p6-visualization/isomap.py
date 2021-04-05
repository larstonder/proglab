"""Subclass of dimred, performs isometric mapping"""

import numpy as np
import scipy.linalg as sp
import sklearn.utils.graph_shortest_path as sg
from dimred import DimRed
from kNN import k_nearest

class IsoMap(DimRed):
    """Subclass for Dimensionality reduction using isometric mapping"""

    k = 40
    m = 2

    def get_description(self):
        """A Description of the dimensionality reduction algorithm"""
        return """Nonlinear reduction algoritm which computes the datasets geodesics and 
        performs multidimensional scaling to reduce dimensons"""

    def reduce_dimensions(self, dataset):
        """Reduces the dimensions of the dataset"""
        numpoints = len(dataset)
        geodesics_matrix = self.__compute_geodesics(dataset)
        return self.__MDS(geodesics_matrix, numpoints)
    
    def __compute_geodesics(self, dataset):
        """Takes high-dimensial data points and user specified parameter k and returns distance matrix D, 
        where D_ij is the shortest-path distance between x_i and x_j along the manifold"""
        knn_graph = k_nearest(dataset, self.k)
        return sg.graph_shortest_path(knn_graph)
    
    def __MDS(self, dataset, numpoints):
        """Applies classical multidimensional scaling over a geodesic distance matrix, and returns
        the coordinates of the low-dimensional mapped points y_1 ... y_n"""
        # squared = dataset
        # for i in range(numpoints):
        #     for j in range(len(dataset[i])):
        #         squared[i][j] = np.square(dataset[i][j])
    
        squared = np.square(dataset)
        ones = np.empty((numpoints,numpoints,))
        ones[:] = 1
        # centering = np.subtract(np.identity(numpoints), np.multiply((1/numpoints), ones))
        centering = np.subtract(np.identity(numpoints), np.multiply((1/numpoints), np.dot(np.full(1, 1), np.full(1,1).T)))
        double_centering = np.multiply(-(1/2), np.dot(centering, squared))
        # e_values, e_vectors = sp.eigh(double_centering, eigvals=(numpoints-self.m, numpoints-1))
        e_values, e_vectors = np.linalg.eig(double_centering)
        print(np.dot(e_vectors, np.sqrt(np.diag(e_values))))
        return np.dot(e_vectors, np.sqrt(np.diag(e_values)))
