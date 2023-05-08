import numpy as np
from numpy.random import default_rng
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rng = default_rng()

def initial(rnc, density):
    means = []
    cov = [[1, 0], [0, 1]]
    n = density
    X = []
    for i in range(rnc):
        means.append(np.random.randint(low=0, high=20, size=(2)).tolist())
        X.append(np.random.multivariate_normal(means[i], cov, n))
        
    means = np.array(means)
    X = np.array(X)
    return means, X

def plot_kmeans(rnc, X, means):
    fig, axs = plt.subplots(rnc)
    fig.tight_layout(pad=0.3)
    for i in range(rnc):
        axs[i].scatter(X[i,:,0], X[i,:,1])
        axs[i].scatter(means[i,0], means[i,1], color='red')
    return fig

def Simulation_Plot(mode=["Many Cities"], population=10, initial_infected=3, contact_radius=3, recovery_chance=50, fatality=50,
                    distancing=None, distancing_duration=0, center_gather_rate=0, symptom_showing=0,
                    infected_threshold=0, travel_rate=0, vaccination_chance=0, expire_date=0):
    rnc = 1
    if "Many Cities" in mode:
        rnc += 5
    if "Identify + Isolate" in mode:
        rnc += 1
    infect = rng.choice(population, size=initial_infected, replace=False).tolist()
    
    #st.text(f"{infect, population, initial_infected}")
    people = []
    for idx in range(population):
        plot = [np.random.randint(0, 3), np.random.randint(0, 3)] if "Many Cities" in mode else 0
        means, X = initial(rnc=rnc, density=population)
        
        people.append([plot, X[:, 0], X[:, 1], "infected" if idx in infect else "normal"])
    
    #print(people)
        
    #people: plot_index, x, y, state
    #for default 1 plot
    #people = [ [0, x1, y1, "normal"], [0, x2, y2, "infected", ... ]
    #for many_cities
    #people = [ [[0, 1], x1, y1, "normal"], [[2, 0], x2, y2, "infected", ... ]
    return (plot_kmeans(rnc, X, means), people)