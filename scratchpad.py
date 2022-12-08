from neural_network import NeuralNetwork, Neuron
import random

def temp_build_brain(num_inputs, num_hidden, num_outputs):
    # Create the NeuralNetwork object
    nn = NeuralNetwork([2, 4, 3], ['one', 'two', 'three'], [], id=0)
    nn.print()
    nn.visualize(should_show=True)
