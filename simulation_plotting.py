import numpy as np
from numpy.random import default_rng
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rng = default_rng()

class Person:
    def __init__(self, plot, x, y, state):
        self.plot = plot
        self.x = x
        self.y = y
        self.state = state

    def quarantine(self):
        """
        cool, and a threshold until the infected, which show symptoms, get to a point
        -> there by making covid tests and increase chance of showing
        
        so like this
        all infecteds will be tagged as no symptoms
        then after a few iterations there'll be chances of them being turned to infected (showing symptoms)

        Then i recommend making an Update() function first, as these functions rely heavily
        on the update
        """
        if self.state == 'infected':
            # self.plot to quarantine
            pass
        pass
            
            
def plot_initiate(mode, population, initial_infected, contact_radius, recovery_chance, fatality, 
                    distancing=None, distancing_duration=0, center_gather_rate=0, symptom_showing=0,
                    infected_threshold=0, travel_rate=0, vaccination_chance=0, expire_date=0, history=[]):
    #Create population data
    infect = rng.choice(population, size=initial_infected,replace=False).tolist()
    people = []
    for idx in range(population):
        plot = [np.random.randint(0, 3), np.random.randint(0, 3)] if "Many Cities" in mode else 0
        x = np.random.randint(0, 1000)
        y = np.random.randint(0, 1000)
        state = "infected" if idx in infect else "normal"
        people.append(Person(plot, x, y, state))
    history.append(people)

    #Identify which modes and how the plots are displayed
    if "Many Cities" in mode:
        fig, axs = plt.subplots([3, 2])
    else:
        fig, axs = plt.subplots()
    
    #Draw
    coords = []
    for someone in people:
        coords.append([someone.x, someone.y])
    coords = np.array(coords)
    axs.scatter(coords[:, 0], coords[:, 1])

    isolatefig = False
    if "Isolate" in mode:
        isolatefig, isolateaxs = plt.subplots()

    #Live graph for real-time analysis
    livefig = live_graph(history)
    fig.tight_layout(pad=0.3)

    return (fig, isolatefig), livefig, people, history

e = """
"normal", "infected", "infected no symptoms", "vaccinated", "removed"

colors: blue, red, yellow, green, gray
"""

def live_graph(history=[[Person(0, 0, 0, "normal"), Person(0, 0, 0, "normal")], 
                        [Person(0, 0, 0, "infected"), Person(0, 0, 0, "normal")]]): 
    fig, axs = plt.subplots()
    hist = []
    for i, people in enumerate(history):
        for human in people:
            s_count = 0
            i_count = 0
            r_count = 0
            if human.state == "normal" or human.state == "vaccinated": s_count+=1
            if human.state == "infected" or human.state == "infected no symptoms": i_count+=1
            if human.state == "removed": r_count+=1
        hist.append([i, s_count, i_count, r_count])
    hist = np.array(hist)
    
    axs.plot(hist[:,0], hist[:,1], c="blue")
    axs.plot(hist[:,0], hist[:,2], c="red")
    axs.plot(hist[:,0], hist[:,3], c="gray")
    axs.legend(["normal", "infected", "removed"])
    plt.show()
live_graph()