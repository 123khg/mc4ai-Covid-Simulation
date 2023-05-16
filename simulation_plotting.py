import numpy as np
from numpy.random import default_rng
import sklearn.cluster._kmeans as kmc
import matplotlib.pyplot as plt

rng = default_rng()

class Person:
    def __init__(self, plot, x, y, state, quarantine_rate = 0):
        self.plot = plot
        self.x = x
        self.y = y
        self.state = state
        self.quarantine_rate = quarantine_rate/100
        self.vaccin_expire = 0
        
    def move(self, coords, mode, contact_radius, distancing_duration, _norm = np.linalg.norm): 
        vel = 10
        if vel <= self.x <= 1000-vel: 
            x = np.random.randint(low=-vel, high=vel)
        else:
            x = vel*(500-self.x)/(abs(500-self.x)+1)
        if vel <= self.y <= 1000-vel: 
            y = np.random.randint(low=-vel, high=vel)
        else:
            y = vel*(500-self.y)/(abs(500-self.y)+1)

        if "Social Distancing" in mode:
            if distancing_duration > 0:
                thiscoord = np.array([self.x, self.y])
                for coord in coords:
                    dist = _norm(np.array(coord)-thiscoord)
                    if dist <= contact_radius*5:
                        x += 50*vel*(contact_radius/dist) * ((self.x - coord[0])/(abs(self.x - coord[0])+1))
                        y += 50*vel*(contact_radius/dist) * ((self.y - coord[1])/(abs(self.y - coord[1])+1))
        
        self.x += int(x)
        self.y += int(y)

    def die_or_revive(self, fatality, recovery_chance):
        if np.random.binomial(1, recovery_chance/100, 1):
            self.state = "normal"
        elif np.random.binomial(1, fatality/100, 1):
            self.state = "removed"

    def move_between_cities(self, travel_rate):
        if np.random.binomial(1, travel_rate/100, 1):
            self.plot = [np.random.randint(low=0, high=3), np.random.randint(low=0, high=2)]    
            self.x = np.random.randint(-999, 999)
            self.y = np.random.randint(-999, 999)

    def commute_to_center(self, gather_rate):
        if 450 <= self.x <= 550 and 450 <= self.y <= 550:
            self.x = np.random.randint(0, 999)
            self.y = np.random.randint(0, 999)
        if np.random.binomial(1, gather_rate/100, 1):
            self.x = np.random.randint(low=490, high=510)
            self.y = np.random.randint(low=490, high=510)
    
    def quarantine(self, symptom_showing):
        if self.state == "infected no symptoms":
            if np.random.binomial(1, symptom_showing/100, 1):
                self.state = "infected"
        elif self.state == "infected":
            if np.random.binomial(1, self.quarantine_rate, 1):
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
    infected_coords = []
    for idx, someone in enumerate(people):
        if someone.state == "normal":
            for infected in infect_coords:
                if np.linalg.norm(np.array([someone.x, someone.y]) - np.array([infected[0], infected[1]])) <= contact_radius:
                    infected_coords.append(["infected no symptoms" if "Isolate" in mode else "infected", idx])
                    break
    return np.array(infected_coords)

"""
"normal", "infected", "infected no symptoms", "vaccinated", "removed"

colors: blue, red, yellow, green, gray
"""

def drawUI_filter_color(plot_coords, state, plot_state, color="r"): 
    filter = state[plot_coords[:, 2]] == plot_state
    if len(filter):
        kwargs = { 
            "x" : plot_coords[filter, 0], 
            "y" : plot_coords[filter, 1],
            "c" : color
        }
    return kwargs

def drawUI(people=[], mode=[]):
    # people = [Person([1, 1], 5, 10, "normal"), Person([2, 0], 2, 5, "infected"), Person([0, 0], 10, 4, "removed")]
    # mode = ["Many Cities"]
    state = np.array([someone.state for someone in people])
    isolated_coords = []

    #Plot drawing
    if "Many Cities" in mode:
        fig, axs = plt.subplots(3, 2)

        #Create map
        coords = {}
        for row in range(3):
            for col in range(2):
                coords[f"[{row}, {col}]"] = []
        
        #Add coords to map
        for idx, someone in enumerate(people):
            if someone.plot == 1:
                isolated_coords.append([someone.x, someone.y, idx])
            else:
                coords[f"{someone.plot}"].append([someone.x, someone.y, idx])
        
        #Draw
        for row in range(3):
            for col in range(2):
                plot_coords = np.array(coords[f"[{row}, {col}]"])

                axs[row][col].set_xlim(1000)
                axs[row][col].set_ylim(1000)
                axs[row][col].axis("off")
                axs[row][col].plot([0, 1000, 1000, 1, 1], [0, 0, 1000, 1000, 0], c="black")
                
                #Filter color for each state
                if len(plot_coords):
                    if "normal" in state:
                        axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "normal", "b"))
                    if 'infected' in state:
                        axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "infected", "r"))
                    if 'infected no symptoms' in state:
                        axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "infected no symptoms", "y"))
                    if "vaccinated" in state:
                        axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "vaccinated", "g"))
                    if "removed" in state:
                        axs[row][col].scatter(**drawUI_filter_color(plot_coords, state, "removed", "gray"))
    else:
        fig, axs = plt.subplots()
        axs.axis("off")
        axs.set_xlim(1000)
        axs.set_ylim(1000)

        coords = []
        for idx, someone in enumerate(people):
            if someone.plot == 1:
                isolated_coords.append([someone.x, someone.y, idx])
            else:
                coords.append([someone.x, someone.y, idx])
        coords = np.array(coords)

        #Filter color for each state
        if "normal" in state:
            axs.scatter(**drawUI_filter_color(coords, state, "normal", "b"))
        if 'infected' in state:
            axs.scatter(**drawUI_filter_color(coords, state, "infected", "r"))
        if 'infected no symptoms' in state:
            axs.scatter(**drawUI_filter_color(coords, state, "infected no symptoms", "y"))
        if "vaccinated" in state:
            axs.scatter(**drawUI_filter_color(coords, state, "vaccinated", "g"))
        if "removed" in state:
            axs.scatter(**drawUI_filter_color(coords, state, "removed", "gray"))
        axs.plot([0, 1000, 1000, 1, 1], [0, 0, 1000, 1000, 0], c="black")

    if "Isolate" in mode:
        isolated_coords = np.array(isolated_coords)
        isolatefig, isolateaxs = plt.subplots()
        isolateaxs.axis("off")
        isolateaxs.set_xlim(1000)
        isolateaxs.set_ylim(1000)
        if len(isolated_coords):
            isolateaxs.scatter(isolated_coords[:, 0], isolated_coords[:, 1], c="r")
        isolateaxs.plot([0, 1000, 1000, 1, 1], [0, 0, 1000, 1000, 0], c="black")
    else:
        isolatefig = False

    return fig, isolatefig

def live_graph(history): 
    fig, axs = plt.subplots()
    if len(history) > 0: 
        hist = []
        for day, people in enumerate(history):
            sir_count = [0, 0, 0]

            for someone in people:
                if someone.state == "normal" or someone.state == "vaccinated": 
                    sir_count[0] += 1
                if "infect" in str(someone.state): 
                    sir_count[1] += 1
                if someone.state == "removed": 
                    sir_count[2] += 1
                
            hist.append([day, sir_count[0], sir_count[1], sir_count[2]])
        hist = np.array(hist)
        #print(hist, hist[:, 0], hist[:, 1], hist[:, 2], hist[:, 3], type(hist[:,0]))

        axs.plot(hist[:, 0], hist[:, 1], c="blue")
        axs.plot(hist[:, 0], hist[:, 2], c="red")
        axs.plot(hist[:, 0], hist[:, 3], c="gray")
        axs.legend(["normal", "infected", "removed"])
    return fig

def plot_initiate(mode, population, initial_infected, history, distance_duration, quarantine_rate):
    #Create population data
    infect = rng.choice(population, size=initial_infected,replace=False).tolist()
    people = []
    for idx in range(population):
        plot = [np.random.randint(0, 3), np.random.randint(0, 2)] if "Many Cities" in mode else 0
        x = np.random.randint(0, 999)
        y = np.random.randint(0, 999)
        if "Isolate" in mode:
            state = "infected no symptoms" if idx in infect else "normal"
        else:
            state = "infected" if idx in infect else "normal"
        
        people.append(Person(plot, x, y, state, quarantine_rate if "Isolate" in mode else 0))

    #Live graph for real-time analysis
    livefig = live_graph(history)
    fig, isolatefig = drawUI(people, mode)
    fig.tight_layout(pad=0.3)
    return fig, isolatefig, livefig, people, distance_duration

def update(mode, contact_radius, recovery_chance, fatality, distancing_duration_countdown, gather_rate, simulation_state,
           symptom_showing, people, travel_rate, vaccination_chance, expire_date, history):
    if simulation_state != "Pause" or simulation_state != "Stop":
        coords = np.array([[someone.x, someone.y] for someone in people])

        infect_coords = [] 
        for someone in people:
            if someone.state != "removed":
                # Default functionalities
                someone.move(coords, mode, contact_radius, distancing_duration_countdown) #has social distancing

                if "infect" in someone.state:
                    infect_coords.append([someone.x, someone.y])
                    someone.die_or_revive(fatality, recovery_chance)
                
                # Scenarios
                if "Isolate" in mode:
                    someone.quarantine(symptom_showing)
                if "Many Cities" in mode:
                    someone.move_between_cities(travel_rate)
                if "Central Area" in mode:
                    someone.commute_to_center(gather_rate)
                if "Vaccinate" in mode:
                    if someone.state == "normal" or someone.state == "vaccinated":
                        someone.vaccinate(vaccination_chance, expire_date)
            
        
        # Move first, Infect later
        infected_coords = infect(people, infect_coords, contact_radius, mode)
        if len(infected_coords):
            for idx, someone in enumerate(np.array(people)[infected_coords[:, 1].astype(int)]):
                someone.state = infected_coords[idx, 0]

        #Countdown for Social Distancing
        distancing_duration_countdown -= 1

    # draw
    livefig = live_graph(history)
    fig, isolatefig = drawUI(people, mode)
    fig.tight_layout(pad=0.3)
    return fig, isolatefig, livefig, people, distancing_duration_countdown
