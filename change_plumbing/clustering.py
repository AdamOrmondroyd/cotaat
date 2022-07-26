import numpy as np
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


def custom_cluster(
    position_matrix,
):
    print("started clustering", flush=True)
    amount_initial_centers = 1
    initial_centers = kmeans_plusplus_initializer(
        position_matrix, amount_initial_centers
    ).initialize()

    xmeans_instance = xmeans(position_matrix, initial_centers, 8, ccore=False)
    xmeans_instance.process()
    clusters = xmeans_instance.get_clusters()
    cluster_list = np.zeros(len(position_matrix))
    for i, cluster in enumerate(clusters):
        cluster_list[cluster] = i
    print("finished clustering", flush=True)
    return cluster_list
