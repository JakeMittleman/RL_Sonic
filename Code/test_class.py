from node_gene import NodeGene
from genome import Genome
from visualization import *

OUTPUT = "../output/"

def test_cross():
    innovation = 1
    testNode1 = NodeGene('input', 1)
    testNode2 = NodeGene('input', 2)
    testNode3 = NodeGene('input', 3)
    testNode4 = NodeGene('output', 4)
    testNode5 = NodeGene('hidden', 5)
    testNode6 = NodeGene('hidden', 6)

    parentA = Genome(node_genes=[testNode1, testNode2, testNode3, testNode4])
    parentB = Genome(node_genes=[testNode1, testNode2, testNode3, testNode4])
    parentA.add_connection(testNode1, testNode4, innovation)
    parentB.add_connection(testNode1, testNode4, innovation)
    innovation += 1
    parentA.add_connection(testNode2, testNode4, innovation)
    parentB.add_connection(testNode2, testNode4, innovation)
    innovation += 1
    parentA.add_connection(testNode3, testNode4, innovation)
    parentB.add_connection(testNode3, testNode4, innovation)
    innovation += 1
    parentA.add_node(testNode5, parentA.get_connection(testNode2, testNode4), innovation)
    parentB.add_node(testNode5, parentB.get_connection(testNode2, testNode4), innovation)
    innovation += 1
    parentB.add_node(testNode6, parentB.get_connection(testNode5, testNode4), innovation)
    innovation += 1
    parentB.add_connection(testNode3, testNode5, innovation)
    innovation += 1
    parentB.add_connection(testNode1, testNode6, innovation)
    saveGenomeToFile(parentA, filename=OUTPUT + "test_cross_parentA.png")
    saveGenomeToFile(parentB, filename=OUTPUT + "test_cross_parentB.png")

    new_genome = parentA.cross(parentB)

    saveGenomeToFile(new_genome, filename=OUTPUT + "test_cross_newGene.png")


def test_visualization():
    innovation = 1
    testNode1 = NodeGene('input', 1)
    testNode2 = NodeGene('hidden', 2)
    testNode3 = NodeGene('output', 3)

    gene = Genome(node_genes=[testNode1, testNode2, testNode3])
    gene.add_connection(testNode1, testNode2, innovation)
    gene.add_connection(testNode2, testNode3, innovation+1)
    saveGenomeToFile(gene, filename=OUTPUT + "testGenome.png")


def main():

    test_visualization()
    test_cross()

main()
