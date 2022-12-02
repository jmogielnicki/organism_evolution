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
