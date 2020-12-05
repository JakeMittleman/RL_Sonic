from node_gene import NodeGene
from genome import Genome
import networkx as nx
import matplotlib.pyplot as plt
from visualization import *

def main():

    testNode1 = NodeGene('input', 1)
    testNode2 = NodeGene('output', 2)
    testNode3 = NodeGene('hidden', 3)

    gene = Genome(node_genes=[testNode1, testNode2, testNode3])
    gene.add_connection(testNode1, testNode2)
    gene.add_connection(testNode2, testNode3)
    saveGenomeToFile(gene, "testGenome.png")

main()
