import numpy as np
from numpy.random import default_rng
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rng = default_rng()

class Person:
    def __init__(self, plot, x, y, state, delay = 5):
        self.plot = plot
        self.x = x
        self.y = y
        self.state = state
        self.delay = delay # Cuz the officials are too bad they cant isolate quickly

    def quarantine(self):
        if self.state == 'infected':
            '''1. Check if infected ( has symptom )
            2. Check delay
            3. Delay not 0 -> self.delay -= 1
            4. Delay = 0 -> self.plot -> isolate
            so the normal one is 0 for default
            [2,3] smthing for many cities
            make it 1 ( like 1 plot is 0 and the isolation chamber is 1 )
            '''
            if self.delay > 0: self.delay -= 1
            else: self.plot = 1
            # guess that's it for update()
        pass
        
    def move(self): 
        if 3 <= self.x <= 997: 
            self.x = self.x + np.random.randint(low=-3, high=3)
        if 3 <= self.y <= 997: 
            self.y = self.y + np.random.randint(low=-3, high=3)
            
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

        coords = {}
        for row in range(3):
            for col in range(2):
                coords[[row, col]] = []
        
        for someone in people:
            coords[someone.plot].append([someone.x, someone.y])

        for row in range(3):
            for col in range(2):
                axs[row][col].scatter(
                    np.array(coords[[row, col]])[:, 0],
                    np.array(coords[[row, col]])[:, 1])
        
    else:
        fig, axs = plt.subplots()
    
        coords = []
        for someone in people:
            coords.append([someone.x, someone.y])
        coords = np.array(coords)
        axs.scatter(coords[:, 0], coords[:, 1])

    isolatefig = False
    if "Isolate" in mode:
        isolatefig, isolateaxs = plt.subplots() #Over here
        #replace this plt.subplots() into a function that returns isolatefig and axs
        #so basically, hang on. Imma add a new property to "Person" called quarantine delay
        # ok and how does the update() thingy work
        # So
        '''1. Check if infected
        2. Check delay
        3. Delay not 0 -> self.delay -= 1
        4. Delay = 0 -> self.plot -> isolate
        so the normal one is 0 for default
        [2,3] smthing for many cities
        make it 1 ( like 1 plot is 0 and the isolation chamber is 1 )
'''
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
    return fig

def update(people, history):
    # change values here
    for someone in Person:
        someone.move()
        someone.quarantine()
    # draw
    live_graph(history)
'''
so like in this "people" list
u have 1st: x, y coords and plot index for plotting
2nd: state -> color
from history
3rd: state -> live graph

wait so update's just drawing all the data from people/history?

draw first -> change the values


need quarantine() to count and add them to each plots (aka changing their self.plot)
need people to Move() -> to update their position -> New people -> New history
need fig = Plotting for simulation
need isolatefig = Function()
need live_fig = Live_graph()
for now thats it

Need to return this : 

(fig, isolatefig), livefig, people, history
'''