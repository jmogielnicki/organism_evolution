import numpy as np
from neuron import Neuron


class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.neurons = []
        # Initialize the weights randomly
        for i in range(1, len(layers)):
            layer_neurons = []
            for j in range(layers[i]):
                # Create a neuron with random weights and bias
                weights = np.random.rand(layers[i - 1])
                bias = np.random.rand(1)
                neuron = Neuron(weights, bias)
                layer_neurons.append(neuron)
            self.neurons.append(layer_neurons)

    def feedforward(self, inputs):
        # Feed the inputs through the neural network
        outputs = inputs
        for i in range(len(self.neurons)):
            layer_outputs = []
            for neuron in self.neurons[i]:
                # Compute the output of the neuron
                output = neuron.activate(outputs)
                layer_outputs.append(output)
            outputs = layer_outputs
        return outputs

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
