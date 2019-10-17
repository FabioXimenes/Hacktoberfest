import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
 
def separate_by_class(data):
    # Separate the data by class. Return sets for each class.
    classes = np.unique(data[:, -1]).astype(int)
    return [np.vstack([x for x in data if x[-1] == c]) for c in classes]
 
def priori(data, total):
    # Calculate the priori probability for each class
    return np.divide([len(class_set) for class_set in data], total)
 
def initialize_params(data, n_components):  # Initialize parameters
 
    m, d = data.shape
 
    pi = 1/n_components  # Initialize the pi's with the same probability
 
    mu = data[np.random.choice(m, n_components, replace=False)]  # Get n_components rows randomly from the data
 
    Sigma = np.eye((d))  # Initialize cov with identity matrices
 
    params = {}
 
    for k in range(n_components):  # Initialize parameters equals for all components k
        params[k] = {'mu': mu[k],
                     'Sigma': Sigma,
                     'pi': pi}
 
    return params
 
def mvnpdf(data, mu, Sigma):
    det = np.linalg.det(Sigma)  # Calcule the determinant of covariance matrice
    inv = np.linalg.inv(Sigma)  # Calcule the inverse of covariance matrice
 
    m, d = data.shape
    pdfs = np.zeros(m)
 
    #mvn = multivariate_normal(mu, Sigma)
 
    for i in range(m):
        #pdfs[i] = mvn.pdf(data[i])
        pdfs[i] = (1 / ((2 * np.pi) ** (d / 2) * np.sqrt(det))) * np.exp(
               -(1 / 2) * np.inner(np.inner(data[i] - mu.T, inv), data[i] - mu))
 
    return np.squeeze(pdfs)
 
def expectation(data, params):  # Step-E: Compute the responsibilities
 
    k = len(params)
 
    delta = np.zeros((data.shape[0], k))
 
    for i in range(k):
 
        mu = params[i]['mu']
        Sigma = params[i]['Sigma']
        pi = params[i]['pi']
 
        delta[:, i] = mvnpdf(data=data, mu=mu, Sigma=Sigma) * pi
 
    return delta / delta.sum(axis=1)[:, np.newaxis]  # Divide each element column by the row sum
 
def maximization(data, delta, params):  # Step-M: Reestimative of the parameters
    N = delta.sum(axis=0)
 
    m, d = data.shape
 
    for i in range(len(N)):
        params[i]['mu'] = (data.T * delta[:, i]).sum(axis=1)/N[i]
        params[i]['Sigma'] = weight_Sigma(data=data, mu=params[i]['mu'], delta=delta[:, i], Nk=N[i])
        params[i]['pi'] = N[i]/m
 
    return params
 
def weight_Sigma(data, mu, delta, Nk):
    A = (data - mu).T * delta
    Sigma = np.inner(A, (data - mu).T) / Nk
    if np.isfinite(np.linalg.cond(Sigma)) or np.inf:
        Sigma = Sigma + 0.01 * np.eye(Sigma.shape[0], Sigma.shape[1])
 
    return Sigma
 
 
def gaussianMixEM(data, k, epochs, epsilon):
 
    params = initialize_params(data=data[:, :-1], n_components=k)  # Initialize the parameters
 
    for i in range(epochs):
        delta = expectation(data[:, :-1], params=params)
 
        log_likelihood = (np.log(delta.sum(axis=0))).sum()
 
        if i > 1 and (log_likelihood <= epsilon or log_likelihood == oldLog):
            print('The parameters converged at epoch '+str(i))
            break
 
        oldLog = log_likelihood
 
        params = maximization(data=data[:, :-1], delta=delta, params=params)
 
    return params
 
 
def train(train_set, k, epochs=200, epsilon=1e-4):
    # Separate patterns by class
    sets = separate_by_class(train_set)
 
    # Calculate priori probabilities for each class
    priori_probabilities = priori(sets, train_set.shape[0])
 
    params = {}
 
    for i in range(len(sets)):
        params[i] = gaussianMixEM(data=sets[i], k=k, epochs=epochs, epsilon=epsilon)
 
    return {'params': params, 'prioris': priori_probabilities}
 
 
def predict(model, test_set, k):
    classes = len(model['params'])
    prioris = model['prioris']
    m, d = test_set[:, :-1].shape
 
    posterioris = np.zeros((m, classes))
 
    for i in range(len(model['params'])):  # The quantity of models is equals the number of classes
        params = model['params'][i]
        temp_posteriori = np.zeros((m, k))
        for j in range(k):
            temp_posteriori[:, j] = mvnpdf(data=test_set[:, :-1], mu=params[j]['mu'], Sigma=params[j]['Sigma'])\
                                    * params[j]['pi']
 
        posterioris[:, i] = temp_posteriori.sum(axis=1) * prioris[i]
 
    return np.argmax(posterioris, axis=1)
 
 
def surfaceDecision(namedataset, data, rows, cols, attributes, classes, k):
 
    labels = data[:, -1].astype(int)
 
    cmap = plt.get_cmap("Set2")
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
            model = train(train_set=np.column_stack((X, Y,  data[:, -1])), k=k)
 
            x1 = np.linspace(0, 1, 100)
            x2 = np.linspace(0, 1, 100)
 
            if gg == cols:
                l0 = mpatches.Patch(color=cmap.colors[0], label=classes[0])
                l1 = mpatches.Patch(color=cmap.colors[1], label=classes[1])
                l2 = mpatches.Patch(color=cmap.colors[2], label=classes[2])
                plt.legend(handles=[l0, l1, l2], bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
                # plt.show()
 
                fig, axes = plt.subplots(nrows=rows, ncols=cols, sharex=True, sharey=True, squeeze=False)
                axes = axes.ravel()
                fig.suptitle('Superfícies de Decisão com Atributos Combinados Par a Par - ' + namedataset, fontsize=14)
                gg = 0
 
            for xi in x1:
                for xj in x2:
                    x = np.array([xi, xj, 0]).reshape((1, 3))
                    label = predict(model=model, test_set=x, k=k)
                    axes[gg].plot(xi, xj, marker='o', c=cmap.colors[label[0]], zorder=1)
 
            for c in np.unique(labels):
                indices = np.where(labels == c)
                axes[gg].scatter(data[indices, m], data[indices, n], s=15, c=cmap.colors[c], edgecolor="w", linewidth=1,
                                 marker='o', zorder=2)
                axes[gg].grid(False)
 
 
            axes[gg].set_xlabel(attributes[m])
            axes[gg].set_ylabel(attributes[n])
            gg += 1
