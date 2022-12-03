import numpy as np
from neuron import Neuron
import numpy.typing as npt


class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

    def forward_propagate(self, inputs):
        # Propagate the inputs through the network layer by layer
        for layer in self.layers:
            new_inputs = []
            for neuron in layer:
                new_inputs.append(neuron.activate(inputs))
            inputs = new_inputs
        return inputs

    # def visualize(self):
    #     plt.figure(figsize=(10, 5))
    #     plt.xlim(-0.2, 1.2)
    #     plt.ylim(-0.2, 1.2)

    #     # Plot the input layer
    #     plt.scatter(inputs[:, 0], inputs[:, 1], c=targets)

    #     # Draw lines between the input and hidden layers
    #     for i in range(len(self.neurons[0])):
    #         neuron = self.neurons[0][i]
    #         w = neuron.weights
    #         plt.plot([0, w[1]], [0, w[2]], 'k')

    #     # Draw lines between the hidden and output layers
    #     for i in range(len(self.neurons[1])):
    #         neuron = self.neurons[1][i]
    #         w = neuron.weights
    #         plt.plot([w[0], w[1]], [w[0], w[2]], 'k')

    #     plt.show()
