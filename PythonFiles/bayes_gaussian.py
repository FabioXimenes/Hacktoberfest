import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Utils as util
import matplotlib.patches as mpatches
from discriminants import discriminant
 
times_train = []
times_test = []
 
 
def separate_by_class(data):
    # Separate the data by class. Return sets for each class.
    classes = np.unique(data[:, -1]).astype(int)
    return [np.vstack([x for x in data if x[-1] == c]) for c in classes]
 
def averages(data):
    # Calculate the average of each column, for each class
    return [np.mean(class_set[:, :-1], axis=0) for class_set in data]
 
def covariances(data):
    # Calculate the covariances matrix for each class
    return [np.cov(class_set[:, :-1].T) for class_set in data]
 
def priori(data, total):
    # Calculate the priori probability for each class
    return np.divide([len(class_set) for class_set in data], total)
 
def bayes_predict(test_set, model, type):
    predicts = []
 
    if type == '':
        type = 'mvnpdf'
 
    for x in test_set:
        gi = discriminant(x, model, type)
 
        # Select the index(class) corresponding to the function of higher discriminant value.
        predicts.append(np.argmax(gi))
 
    return predicts
 
 
def bayes_train(train_set):
    # Separate patterns by class
    sets = separate_by_class(train_set)
 
    # Calculate mean for each class
    mu = averages(sets)
 
    # Calculate covariance matrix for each class
    Sigmas = covariances(sets)
 
    for i in range(len(Sigmas)):
        if np.isfinite(np.linalg.cond(Sigmas[i])) or np.inf:
            Sigmas[i] = Sigmas[i] + 0.01 * np.eye(Sigmas[i].shape[0],  Sigmas[i].shape[1])
 
    # Calculate priori probabilities for each class
    priori_probabilities = priori(sets, train_set.shape[0])
 
    # Calculate covariance matrix with all data, without distinguish by classes
    SigmaAll = np.cov(train_set[:, :-1].T)
 
    return {'mu': mu, 'Sigmas': Sigmas, 'prioris': priori_probabilities, 'SigmaAll': SigmaAll}
 
def surfaceDecision(namedataset, data, rows, cols, attributes, classes, type):
 
    labels = data[:, -1].astype(int)
 
    #cmap = plt.get_cmap("Set1")
    cmap = plt.get_cmap("tab10")
    markers = ['o', '*', '^']
    plt.rcParams['figure.figsize'] = (13, 4)
 
 
 
    fig, axes = plt.subplots(nrows=rows, ncols=cols, sharex=True, sharey=True, squeeze=False)
    axes = axes.ravel()
    fig.suptitle('Superfícies de Decisão com Atributos Combinados Par a Par - ' + namedataset, fontsize=14)
    gg = 0
    plt.show()
 
    for m in range(data.shape[1] - 2):  # For in attributes of data
 
        for n in range(m + 1, data.shape[1] - 1):
 
            X = data[:, m]
            Y = data[:, n]
            model = bayes_train(np.column_stack((X, Y, data[:, -1])))
 
            x1 = np.linspace(0, 1, 100)
            x2 = np.linspace(0, 1, 100)
 
            for xi in range(len(x1)):
                for xj in range(len(x2)):
                    x = [np.array([x1[xi], x2[xj]])]
                    label = bayes_predict(x, model, type)
                    axes[gg].plot(x1[xi], x2[xj], '.', c=cmap.colors[label[0]], zorder=1)
 
            for c in np.unique(labels):
                indices = np.where(labels == c)
                axes[gg].scatter(data[indices, m], data[indices, n], s=15, c=cmap.colors[c], edgecolor="w", linewidth=1, marker=markers[c], zorder=2)
                axes[gg].grid(False)
 
 
            axes[gg].set_xlabel(attributes[m])
            axes[gg].set_ylabel(attributes[n])
            gg += 1
 
        l0 = mpatches.Patch(color=cmap.colors[0], label=classes[0])
        l1 = mpatches.Patch(color=cmap.colors[1], label=classes[1])
        l2 = mpatches.Patch(color=cmap.colors[2], label=classes[2])
        plt.legend(handles=[l0, l1, l2], bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
        #plt.show()
 
    #plt.savefig(namedataset + '' + str(m + n) + '.png')
 
 
#============================================================
data1 = np.genfromtxt("../Datasets/iris.data.txt", delimiter = ",",usecols = (0, 1, 2, 3, 4))
#attributes = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width']
classes1 = ['Setosa', 'Versicolour', 'Virginica']
 
data2 = np.genfromtxt("../Datasets/column_3C.dat", delimiter = ",", usecols = (0, 1, 2, 3, 4, 5, 6))
#attributes = ['Pelvic Incidence', 'Pelvic Tilt', 'Lumbar Lord.Angle', 'Sacral Slope',
#                    'Pelvic Radius', 'Grade of Spond.']
classes2 = ['Disk Hernia', 'Spondylolisthesis', 'Normal']
 
data3 = np.genfromtxt("../Datasets/breast.data", delimiter = ",",usecols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
classes3 = ['Benign', 'Malignant']
 
data4 = np.genfromtxt("../Datasets/dermatology.data", delimiter = ",",usecols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                                                 10, 11, 12, 13, 14, 15, 16, 17,
                                                                                 18, 19, 20, 21, 22, 23, 24, 25,
                                                                                 26, 27, 28, 29, 30, 31, 32, 33, 34))
classes4 = ['Psoriasis', 'Seboreic Dermatitis', 'Lichen Planus ', 'Pityriasis Rosea',
          'Cronic Dermatitis', 'Pityriasis Rubra Pilaris']
 
#data = util.generateArtificialDataset()
#attributes = ['Attribute 1', 'Attribute 2']
#classes = ['Class 1', 'Class 2', 'Class 3']
 
data_to_plot = []
datas = [data1, data2, data3, data4]
classes = [classes1, classes2, classes3, classes4]
 
for j in range(len(datas)):
    realizations = 30
    accuracies = []
    erros = []
 
    data = util.normalize(datas[j])
 
    models = {}  # This dictionary going to save the train_set and test_set in each realization
    type = 'quadratic'
 
    for i in range(realizations):
        np.random.shuffle(data)
 
        train_set, test_set = np.split(data, [int(.8 * len(data))])  # Split data in train(80%) and test(20%)
 
        # Train
        start = time.time()
        model = bayes_train(train_set)
        end = time.time()
        times_train.append(end - start)  # Getting time of training
 
        #Test
        start = time.time()
        predicts = bayes_predict(test_set[:, :-1], model, type)
        end = time.time()
        times_test.append(end - start)  # Getting time of test
 
        hits = (test_set[:, -1] == predicts).sum()
        accuracies.append(hits/test_set.shape[0])
        erros.append(1-accuracies[-1])
 
        models[i] = i, train_set.copy(), test_set.copy(), predicts.copy(), accuracies[-1].copy()
 
 
    best_model = models[util.find_nearest(accuracies, np.mean(accuracies))] #Find the model with accuracy more closer of the mean accuracies
    util.confusion_matrix(best_model[2][:, -1], best_model[3], classes[j])
    #np.savetxt("train_set.csv", best_model[1], delimiter=",", fmt='%10.5f')
    #np.savetxt("test_set.csv", best_model[2], delimiter=",", fmt='%10.5f')
    #surfaceDecision('Iris', best_model[1], 2, 3, attributes, classes, type)
 
    data_to_plot.append(accuracies)
    print('Mean Train Time:' + str(np.mean(times_train)))
    print('Mean Test Time:' + str(np.mean(times_test)))
    print('Mean Accuracy:' + str(np.mean(accuracies)))
    print('Standard Deviation:' + str(np.std(accuracies)))
 
rotules = ['Iris', 'Coluna Vertebral', 'Câncer de Mama', 'Dermatologia']
util.plot_boxplot(data_to_plot, rotules)
