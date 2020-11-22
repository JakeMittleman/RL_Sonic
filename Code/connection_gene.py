"""
This class represents a connection between either an input node and a hidden node or
a hidden node and an output node.
Input -> Hidden or Hidden -> Output
"""
class ConnectionGene:

    def __init__(self, in_node=None, out_node=None, weight=0.0, enabled=True, innovation=0):
        """
        :param in_node: the origin of a directed connection between two nodes
        :param out_node: the destination of a directed connection between two nodes
        :param weight: the weight of the connection
        :param enabled: whether or not this connection gene is expressed
        :param innovation: historical markers that identify the original historical ancestor of each gene.
        """
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation
