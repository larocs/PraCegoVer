from collections import defaultdict

import hdbscan
import networkx as nx
import numpy as np
from sklearn.metrics import pairwise_distances
from tqdm import tqdm


def get_clusters(features):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=200,
                                min_samples=10, gen_min_span_tree=True)
    clusterer.fit(features)
    labels = np.asarray(clusterer.labels_)
    np.save("clusters.npy", labels)
    return labels


def group_by_cluster(clusters):
    groups = defaultdict(lambda: [])
    for i, cluster in enumerate(clusters):
        groups[cluster].append(i)

    # split outlier cluster into ~10 sub clusters
    n_slice = 10
    cluster_size = len(groups[-1]) // n_slice
    for i in range(n_slice + 1):
        groups[-(i + 2)] = groups[-1][i * cluster_size:(i + 1) * cluster_size]

    del groups[-1]
    return groups


def deduplicate(image_features, text_features, clusters,
                         threshold_img=0.1, threshold_text=0.1):
    groups = group_by_cluster(clusters)
    dedup_indeces = []
    with open("duplications.json", "w") as file:
        for cluster, example_indices in tqdm.tqdm(groups.items()):
            # computing image distance matrix
            text_dist_matrix = pairwise_distances(text_features[example_indices], metric='cosine')
            img_dist_matrix = pairwise_distances(image_features[example_indices], metric='cosine')

            # creating similarity graph
            G = nx.Graph()
            n = img_dist_matrix.shape[0]
            G.add_nodes_from([example_indices[i] for i in range(n)])

            for i in range(n):
                for j in range(i + 1, n):
                    if np.abs(img_dist_matrix[i][j]) <= threshold_img and \
                            np.abs(text_dist_matrix[i][j]) <= threshold_text:
                        G.add_edge(example_indices[i], example_indices[j])

            assert len(G) == len(example_indices), "Graph has an unexpected number of nodes."
            # save duplications
            for c in nx.connected_components(G):
                file.write(f"{c}\n")
            dedup_indeces.append(c)

    return dedup_indeces
