
"""Implementation of t-SNE"""

from time import time
from datetime import datetime
from sys import stdout
import numpy as np

from dimred import DimRed
from kNN import pairwise_squared_dist, symmetric_binary_k_nearest


class TSNE(DimRed):
    """t-SNE implementation class"""

    def __init__(self):
        DimRed.__init__(self)
        self.k = 40
        self.max_iterations = 1000
        self.p_multiplier = lambda x: 4 if x < 100 else 1
        self.alpha = lambda x: 0.5 if x < 250 else 0.8
        self.epsilon = 500
        self.seed = 3

    def get_description(self):
        return "Student t-Distributed Stochastic Neighbor Embedding"

    def reduce_dimensions(self, dataset):
        n = len(dataset)
        print("Dataset size:", n)
        print("Calculating symmetric binary kNN, k:", self.k)
        p = symmetric_binary_k_nearest(dataset, self.k)
        p_sum = p.sum()

        print("Picking random starting values for Y")
        np.random.seed(self.seed)
        Y = np.random.normal(loc=0, scale=10**-4, size=(n, 2))
        g = np.full((n, 2), 1)
        delta = np.full((n, 2), 0)

        start = time()
        print("Starting iteration at:", datetime.now().strftime("%H:%M:%S"))
        for iteration in range(self.max_iterations):
            q = 1 / (1 + pairwise_squared_dist(Y))
            q_sum = q.sum()

            # y_j is a NxN matrix with element i,j = y_j (aka a point)
            # This means the row is "ignored" (all rows are identical)
            y_j = np.array([Y, ] * n)

            # y_i is independent on j, so all columns are equal
            y_i = np.swapaxes(y_j, 0, 1)

            p_mul = self.p_multiplier(iteration)

            p_q_diff = p_mul * p / p_sum - q / q_sum
            p_q_diff_times_q = p_q_diff * q  # (2000,2000)
            p_q_diff_times_q = p_q_diff_times_q.reshape((n, n, 1))
            y_i_j_diff = y_i - y_j  # (2000,2000,2)
            product = p_q_diff_times_q * y_i_j_diff
            gradient = 4 * (product).sum(axis=1)

            g_plus = g + 0.2
            g_times = g * 0.8

            use_plus = np.sign(delta) != np.sign(gradient)
            all_true = np.full((n, 2), True)
            g = np.select([use_plus, all_true], [g_plus, g_times])
            g = np.maximum(g, 0.01)

            delta = self.alpha(iteration) * delta - self.epsilon * g * gradient
            Y = Y + delta

            done = iteration + 1
            if done % 10 == 0:
                time_spent = time() - start
                time_per = time_spent / done
                estimate = (self.max_iterations - done) * time_per
                print(
                    f"\rProgress: {done}/{self.max_iterations}" +
                    f"    [{time_spent:.3f}s]  est {estimate:.0f}s left",
                    end="")
                stdout.flush()

        return Y
