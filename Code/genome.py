import random
from connection_gene import ConnectionGene

class Genome:

    def __init__(self, connection_genes=None):
        """
        :param connection_genes: a list of ConnectionGene objects
        """
        if connection_genes is None:
            connection_genes = []
        self.connection_genes = connection_genes

    def add_connection(self, in_node, out_node):
        """
        Add a new connection gene with a random weight connecting two previously unconnected nodes.
        :param in_node: the parent node
        :param out_node: the child node
        :return: nothing
        """

        # TODO: Check if in_node can be connected to out_node.
        #  If in_node=output and out_node=input then it can't be done for example.
        #  For now we're just assuming it's done properly.

        # TODO: Check if in_node and out_node are previously connected (cannot connect 2 connected nodes)

        # NEAT paper says the new connection gene gets a random weight
        self.connection_genes.append(ConnectionGene(in_node, out_node, random.random()))

    # TODO: Do we want to ask the user to provide the connection gene or the in_node and out_node?
    #  My instinct is the connection but I could see an argument made for the in/out nodes
    def add_node(self, node, connection):
        """
        This severs a connection between two nodes (disables it) and creates two connection genes. One from the old
        connection's parent to this new node and one from this new node to the old connection's child.
        Here's an example:
        A ---> B
        new node = C
        new connections: A --> C --> B
        :param node: the node to splice into a connection
        :param connection: the connection to be disabled.
        :return: nothing
        """

        # TODO: Implement this method

        # 0) Check if the connection exists in our genome?
        # 1) Disable the old connection
        # 2) Get the in_node and out_node
        # 3) Make a connection genome from in_node -> node with a weight of 1
        # 4) Make a connection genome from node -> out_node with weight of the old connection
