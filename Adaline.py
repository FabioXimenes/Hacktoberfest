import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from mpl_toolkits.mplot3d import Axes3D
 
class Adaline(object):
 
    def __init__(self, epochs=500):
        self.parameters = {}
        self.learning_rates = None
        self.epochs = epochs
        self.rmse = []  # to keep track of the cost - Root Mean Square Error
 
    def initialize_parameters(self, n_x):
        """
        Argument:
        n_x -- size of the input layer
 
        Returns:
        parameters -- python dictionary containing your parameters:
                        W1 -- weight matrix of shape (1, n_x)
                        b1 -- bias vector of shape (1, 1)
        """
 
        W1 = np.random.randn(1, n_x) * 0.01
        b1 = np.zeros((1, 1))
 
        self.parameters = {"W1": W1, "b1": b1}
 
    def linear_activation_forward(self, x):
        """
        Arguments:
        x -- input data
 
        Returns:
        A -- the output of the activation function, also called the post-activation value
        """
 
        W = self.parameters['W1']
        b = self.parameters['b1']
 
        z = np.dot(W, x) + b
 
        return np.squeeze(z)
 
    def update_parameters(self, error, x, t):
        """
        Arguments:
        error -- desired error - model output
        x -- input data
        t -- instant t
 
        Returns:
        parameters -- python dictionary containing your updated parameters
                      parameters["W1"] = ...
                      parameters["b1"] = ...
        """
 
        self.parameters["W1"] = self.parameters["W1"] + self.learning_rates[t] * error * x
        self.parameters["b1"] = self.parameters["b1"] + self.learning_rates[t] * error
 
    def fit(self, data, alpha_start=0.3, Jmin=0.5):
        """
        Arguments:
        data -- input data, of shape (n_x, number of examples)
        alpha_start -- initial learning rate
        """
        m, n = data.shape  # number of examples
 
        tmax = m * self.epochs  # Max number of iterations on training set
 
        # Generate learning_rates decay to train
        self.learning_rates = [alpha_start * (1 - (t / tmax)) for t in range(tmax)]
 
        # Initialize parameters dictionary, by calling one of the functions you'd previously implemented
        self.initialize_parameters(n - 1)
 
        t = 0
        for i in range(self.epochs):
 
            np.random.shuffle(data)
 
            X = data[:, :-1]
            Y = data[:, -1]
 
            sum_error = 0
 
            for x, y in zip(X, Y):
                # Forward propagation: LINEAR. Inputs: "X, W1, b1". Output: "sum".
                pred = self.linear_activation_forward(x)
 
                # Compute error
                error = y - pred
                sum_error += error ** 2
 
                # Update parameters.
                self.update_parameters(error, x, t)
 
                t += 1
 
            # if i % 10 == 0:
            self.rmse.append(np.sqrt(sum_error / m))
 
            if self.rmse[-1] < Jmin:
                print('The training stopped at epoch ' + str(i) + '. The last error in training is less than {}', Jmin)
                break
 
    def predict(self, X_test):
        return self.linear_activation_forward(X_test.T)
 
    def curve_sum_erros(self, namedaset):
        plt.plot(np.squeeze(self.rmse), marker='.')
        plt.ylabel('error')
        plt.xlabel('number of epochs')
        plt.title("RMSE by Epoch")
        plt.savefig(namedaset+"_curve_rmse.png")
        plt.close()
 
    def surfaceDecision(self, namedataset, data):
 
        plt.rcParams['figure.figsize'] = (7, 4)
        plt.title('Superfícies de Decisão - ' + namedataset, fontsize=10)
 
        X = data[:, :-1]
        Y = data[:, -1]
        self.fit(np.column_stack((X, Y)))
 
        x1 = np.linspace(0, 1, 100)
 
        if namedataset == 'Artificial I':
            reg = self.predict(x1.reshape(100, 1))
            plt.plot(x1, reg, c='r', zorder=1)
            plt.scatter(X, Y, s=15, c='b',
                        edgecolor='w', linewidth=1,
                        marker='o', zorder=2)
        else:
            x2 = np.linspace(0, 1, 100)
            X1, X2 = np.meshgrid(x1, x2)
            reg = []
            for xi in x1:
                for xj in x2:
                    reg.append(self.predict(np.column_stack((xi, xj))))
 
            ax = plt.axes(projection='3d')
            ax.plot_surface(X1, X2, np.reshape(reg, (100,100)), color='r')
 
            ax.scatter3D(X[:, 0], X[:, 1], Y, c='b',
                         edgecolor='w', linewidth=1,
                         marker='o', zorder=2)
 
        plt.savefig(namedataset + '_surface.png')
 
        plt.close()
