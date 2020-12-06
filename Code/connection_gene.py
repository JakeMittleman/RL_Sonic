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

        """
        This is the historical origin of this gene.
        Every time a new connection gene is created it receives an innovation number of +1.
        My expectation is somewhere we'll maintain a global track of the current innovation. This is probably
        to tell which genes are older and which are newer. Maybe.

        Magnus adds: This is to keep track of which genes should pair with eachother. So when you do crossover,
        you use the innovation number like an ID for pairing (ID: 8 pairs with ID:8 in the other gene.)
        """
        self.innovation = innovation

    """
    We need a way to check for equality between connections (in case, a random connection is the same twice
    in one generations mutation, in which case it should have the same innovation number). Since the innovation
    number might be different, we must check between everything else.
    """

    def __eq__(self, otherConnection):
        # I think this is enough?
        return self.in_node == otherConnection.in_node and self.out_node == otherConnection.out_node

    """
    This will also be needed for crossover.
    """

    def copy(self):
        return ConnectionGene(self.in_node, self.out_node, self.weight, self.enabled, self.innovation)
