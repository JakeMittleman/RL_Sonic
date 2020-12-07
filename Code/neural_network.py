import math
from genome import Genome
from node_gene import NodeGene
from connection_gene import ConnectionGene
from innovation_tracker import InnovationTracker
import random
import uuid


class NeuralNetwork:

    def __init__(self, genome):
        self.innovation_tracker = genome.innovation_tracker
        self.input_nodes = [x for x in genome.node_genes if x.type == "input"]
        self.output_nodes = [
            x for x in genome.node_genes if x.type == "output"]
        self.node_values = {
            x.id: 0.0 for x in self.input_nodes + self.output_nodes}
        self.hidden_values = {x.id: 0.0 for x in [
            y for y in genome.node_genes if y.type == "hidden"]}
        self.genome = genome

    def activate(self, inputs):
        if len(inputs) != len(self.input_nodes):
            raise RuntimeError("input length:", len(inputs), "!= input_nodes:", len(self.input_nodes))

        for node, input_val in zip(self.input_nodes, inputs):
            self.node_values[node.id] = input_val

        nodes = self.input_nodes[:]
        next_layer = set()
        for node in nodes:
            next_layer.union(self.handle_node_connections(node))

        while next_layer:
            curr_layer = next_layer.copy()
            next_layer = set()

            for in_node in curr_layer:
                value = self.hidden_values[in_node.id]
                self.hidden_values[in_node.id] = self.sigmoid(value)
                next_layer.union(self.handle_node_connections(in_node))

        for out_node in self.output_nodes:
            value = self.node_values[out_node.id]
            self.node_values[out_node.id] = self.sigmoid(value)

        return [self.node_values[out_node.id] for out_node in self.output_nodes]

    def sigmoid(self, value):
        value = max(-60.0, min(60.0, 5.0 * value))
        return 1.0 / (1.0 + math.exp(-value))

    def handle_node_connections(self, node):
        next_layer = set()
        for connection_gene in self.genome.connection_genes:
            if not connection_gene.enabled:
                continue
            in_node = connection_gene.in_node
            out_node = connection_gene.out_node
            weight = connection_gene.weight
            if in_node == node:
                if out_node.type == "output":
                    self.node_values[out_node.id] += self.node_values[in_node.id] * weight

                else:
                    self.hidden_values[out_node.id] += self.node_values[in_node.id] * weight
                    next_layer.add(out_node)

        return next_layer

    @staticmethod
    def create(num_inputs, num_outputs):
        innovation_tracker = InnovationTracker()
        input_genes = []
        output_genes = []
        for i in range(num_inputs):
            input_genes.append(NodeGene("input", i))
        for i in range(num_inputs, num_inputs + num_outputs):
            output_genes.append(NodeGene("output", i))

        connection_genes = []

        for input_node in input_genes:
            for output_node in output_genes:
                if random.random() > 0.5:
                    connection_genes.append(ConnectionGene(input_node, output_node, random.random(),
                                                           enabled=True if random.random() > 0.8 else False,
                                                           innovation=innovation_tracker.get_innovation()))

        genome = Genome(innovation_tracker, connection_genes,
                        input_genes + output_genes)
        return NeuralNetwork(genome)
