#!/usr/bin/env python3

"""The main entry point for testing and visualizing different dimension reduction algorithm"""

import numpy as np
import matplotlib.pyplot as plt

from tsne import TSNE
from isomap import IsoMap

def read_csv(filename, sep=","):
    """Reads the content of a csv into a numpy matrix. Each line becomes a row"""
    with open("data/" + filename) as fil:
        return np.array([[float(x) for x in line.strip().split(sep)] for line in fil.readlines()])

# All data in data/ folder
DATASETS = [("swiss_data.csv", None), ("digits.csv", "digits_label.csv")]

# The different algos for dimension reduction
REDUCERS = {
    "PCA": None,
    "ISOMAP": IsoMap(),
    "T-SNE": TSNE()
}

def main():
    """The main function, entry point of the program"""
    print("Welcome to PLab 6 visualization")

    print("Pick your dataset: ")
    for index, datalabel in enumerate(DATASETS):
        data, label = datalabel
        print(f" {index+1} - {data}", " (with labels)" if label is not None else "")

    selected = int(input("Choice: "))

    data, label = DATASETS[selected-1]
    dataset = read_csv(data)
    labels = read_csv(label)[:,0] if label is not None else None

    print("Pick your dimension reduction: ")

    for key, value in REDUCERS.items():
        print(f" {key} - {value.get_description() if value is not None else 'TODO'}")

    selected = input("Choice: ").strip().upper()
    reducer = REDUCERS[selected]

    reduced = reducer.reduce_dimensions(dataset)

    if labels is not None:
        options = {
            'c': labels,
            'cmap': 'tab10'
        }
    else:
        options = {
            'c': range(len(reduced)),
            'cmap': 'rainbow'
        }

    _, axes = plt.subplots()
    scatter = axes.scatter(reduced[:,0], reduced[:,1], **options)
    if labels is not None:
        legend1 = axes.legend(*scatter.legend_elements())
        axes.add_artist(legend1)
    plt.show()


if __name__ == "__main__":
    main()
