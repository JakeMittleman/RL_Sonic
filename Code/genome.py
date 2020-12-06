import random
from connection_gene import ConnectionGene


class Genome:

    def __init__(self, connection_genes=None, node_genes=None):
        """
        :param connection_genes: a list of ConnectionGene objects
        """
        if connection_genes is None:
            connection_genes = []
        if node_genes is None:
            node_genes = []
        self.connection_genes = connection_genes
        self.node_genes = node_genes

    def add_connection(self, in_node, out_node, innovation):
        """
        Add a new connection gene with a random weight connecting two previously unconnected nodes.
        :param in_node: the parent node
        :param out_node: the child node
        :param innovation: the innovation
        :return: the new connection
        """

        if in_node.type == "output" or out_node.type == "input" or (in_node.type == out_node.type) or \
                not (in_node in self.node_genes and out_node not in self.node_genes):
            return

        for connection_gene in self.connection_genes:
            if connection_gene.in_node == in_node and connection_gene.out_node == out_node:
                return

        # NEAT paper says the new connection gene gets a random weight
        new_connection = ConnectionGene(in_node, out_node, random.random(), innovation=innovation)
        self.connection_genes.append(new_connection)
        return new_connection

    # TODO: Do we want to ask the user to provide the connection gene or the in_node and out_node?
    #  My instinct is the connection but I could see an argument made for the in/out nodes
    def add_node(self, node, connection, innovation):
        """
        This severs a connection between two nodes (disables it) and creates two connection genes. One from the old
        connection's parent to this new node and one from this new node to the old connection's child.
        Here's an example:
        A ---> B
        new node = C
        new connections: A --> C --> B
        :param node: the node to splice into a connection
        :param connection: the connection to be disabled.
        :param innovation: the new innovation number
        :return: nothing
        """

        # 0) Check if the connection exists in our genome?
        if connection not in self.connection_genes:
            return
        # 1) Disable the old connection
        connection.enabled = False
        # 2) Get the in_node and out_node
        in_node = connection.in_node
        out_node = connection.out_node
        # 3) Make a connection genome from in_node -> node with a weight of 1
        # TODO: change these innovation numbers
        in_connection = ConnectionGene(in_node, node, 1.0, True, innovation=innovation)
        # 4) Make a connection genome from node -> out_node with weight of the old connection
        out_connection = ConnectionGene(node, out_node, connection.weight, innovation=innovation+1)
        self.connection_genes.append(in_connection)
        self.connection_genes.append(out_connection)
        self.node_genes.append(node)

        return in_connection, out_connection

    def merge(self, parent2):
        """
        This method takes two parent genomes (or just two genomes that will eventually become parents)
        and merges them into one genome.
        :param parent2: other genome to merge with this genome
        :return: a new genome merged from parent1 and parent2
        """

        # Any connections labeled as DISABLED (even if the other genome has an enabled connection) remains
        # disabled in the returned child genome

        raise NotImplementedError("This method is not implemented")

    def get_compatibility_distance(self, genome2, c1, c2, c3, N):
        """
        Formula: δ = (c1E / N) + (c2D / N) + c3 * ~W
        E: Total number of excess genes (Connection Genes where the innovation number
                                        > max innovation number in other genome)
        D: Total number of disjoint genes (Connection Genes where the innovation number is < max innovation number in
                                            other genome but doesn't have a match)
        N: Number of genes in larger genome (Note: Can be 1 if genomes are small I.E. < 20 genes)
        C1, C2, C3: Constants that we choose

        :param genome2: the other genome to check compatibility distance
        :return: the commpatibility distance
        """

        E = self.count_excess_genes(genome2)
        D = self.count_disjoint_genes(genome2)
        W = self.get_average_weight_diff(genome2)

        return ((c1 * E) / N) + ((c2 * D) / N) + c3 * W

    def get_matching_genes(self, genome2):

        inno_nums_p1 = list(map(lambda x: x.innovation, self.connection_genes))
        inno_nums_p2 = list(map(lambda x: x.innovation, genome2.connection_genes))

        all_nums = set(inno_nums_p1).intersection(set(inno_nums_p2))

        matches = {num: [] for num in all_nums}

        for connection_gene in self.connection_genes:
            if connection_gene.innovation in all_nums:
                matches[connection_gene.innovation].append(connection_gene)

        for connection_gene in genome2.connection_genes:
            if connection_gene.innovation in all_nums:
                matches[connection_gene.innovation].append(connection_gene)

        return matches

    def get_average_weight_diff(self, genome2):

        matching_genes = list(self.get_matching_genes(genome2).values())

        # total_weight / num_matches

        total_weight = 0

        for match in matching_genes:
            total_weight += abs(match[0].weight - match[1].weight)

        return total_weight / len(matching_genes)

    def get_max_innovation_num(self):
        return self.connection_genes[-1].innovation if self.connection_genes else 0

    def count_excess_genes(self, genome2):
        """
        counts number of excess genes
        :param genome2: the other genome
        :return: number of excess genes
        """

        max_innovation_p1 = self.get_max_innovation_num()
        max_innovation_p2 = genome2.get_max_innovation_num()

        if max_innovation_p1 == 0:
            return len(genome2.connection_genes)
        elif max_innovation_p2 == 0:
            return len(self.connection_genes)

        num_excess = 0

        if max_innovation_p1 > max_innovation_p2:
            for i in range(len(self.connection_genes)-1, -1, -1):
                if self.connection_genes[i].innovation > max_innovation_p2:
                    num_excess += 1
                else:
                    break

        elif max_innovation_p2 > max_innovation_p1:
            for i in range(len(genome2.connection_genes) - 1, -1, -1):
                if genome2.connection_genes[i].innovation > max_innovation_p1:
                    num_excess += 1
                else:
                    break

        return num_excess

    def count_disjoint_genes(self, genome2):
        """
        count number of disjoint genes
        :param genome2: the other genome
        :return: number of disjoint genes
        """

        inno_nums_p1 = list(map(lambda x: x.innovation, self.connection_genes))
        inno_nums_p2 = list(map(lambda x: x.innovation, genome2.connection_genes))

        p1_max = max(inno_nums_p1)
        p2_max = max(inno_nums_p2)

        num_disjoint = 0

        all_nums = set(inno_nums_p1 + inno_nums_p2)

        for num in all_nums:
            if (((num not in inno_nums_p1 and num in inno_nums_p2) or (num in inno_nums_p1 and num not in inno_nums_p2))
                  and num <= min(p1_max, p2_max)):

                num_disjoint += 1

        return num_disjoint
