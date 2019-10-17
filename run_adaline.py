import matplotlib.pyplot as plt
import numpy as np
import nn_utils as utils
import time
from Adaline import Adaline
from mpl_toolkits.mplot3d import Axes3D
 
def generateArtificialI():
    x = np.linspace(-5, 5, 100)
    noise = np.random.uniform(low=0, high=2, size=100)
    y = (2 * x + 1) + noise
    plt.plot(x, y, '.', label='y=2x+1+noise')
    plt.title('Graph of y=2x+1')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.grid()
    plt.savefig('artificialI.png')
    plt.close()
 
    return np.column_stack((x, y))
 
 
def generateArtificialII():
    x1 = np.random.uniform(low=0, high=2, size=100)
    x2 = np.random.uniform(low=0, high=2, size=100)
    noise = np.random.uniform(low=-1, high=1, size=100)
    y = (2 * x1 + 4 * x2 + 1) + noise
 
    #fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(x1, x2, y, c='r', marker='.')
    ax.set_xlabel('X1 Label')
    ax.set_ylabel('X2 Label')
    ax.set_zlabel('Y Label')
 
    plt.title('Graph of y=2x1+4x2+1+noise')
    plt.savefig('artificialII.png')
    plt.close()
 
    return np.column_stack((x1, x2, y))
 
artificialI = generateArtificialI()
artificialII = generateArtificialII()
 
datas = [artificialI, artificialII]
names = ["Artificial I", "Artificial II"]
boxplot = []
 
for data, name in zip(datas, names):
 
    realizations = 20
 
    times_train = []
    times_test = []
 
    mse = []  # mean square error
    rmse = []  # root mean square error
 
    data = utils.normalize(data)
 
    models = {}
 
    for i in range(realizations):
        np.random.shuffle(data)
 
        train_set, test_set = np.split(data, [int(.8 * len(data))])  # Split data in train(80%) and test(20%)
 
        # Train
        start = time.time()
        adaline = Adaline()
        adaline.fit(train_set)
        end = time.time()
        times_train.append(end - start)  # Getting time of training
 
        # Test
        start = time.time()
        predicted = adaline.predict(test_set[:, :-1])
        end = time.time()
        times_test.append(end - start)  # Getting time of test
 
        Y_true = test_set[:, -1]
 
        mse.append(np.mean((Y_true - predicted)**2))
        rmse.append(np.sqrt(mse[-1]))
 
        models[i] = i, train_set.copy(), test_set.copy(), predicted.copy(), rmse[-1].copy(), mse[-1].copy(), adaline
 
    print("Dataset name: {}".format(name))
    print("Mean Square Error: {}".format(np.mean(mse)))
    print("Root Mean Square Error: {}".format(np.mean(rmse)))
    print("Standard Deviation MSE: {}".format(np.std(mse)))
    print("Standard Deviation RMSE: {}".format(np.std(rmse)))
    print('Mean Train Time:' + str(np.mean(times_train)))
    print('Mean Test Time:' + str(np.mean(times_test)))
 
    best_model = min(models.items(), key=lambda x: x[1][4])[1]  # Find the model with minimun root square mean error
    best_model[-1].curve_sum_erros(name)
 
    np.savetxt(name + "train_set.csv", best_model[1], delimiter=",", fmt='%10.5f')
    np.savetxt(name + "test_set.csv", best_model[2], delimiter=",", fmt='%10.5f')
 
    boxplot.append(rmse)
 
    adaline.surfaceDecision(name, best_model[1])
 
rotules = ['Artificial I', 'Artificial II']
utils.plot_boxplot(boxplot, rotules=rotules, title='Gráfico de caixas da raiz quadrada do erro quadrático médio dos datasets.')
