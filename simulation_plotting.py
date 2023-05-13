import numpy as np
from numpy.random import default_rng
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rng = default_rng()

class Person:
    def __init__(self, plot, x, y, state, delay = 5): #"""mode, rng"""):
        self.plot = plot
        self.x = x
        self.y = y
        self.state = state
        self.quarantine_delay = delay # Cuz the officials are too bad they cant isolate quickly
        self.vaccin_expire = 0
        
    def move(self, coords, mode, contact_radius, distancing_duration, _norm = np.linalg.norm): 
        if 3 <= self.x <= 997: 
            x = np.random.randint(low=-100, high=100)
        if 3 <= self.y <= 997: 
            y = np.random.randint(low=-100, high=100)

        if "Social Distancing" in mode:
            if distancing_duration > 0:
                thiscoord = [self.x, self.y]
                for coord in coords:
                    dist = _norm(coord-thiscoord)
                    if dist <= contact_radius*0.2:
                        x += (2/dist) * (self.x - coord[0])/abs((self.x - coord[0]))
                        y += (2/dist) * (self.y - coord[1])/abs((self.y - coord[1]))
        
        self.x += x
        self.y += y

    def die_or_revive(self, fatality, recovery_chance):
        if np.random.binomial(1, recovery_chance/100, 1):
            self.state = "normal"
        elif np.random.binomial(1, fatality/100, 1):
            self.state = "removed"

    def move_between_cities(self, travel_rate):
        if np.random.binomial(1, travel_rate/100, 1):
            if "Many Cities" in self.mode:
                self.plot = [np.random.randint(low=1, high=3), np.random.randint(low=1, high=2)]    

    def commute_to_center(self, gather_rate):
        if "Central Area" in self.mode:
            if np.random.binomial(1, gather_rate/100, 1) and self.x != 500 and self.y != 500:
                self.x = 500
                self.y = 500
            elif self.x == 500 and self.y == 500:
                self.x = np.random.randint(0, 1000)
                self.y = np.random.randint(0, 1000)
    
    def quarantine(self, symptom_showing):
        if self.state == "infected no symptoms":
            if np.random.binomial(1, symptom_showing/100, 1):
                self.state = "infected"
        elif self.state == "infected":
            if self.quarantine_delay > 0:
                self.quarantine_delay -= 1
            else:
                self.plot = 1
    
    def vaccinate(self, vaccination_chance, expire_date):
        if self.state == "normal":
            if np.random.binomial(1, vaccination_chance/100, 1):
                self.state = "vaccinated"
                self.vaccin_expire = expire_date
        elif self.state == "vaccinated":
            if self.vaccin_expire > 0:
                self.vaccin_expire -= 1
            else:
                self.state = "normal"
                          
def infect(people, infect_coords, contact_radius, mode):

    for someone in people:
        if someone.state == "normal":
            for infected in infect_coords:
                if np.linalg.norm([someone.x, someone.y] - [infected[0], infected[1]]) <= contact_radius:
                    someone.state == "infected no symptoms" if "Isolate" in mode else "infected"
    return people

"""
"normal", "infected", "infected no symptoms", "vaccinated", "removed"

colors: blue, red, yellow, green, gray
"""

def drawUI_filter_color(plot_coords, state, plot_state, color="r"):
    #plot_coords=np.array([[1, 2, 0], [3, 2, 1], [5, 8, 2], [10, 0, 3]])
    #state=np.array(["normal", "infected", "normal", "infected"])
    #plot_state="normal"
    #color="r"
    #print(np.where(state == plot_state)[0])
    #print(plot_coords[:, 2])
    filter = plot_coords[np.where(state == plot_state)[0], 2] #find idx of type, get array, filter people of plot
    #print(filter)
    kwargs = {
        "x" : plot_coords[filter, 0],
        "y" : plot_coords[filter, 1],
        "c" : color
    }
    return kwargs
#drawUI_filter_color()

def drawUI(people, mode):
    state = np.array([someone.state for someone in people])
    isolated_coords = []
    if "Many Cities" in mode:
        fig, axs = plt.subplots([3, 2])

        coords = {}
        for row in range(3):
            for col in range(2):
                coords[[row, col]] = []
        
        for idx, someone in enumerate(people):
            if someone.plot == 1:
                isolated_coords.append([someone.x, someone.y, idx])
            else:
                coords[someone.plot].append([someone.x, someone.y, idx])

        for row in range(3):
            for col in range(2):
                plot_coords = np.array(coords[[row, col]])
                #Filter color for each state
                axs[row][col].set_xlim(1000)
                axs[row][col].set_ylim(1000)
                axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "normal", "b"))
                axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "infected", "r"))
                axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "infected no symptoms", "y"))
                axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "vaccinated", "g"))
                axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "removed", "gray"))
                
    else:
        fig, axs = plt.subplots()
        axs.set_xlim(1000)
        axs.set_ylim(1000)
        coords = []
        for idx, someone in enumerate(people):
            if someone.plot == 1:
                isolated_coords.append([someone.x, someone.y, idx])
            else:
                coords.append([someone.x, someone.y, idx])
        coords = np.array(coords)
        axs.scatter(**drawUI_filter_color(coords, state, "normal", "b"))
        axs.scatter(**drawUI_filter_color(coords, state, "infected", "r"))
        axs.scatter(**drawUI_filter_color(coords, state, "infected no symptoms", "y"))
        axs.scatter(**drawUI_filter_color(coords, state, "vaccinated", "g"))
        axs.scatter(**drawUI_filter_color(coords, state, "removed", "gray"))

    if "Isolate" in mode:
        isolated_coords = np.array(isolated_coords)
        isolatefig, isolateaxs = plt.subplots()
        isolateaxs.set_xlim(1000)
        isolateaxs.set_ylim(1000)
        isolateaxs.scatter(isolated_coords[:, 0], isolated_coords[:, 1], c="r")
    else:
        isolatefig = False

    return fig, isolatefig

def live_graph(history): 
    fig, axs = plt.subplots()
    if len(history) > 0:
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

def plot_initiate(mode, population, initial_infected, history=[], distance_duration=0):
    #Create population data
    infect = rng.choice(population, size=initial_infected,replace=False).tolist()
    people = []
    for idx in range(population):
        plot = [np.random.randint(0, 3), np.random.randint(0, 2)] if "Many Cities" in mode else 0
        x = np.random.randint(0, 1000)
        y = np.random.randint(0, 1000)
        if "Isolation" in mode:
            state = "infected no symptoms" if idx in infect else "normal"
        else:
            state = "infected" if idx in infect else "normal"
        people.append(Person(plot, x, y, state))
    history.append(people)

    #Live graph for real-time analysis
    livefig = live_graph(history)
    fig, isolatefig = drawUI(people, mode)
    fig.tight_layout(pad=0.3)
    return fig, isolatefig, livefig, people, history, distance_duration

def update(mode, contact_radius, recovery_chance, fatality, distancing_duration_countdown, gather_rate, 
           symptom_showing, people, infected_threshold, travel_rate, vaccination_chance, expire_date, history):
    
    coords = np.array([[someone.x, someone.y] for someone in people])
    infect_coords = [] 
    for someone in people:
        if someone.state != "removed":
            # Default functionalities
            someone.move(coords, coords, mode, contact_radius, distancing_duration_countdown) #has social distancing

            if "infect" in someone.state:
                infect_coords.append([someone.x, someone.y])
                someone.die_or_revive(fatality, recovery_chance)
            
            # Scenarios
            if "Isolate" in mode:
                someone.quarantine(symptom_showing, infected_threshold)
            if "Many Cities" in mode:
                someone.move_between_cities(travel_rate)
            if "Central Area" in mode:
                someone.commute_to_center(gather_rate)
            if "Vaccinate" in mode:
                if someone.state == "normal" or someone.state == "vaccinated":
                    someone.vaccinate(vaccination_chance, expire_date)
    # Move first, infect later
    people = infect(people, infect_coords, contact_radius, mode)       

    #Countdown for Social Distancing
    distancing_duration_countdown -= 1

    # draw
    livefig = live_graph(history)
    fig, isolatefig = drawUI(people, mode)
    fig.tight_layout(pad=0.3)
    return fig, isolatefig, livefig, people, history, distancing_duration_countdown
