import networkx as nx
import matplotlib.pyplot as plt

"""
    A function for takinga genome and printing it to a picture.
"""
def saveGenomeToFile(genome, show=False, filename='savedGenome.png'):
    G = nx.DiGraph()
    G.add_nodes_from(genome.node_genes)
    G.add_edges_from(genome.connection_genes)
    nx.draw(G, with_labels=True, node_color="r")
    plt.savefig(filename)
    if show:
        plt.show()