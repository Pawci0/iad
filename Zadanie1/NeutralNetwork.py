import numpy
import scipy.special


class NeutralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate=0.1, bias_switch=0,
                        monemtum_rate=0,activation_function_output=lambda x: scipy.special.expit(x),
                        dactivation_function_output=lambda x: scipy.special.expit(x)*(1-scipy.special.expit(x))):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.lr = learning_rate
        self.bias_switch=bias_switch
        self.wih = numpy.random.rand(self.hnodes, self.inodes)
        self.bih = numpy.random.rand(self.hnodes, 1)*bias_switch
        self.who = numpy.random.rand(self.onodes, self.hnodes)
        self.bho = numpy.random.rand(self.onodes, 1)*bias_switch
        self.momentum=monemtum_rate;
        self.beta=0.1;
        self.activation_function = lambda x: scipy.special.expit(x)
        self.activation_function_output=activation_function_output
        self.dactivation_function_output=dactivation_function_output
        self.who_back=0
        self.wih_back=0
        self.bih_back=0
        self.bho_back=0
        pass
    def train(self, input_list, target_list):
        inputs=numpy.array(input_list, ndmin=2).T
        targets=numpy.array(target_list, ndmin=2).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_inputs += self.bih
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_inputs += self.bho
        final_outputs = self.activation_function_output(final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)

        self.who += self.lr * numpy.dot((output_errors * self.dactivation_function_output(final_outputs)),
                                        numpy.transpose(hidden_outputs))
        # momentum
        self.who+=(self.who_back*self.momentum)
        self.who_back=self.lr * numpy.dot((output_errors * self.dactivation_function_output(final_outputs)),
                                        numpy.transpose(hidden_outputs))
        self.bho += self.lr * output_errors * self.dactivation_function_output(final_outputs)*self.bias_switch
        self.bho += self.bho_back*self.momentum
        self.bho_back = self.lr * output_errors * self.dactivation_function_output(final_outputs)*self.bias_switch
        self.bho *= self.bias_switch

        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs *
                                        (1.0 - hidden_outputs)),numpy.transpose(inputs))
        #momnetum int-hidd
        self.wih+=self.momentum*self.wih_back
        # momentum
        self.wih_back=self.lr * numpy.dot((hidden_errors * hidden_outputs *
                                        (1.0 - hidden_outputs)),numpy.transpose(inputs))

        #momentum bias-int hidd

        self.bih += self.lr * hidden_errors * hidden_outputs * (1.0 - hidden_outputs)
        self.bih +=self.bih_back * self.momentum
        self.bih_back= self.lr * hidden_errors * hidden_outputs * (1.0 - hidden_outputs)
        self.bih*=self.bias_switch

    def query(self, input_list):
        inputs=numpy.array(input_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_inputs += self.bih
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_inputs += self.bho
        final_outputs = self.activation_function_output(final_inputs)
        return final_outputs
    def getHiddenOutputs(self, input_list):
        inputs=numpy.array(input_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_inputs += self.bih
        hidden_outputs = self.activation_function(hidden_inputs)
        return hidden_outputs
