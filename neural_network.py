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
    def __init__(self, shape=[1, 4, 3]):
        print('__construct')
        self.shape = shape
        num_layers = len(shape)
        self.num_inputs = shape[0]
        num_outputs = shape[num_layers - 1]
        hidden_layers_shape = shape[1:num_layers]

        # Initialize the hidden layers and output layer of the network
        self.hidden_layers = []
        self.output_layer = []
        for layer_idx, num_neurons in enumerate(shape[1:], 1):
            print(layer_idx)
            last_layer_num_neurons = shape[layer_idx - 1]
            layer = []
            for _ in range(num_neurons):
                # Create a new neuron with random weights and bias
                weights = np.random.rand(last_layer_num_neurons)
                bias = np.random.rand()
                neuron = Neuron(weights, bias)
                layer.append(neuron)
            if layer_idx == num_layers - 1:
                print('appending to output_layer')
                print(len(layer))
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

        combined_layers = self.hidden_layers + [self.output_layer]
        # print(len(combined_layers))
        fig, ax = plt.subplots()

        # work backwards through the shape of the network
        for i in range(len(self.shape) - 1, -1, -1):
            num_neurons = self.shape[i]
            print(i, ' ', num_neurons)
            layer = 

        # work backwards from the output layer to the first hidden layer (do not include input layer)
        for layer_idx in range(len(combined_layers) - 1, -1, -1):
            print('layer idx: ', layer_idx)
            print('next layer idx: ', layer_idx - 1)
            layer = combined_layers[layer_idx]
            next_layer = combined_layers[layer_idx - 1]
            # print(next_layer)
            label = 'output' if layer_idx == len(combined_layers) - 1 else 'hidden'
            for i, neuron in enumerate(layer):
                ax.scatter(layer_idx + 1, i)
                ax.text(layer_idx + 1, i, '{}_{}'.format(label, i))
                if next_layer:
                    for j, neuron in enumerate(next_layer):
                        ax.plot([layer_idx + 1, layer_idx], [i, j])

        # # plot output layer nodes
        # for i, neuron in enumerate(self.output_layer):
        #     ax.scatter(num_layers - 1, i)
        #     ax.text(num_layers - 1, i, 'output_' + str(i))

        # plot the input layer nodes
        for i in range(self.num_inputs):
            ax.scatter(0, i)
            ax.text(0, i, 'input_' + str(i))

        # # plot the hidden layers
        # for i in range(len(self.hidden_layers)):
        #     for j, neuron in enumerate(self.hidden_layers[i]):
        #         ax.scatter(1 + i, j)
        #         ax.text(1 + i, j, 'hidden_{}_{}'.format(str(i), str(j)))


        plt.show()
