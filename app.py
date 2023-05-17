# Influenced by 3Blue1Brown Epidemic


#SETUP
import streamlit as st, numpy as np, pickle as pkl
from streamlit_autorefresh import st_autorefresh
#import streamlit.components.v1 as components
from simulation_plotting import *
from analysis import * 

mode, population, initial_infected, contact_radius, recovery_chance, fatality, = [0]*6
distancing, duration, gather_rate, symptom_showing, = None, 0, 0, 0
quarantine_rate, travel_rate, vaccination_chance, expire_date = [0]*4

st.set_page_config(page_title = "Epidemic Simulation", layout = "wide")
st.markdown("<h1 style='text-align: center'>Epidemic Simulation</h1>", unsafe_allow_html=True)

#VARIABLES STORING
state = st.session_state
if "val" not in state:
    state.val = True
    state.R = [0]
    state.day = 0
    state.simulate = "Configure"
    state.loop = 0
    state.people = []
    state.history = []
    state.archive = []
    state.distance_duration = 0

def Map_Range(low, high, inputlow, inputhigh, input):
    return (high - low)/(inputhigh - inputlow) * (input - inputlow)

#SIMULATION CONTROLS AND PARAMETERS
with st.sidebar:
    mode = st.multiselect("**Simulation Scenarios**",
                          ["Social Distancing", "Central Area",
                           "Isolate", "Many Cities", "Vaccinate"])
    
    #GENERAL SETTINGS
    st.subheader("General Settings")
    
    col1, col2, col3 = st.columns([1.4, 1.4, 1.25])
    population = np.abs(int(col1.number_input("Population")))
    initial_infected = np.abs(int(col2.number_input("Infected")))
    if initial_infected > population:
        st.warning("The amount of infected is bigger than the population. It is now set to equal the population.")
        initial_infected = population
    
    contact_radius = np.abs(col3.number_input("Interaction radius"))
    check_interval = abs(int(st.number_input("How many days until health authorities recheck population (Reproductive R)")))
    recovery_chance = st.slider("Recovery Chance (%)", 0, 100, 0)
    fatality = st.slider("Fatality (%)", 0, 100, 0)
    
    #SCENARIOS SETTINGS
    if "Social Distancing" in mode:
        st.subheader("Social Distancing")
        distancing = st.radio("Duration", ["Finite", "Infinite"], horizontal = True)
        if distancing == "Finite":
            duration = st.slider("Duration (days)", 0, 365, 0)
    if "Central Area" in mode:
        st.subheader("Central Area")
        gather_rate = st.slider("Gathering Rate (%)", 0, 100, 0)
    if "Isolate" in mode:
        st.subheader("Identify + Isolate")
        symptom_showing = st.slider("Symptom Showing (%)", 0, 100, 0)
        quarantine_rate = st.slider("Detection Rate", 0, 100, 0)
    if "Many Cities" in mode:
        st.subheader("Many Cities")
        travel_rate = st.slider("Travel Rate (%)", 0, 100, 0)
    if "Vaccinate" in mode:
        st.subheader("Vaccinate")
        vaccination_chance = st.slider("Vaccination Chance (%)", 0, 100, 0)
        expire_date = st.slider("Effectiveness (days)", 0, 60, 0)
    
#st.text(f"{state.people}")

#CONTROL BUTTONS
simbutt, paubutt, stobutt = st.columns(3)
if simbutt.button("Simulate"):
    state.simulate = "Initiate"
    state.R = [0]
    state.day = 0
    state.loop = 0
    state.people = []
    state.history = []
    state.distance_duration = 0

if state.simulate != "Pause":
    if paubutt.button("Pause"):
        state.simulate = "Pause"
else:
    if paubutt.button("Continue"):
        state.simulate = "Running"
    
if stobutt.button('Stop'):
    state.simulate = 'Stop'
#MAIN LOOP
if state.simulate != "Configure" and state.simulate != "Stop":
    refresh = st_autorefresh(interval=int(Map_Range(900, 4500, 1, 1000, population+population*len(mode)/3)), limit = 2, key=f"{state.loop}")
    state.loop += 1

#SIMULATION SCREEN
if state.simulate != "Configure":
    #Structure
    if "Isolate" in mode:
        live_chart, simulate_screen, isolation_chamber = st.columns(3)
        isolation_chamber.markdown("<h5 style='text-align: center'>Isolation Chamber</h5>", unsafe_allow_html=True)
    else:
        live_chart, simulate_screen = st.columns(2)

    live_chart.markdown("<h5 style='text-align: center'>Live Population Graph</h5>", unsafe_allow_html=True)
    simulate_screen.markdown("<h5 style='text-align: center'>Population</h5>", unsafe_allow_html=True)

    
    #Update loop
    if state.simulate == "Initiate":
        simulate_fig, isolate_fig, live_fig, state.people, state.distance_duration = plot_initiate(
            mode, population, initial_infected, state.history, duration, quarantine_rate)
        simulate_screen.pyplot(simulate_fig)
        state.archive.append([live_fig, simulate_fig, isolate_fig])
        state.simulate = "Running"
    elif state.simulate == "Running":
        #Reason for encoding and decoding is because 1 person is stored as a "class" and each iteration, the properties change
        #And so does the one before when putting them in a history -> can not store
        #Decode
        history = []
        for people in state.history:
            history.append([Person(someone[0], someone[1], someone[2], someone[3], someone[4]) for someone in people])

        simulate_fig, isolate_fig, live_fig, state.people, state.distance_duration = update(
            mode=mode, contact_radius=contact_radius, recovery_chance=recovery_chance, fatality=fatality, 
            distancing_duration_countdown=state.distance_duration, gather_rate=gather_rate, symptom_showing=symptom_showing, 
            history=history, simulation_state=state.simulate, travel_rate=travel_rate, 
            vaccination_chance=vaccination_chance, expire_date=expire_date, people=state.people)
        
        #Effective R
        if state.day % check_interval == 0 and len(state.history):
            state.R.append(Effective_R(history, check_interval))

        #Encode
        people = [[someone.plot, someone.x, someone.y, someone.state, someone.quarantine_rate] for someone in state.people]
        state.history.append(people)
        state.archive[-1] = [live_fig, simulate_fig, isolate_fig]
        state.day += 1

    #Plot
    simulate_screen.pyplot(state.archive[-1][1])
    if "Isolate" in mode:
        isolation_chamber.pyplot(state.archive[-1][2])
    live_chart.pyplot(state.archive[-1][0])

    #Metrics
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    state_counts = state_count(state.people)
    c1.metric("Normal", state_counts[0])
    c2.metric("Vaccinated", state_counts[1])
    c3.metric("Infected", state_counts[2])
    c4.metric("No symptoms", state_counts[3])
    c5.metric("Removed", state_counts[4])
    state_counts.append(round(state.R[-1], 3))
    c6.metric("Reproductive (R)", state_counts[5])
    state_counts.append(", ".join(mode))
    #Use Reproductive R calculated at the bginning gives a better figure for how fast virus spread
    if state.day > 14:
        state_counts[5] = state.R[14//check_interval-1]
    state.archive[-1].append(state_counts)


#if state.simulate == "Stop" or state.simulate == "Configure":
if state.simulate == "Stop":
    pkl.dump(state.archive[-1][0], open(f"Archived runs/fig{len(state.archive)}.pickle", "wb"))

archivetab, databasetab = st.tabs(["Archive", "Pre-made database"])
with archivetab:
    if state.simulate == "Stop" or state.simulate == "Configure":
        for i in range(1, len(state.archive)+1):
            archivetab.markdown(f"<h3 style='text-align: center'>Simulation #{i}: {state.archive[i-1][3][6]}</h3>", unsafe_allow_html=True)
            archivefig = pkl.load(open(f"Archived runs/fig{i}.pickle", "rb"))
            archivefig.suptitle(f"Normal: {state.archive[i-1][3][0]}, Vaccinated: {state.archive[i-1][3][1]}, Infected: {state.archive[i-1][3][2]}, No symptoms: {state.archive[i-1][3][3]}, Removed: {state.archive[i-1][3][4]}, Reproductive (R): {state.archive[i-1][3][5]}", fontsize=12)
            archivetab.pyplot(archivefig)

with databasetab:
    if state.simulate == "Stop" or state.simulate == "Configure":
        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 1: First introduce of virus</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig1.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 2: Wear mask</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig2.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 3: Shopping center, Wear mask</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig3.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 4: Isolate, Social distancing, Wear mask</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig4.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 5: Many cities, Social distancing, Wear mask, Travel</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig5.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 6: Many cities, Shopping centers, Vaccinate, Wear mask, Travel</h3>", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig6.pickle", "rb"))
        databasetab.pyplot(archivefig)

        databasetab.markdown(f"<h3 style='text-align: center'>Simulation 7: Many Cities, Shopping centers, Vaccinate, Isolate, Social distancing, No travel, Wear mask, Wash hands", unsafe_allow_html=True)
        archivefig = pkl.load(open(f"Pre-made database/fig7.pickle", "rb"))
        databasetab.pyplot(archivefig)

if state.simulate == "Stop":   
    state.simulate = "Configure"
    state.loop = 0
    state.R = 0
    state.people = []
    state.history = []
    state.distance_duration = 0

#BACKEND
def read_file(path):
    with open(path) as f:
        return f.read()
#components.html(read_file("index.html"), height=0, width=0)
st.markdown(f'<style>{read_file("index.css")}<style/>', unsafe_allow_html = True)