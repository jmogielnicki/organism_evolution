import numpy as np

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
