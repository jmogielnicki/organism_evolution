import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from statistics import mean
from helpers import get_random_neuron_weights, get_random_neuron_bias, normalize
from consts import brain_diagrams_dir
import consts
import pprint
import os

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
    def __init__(self, shape: list[int], output_labels: list[str], input_labels: list[str], id: int):
        if output_labels and len(output_labels) != shape[len(shape) - 1]:
            raise Exception("There must be as many output labels as there are outputs")
        if input_labels and len(input_labels) != shape[0]:
            raise Exception("There must be as many input labels as there are inputs")
        if len(shape) < 2:
            raise Exception("There must be at least 2 elements in the shape to represent the input and output layers")
        if len([x for x in shape if x < 1]) > 0:
            raise Exception(
                "Each element in the shape array must be greater than 0, representing the num neurons in that layer")
        self.shape = shape
        num_layers = len(shape)
        self.num_inputs = shape[0]
        self.output_labels = output_labels
        self.input_labels = input_labels
        self.id = id

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
        pp = pprint.PrettyPrinter(indent=4)
        d = [
            {'inputs: ': self.num_inputs},
            {'hidden_layers: ': [[neuron.__dict__ for neuron in layer] for layer in self.hidden_layers]},
            {'output_layer: ': [neuron.__dict__ for neuron in self.output_layer]}
        ]
        pp.pprint(d)

    def visualize(self, should_show=True):
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
            is_output_layer = layer_idx == len(self.shape) - 1
            num_neurons = self.shape[layer_idx]
            layer = combined_layers[layer_idx - 1]  # the combined layers list doesn't include input layer
            for i, neuron in enumerate(layer):
                x = layer_idx
                y = normalize(i, 0, self.shape[layer_idx])
                label = self.output_labels[i] + '_' if is_output_layer and self.output_labels else ''
                bias_val = normalize(neuron.bias, consts.neuron_bias_lower_bound, consts.neuron_bias_upper_bound)
                print(cmap(bias_val))
                ax.scatter(
                    x,
                    y,
                    s=400,
                    c=cmap(bias_val),
                    edgecolors='red' if neuron.bias < 0 else 'blue',
                )
                ax.text(
                    x - 0.01,
                    normalize(i, 0, self.shape[layer_idx]) + 0.03,
                    '{}{}'.format(label, round(neuron.bias, 1))
                )
                for j, weight in enumerate(neuron.weights):
                    x = layer_idx
                    x2 = layer_idx - 1
                    y = normalize(i, 0, num_neurons)
                    y2 = normalize(j, 0, self.shape[layer_idx - 1])
                    weight_val = normalize(weight, consts.neuron_weight_lower_bound, consts.neuron_weight_upper_bound)
                    ax.plot(
                        [x, x2],
                        [y, y2],
                        c=cmap(weight_val),
                        linewidth=abs((weight_val - 0.5)) * 5
                    )
                    # we shift the text over to be closer to the neuron that contains the weights
                    ax.text(x=mean([x, x, x, x, x2]),
                            y=mean([y, y, y, y, y2]),
                            s=round(weight, 1))
        for i, input_label in enumerate(self.input_labels):
            ax.text(x=-0.1,
                    y=normalize(i, 0, len(self.input_labels)),
                    s=input_label)

        plt.grid(False)
        plt.axis('off')
        if should_show:
            plt.show(block=False)
            plt.pause(1)
            input()
            plt.close()
        return plt