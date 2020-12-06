import networkx as nx
import matplotlib.pyplot as plt

"""
    A function for taking a genome and printing it to a picture.
"""
def saveGenomeToFile(genome, show=False, filename='savedGenome.png'):
    G = nx.DiGraph()
    G.add_nodes_from(list(map(lambda x: x.id, genome.node_genes)))
    G.add_edges_from(list(map(lambda x: (x.in_node.id, x.out_node.id),
                              list(filter(lambda y: y.enabled, genome.connection_genes)))))
    nx.draw(G, with_labels=True, node_color="r")
    plt.savefig(filename)
    plt.close()
    if show:
        plt.show()