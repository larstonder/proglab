#!/usr/bin/env python3

"""The main entry point for testing and visualizing different dimension reduction algorithm"""

import numpy as np
import matplotlib.pyplot as plt
from tsne import TSNE
from isomap import IsoMap
from pca import PCA

def read_csv(filename, sep=","):
    """Reads the content of a csv into a numpy matrix. Each line becomes a row"""
    with open("data/" + filename) as fil:
        return np.array([[float(x) for x in line.strip().split(sep)] for line in fil.readlines()])

# All data in data/ folder
DATASETS = [("swiss_data.csv", None), ("digits.csv", "digits_label.csv")]

# The different algos for dimension reduction
REDUCERS = {

    "ISOMAP": IsoMap(),
    "PCA": PCA(),
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

    if labels is not None:
        options = {
            'c': labels,
            'cmap': 'tab10'
        }
    else:
        options = {
            'c': range(len(dataset)),
            'cmap': 'rainbow'
        }

    global maxSeen
    maxSeen = 0.002
    def draw_callback(iteration, reduced):
        global maxSeen

        maxSeen = np.amax(np.abs(reduced), initial=maxSeen)

        figure, axes = plt.subplots(figsize=(8,8))
        scatter = axes.scatter(reduced[:,0], reduced[:,1], **options)
        axes.set_xlim((-maxSeen*1.1, maxSeen*1.1))
        axes.set_ylim((-maxSeen*1.1, maxSeen*1.1))
        if labels is not None:
            legend1 = axes.legend(*scatter.legend_elements())
            axes.add_artist(legend1)
        figure.savefig(f"images/k15/{iteration:04d}.png")
        return figure

    reducer.reduce_dimensions(dataset, draw_callback)

if __name__ == "__main__":
    main()
