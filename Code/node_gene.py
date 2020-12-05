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
    def __init__(self, gene_type, id, inNodes=None, outNodes=None, hiddenNodes=None):
        self.type = gene_type.lower()
        self.id = id
        self.inNodes = inNodes if inNodes is not None else {}
        self.outNodes = outNodes if outNodes is not None else {}
        self.hiddenNodes = hiddenNodes if hiddenNodes is not None else {} 

    """
    We're going to need to be able to copy nodes.
    """
    def copy(self):
        return NodeGene(self.type, self.id, self.inNodes, self.outNodes, self.hiddenNodes)

    """
    String representation, mostly for testing / visualizing.
    """
    def __str__(self):
        return str.format('NodeGene\nId: {}\nType: {}\nInNodes: {}\nOutNodes: {}\nHiddenNodes: {}', self.id, self.type, self.inNodes.values(), self.outNodes.values(), self.hiddenNodes.values())