import numpy as np
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rnc = int(input('Number of settlements: '))
density = int(input("Uniform density: "))

def initial(rnc, density):
    means = []
    cov = [[1, 0], [0, 1]]
    n = density

    for i in range(rnc):
        means.append(np.random.randint(low=0, high=20, size=(2)).tolist())

    X = [np.random.multivariate_normal(means[i], cov, n) for i in range(rnc)]
    means = np.array(means)
    X = np.array(X)
    return means, X

means, X = initial(rnc, density)


def plot(rnc, X, means):
    fig, axs = plt.subplots(1, rnc)
    fig.set_figwidth(8)
    fig.set_figheight(8)
    for i in range(rnc):
        axs[i].scatter(X[i,:,0], X[i,:,1])
        axs[i].scatter(means[i,0], means[i,1], color='red')
    plt.show()

plot(rnc, X, means)


def many_cities(width, height, plots, ppl, initial_infected, travel_rate, social_dist = False):
    pass