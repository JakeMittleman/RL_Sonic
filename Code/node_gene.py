class NodeGene:

    """
    A Node Gene represents a node, with a list of inputs, outputs and hidden nodes.
    The key thing to take away in the node class is that all of the input, output and 
    hidden nodes are not representing any connections - they represent POSSIBLE connections.
    Each is a list of some kind of node that could be connected as either input, output 
    or hidden layer. The input and output probably (TODO: be more certain) refers to the
    genomes input / output.
    The node also needs to have some kind of ID to represent it - this is not the innovation
    number.
    """
    def __init__(self, gene_type, node_id, nodes=None):
        self.type = gene_type.lower()
        self.id = node_id
        self.nodes = nodes if nodes is not None else []

    """
    We're going to need to be able to copy nodes.
    """
    def copy(self):
        return NodeGene(self.type, self.id, self.nodes)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash((self.type, self.id))