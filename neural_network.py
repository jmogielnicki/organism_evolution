import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from statistics import mean
from helpers import get_random_neuron_weights, get_random_neuron_bias, normalize
import consts

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
    def __init__(self, shape=[1, 4, 3]):
        self.shape = shape
        num_layers = len(shape)
        self.num_inputs = shape[0]
        num_outputs = shape[num_layers - 1]
        hidden_layers_shape = shape[1:num_layers]

        # Initialize the hidden layers and output layer of the network
        self.hidden_layers = []
        self.output_layer = []

        # iterate from the first hidden layer to the output layer (skip the input layer)
        # define the necessary neurons with the correct number of weights for the previous layer and a bias
        for layer_idx, num_neurons in enumerate(shape[1:], 1):
            prev_layer_num_neurons = shape[layer_idx - 1]
            layer = []
            for _ in range(num_neurons):
                # Create a new neuron with random weights and bias
                weights = get_random_neuron_weights(prev_layer_num_neurons)
                bias = get_random_neuron_bias()
                neuron = Neuron(weights, bias)
                layer.append(neuron)
            # append the layer to either hidden or output layer
            if layer_idx == num_layers - 1:
                self.output_layer = layer
            else:
                self.hidden_layers.append(layer)

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

    def print(self):
        print('inputs: ', self.num_inputs)
        print('hidden_layers: ', [[neuron.__dict__ for neuron in layer] for layer in self.hidden_layers])
        print('output_layer: ', [neuron.__dict__ for neuron in self.output_layer])

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
        print(node_coords)
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
                        [j, k], 'k-', linewidth=abs(weight))

        plt.show()

    def visualize2(self):
        print('__visualize')
        # layers are equal to hidden layers plus input and output layers
        num_hidden_layers = len(self.hidden_layers)
        num_layers = num_hidden_layers + 2

        # the [0] represents the input layer, which does not have true neurons
        combined_layers = self.hidden_layers + [self.output_layer]
        # print(len(combined_layers))
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)
        cmap = mpl.colormaps['bwr_r']

        # work backwards through the shape of the network
        for layer_idx in range(len(self.shape) - 1, 0, -1):
            num_neurons = self.shape[layer_idx]
            print(layer_idx)
            print(combined_layers)
            layer = combined_layers[layer_idx - 1]  # the combined layers list doesn't include input layer
            label = 'o' if layer_idx == len(
                self.shape) - 1 else 'h'
            for i, neuron in enumerate(layer):
                ax.scatter(
                    layer_idx,
                    i,
                    s=200,
                    c=cmap(normalize(neuron.bias, consts.neuron_bias_lower_bound, consts.neuron_bias_upper_bound)),
                    edgecolors='red' if neuron.bias < 0 else 'blue',
                )
                ax.text(layer_idx, i, '{}'.format(round(neuron.bias, 1)))
                for j, weight in enumerate(neuron.weights):
                    ax.plot(
                        [layer_idx, layer_idx - 1],
                        [i, j],
                        c=cmap(normalize(weight, consts.neuron_weight_lower_bound, consts.neuron_weight_upper_bound)),
                    )
                    ax.text(x=mean([layer_idx, layer_idx, layer_idx, layer_idx, layer_idx - 1]),
                            y=mean([i, i, i, i, j]),
                            s=round(weight, 1))

        plt.show(block=False)
        plt.pause(1)
        input()
        plt.close()
