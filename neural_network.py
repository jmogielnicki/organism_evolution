import numpy as np
import matplotlib.pyplot as plt


class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def activate(self, inputs):
        # Compute the weighted sum of the inputs
        weighted_sum = np.dot(self.weights, inputs) + self.bias
        # Apply the activation function
        return self.sigmoid(weighted_sum)

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, hidden_layers, output_layer):
        # Initialize the hidden layers and output layer of the network
        self.hidden_layers = hidden_layers
        self.output_layer = output_layer

    def forward_propagate(self, inputs):
        # Propagate the inputs through the hidden layers
        hidden_outputs = inputs
        for layer in self.hidden_layers:
            new_inputs = []
            for neuron in layer:
                new_inputs.append(neuron.activate(hidden_outputs))
            hidden_outputs = new_inputs

        # Propagate the hidden outputs through the output layer
        outputs = []
        for neuron in self.output_layer:
            outputs.append(neuron.activate(hidden_outputs))

        return outputs

    def visualize(self):
        # Compute the total number of layers in the network, including the input but excluding the output
        num_layers = len(self.hidden_layers) + 1

        # Compute the maximum number of nodes in any layer of the network
        max_nodes = max([len(layer) for layer in self.hidden_layers]
                        ) if self.hidden_layers else 0
        max_nodes = max(max_nodes, len(self.output_layer))

        # Compute the x and y coordinates for each node in the network
        node_coords = []
        for i in range(num_layers):
            # Compute the y coordinate for each node in the current layer
            y = np.linspace(0, 1, max_nodes)
            # Compute the x coordinate for each node in the current layer
            x = np.ones(max_nodes) * i
            # Add the node coordinates for the current layer to the list
            node_coords.append(np.column_stack((x, y)))

        # Create a figure and axes
        fig, ax = plt.subplots()

        # Plot the nodes
        for i, layer_coords in enumerate(node_coords):
            ax.scatter(layer_coords[:, 0], layer_coords[:, 1])
            ax.text(layer_coords[:, 0].mean(),
                    layer_coords[:, 1].mean(), f'layer {i}')

        # Plot the weights
        for i, layer in enumerate(self.hidden_layers):
            for j, neuron in enumerate(layer):
                for k, weight in enumerate(neuron.weights):
                    ax.plot([i, i + 1], [j, k], 'k-', linewidth=abs(weight / 100))

        for j, neuron in enumerate(self.output_layer):
            for k, weight in enumerate(neuron.weights):
                ax.plot([num_layers - 1, num_layers],
                        [j, k], 'k-', linewidth=abs(weight / 100))

        plt.show()
