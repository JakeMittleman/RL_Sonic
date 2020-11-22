class NodeGene:

    def __init__(self, inputs=None, hidden_nodes=None, outputs=None):
        if outputs is None:
            outputs = []
        if hidden_nodes is None:
            hidden_nodes = []
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.hidden_nodes = hidden_nodes
        self.outputs = outputs

    def add_input(self, input_node):
        self.inputs.append(input_node)

    def add_hidden_node(self, hidden_node):
        self.hidden_nodes.append(hidden_node)

    def add_output(self, output):
        self.outputs.append(output)