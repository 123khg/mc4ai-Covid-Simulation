#SETUP
import streamlit as st, plotly as plt, matplotlib.pyplot as mat, numpy as np, time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
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
    state.simulate = "Configure"
    state.loop = 0
    state.people = []
    state.history = []
    state.archive = []
    state.distance_duration = 0

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
    refresh = st_autorefresh(interval=int(1000+population), limit = 2, key=f"{state.loop}")
    state.loop += 1

#SIMULATION SCREEN
if state.simulate != "Configure":
    #Structure
    if "Isolate" in mode:
        live_chart, simulate_screen, isolation_chamber = st.columns(3)
        live_chart.markdown("<h5 style='text-align: center'>Live Population Graph</h5>", unsafe_allow_html=True)
        simulate_screen.markdown("<h5 style='text-align: center'>Population</h5>", unsafe_allow_html=True)
        isolation_chamber.markdown("<h5 style='text-align: center'>Isolation Chamber</h5>", unsafe_allow_html=True)
    else:
        live_chart, simulate_screen = st.columns(2)
        live_chart.markdown("<h5 style='text-align: center'>Live Population Graph</h5>", unsafe_allow_html=True)
        simulate_screen.markdown("<h5 style='text-align: center'>Population</h5>", unsafe_allow_html=True)

    #Reason for encoding and decoding is because 1 person is stored as a "class" and each iteration, the properties change
    #And so does the one before when putting them in a history -> can not store
    #Decode
    history = []
    for people in state.history:
        history.append([Person(someone[0], someone[1], someone[2], someone[3], someone[4]) for someone in people])
    
    #Update loop
    if state.simulate == "Initiate":
        simulate_fig, isolate_fig, live_fig, state.people, state.distance_duration = plot_initiate(
            mode, population, initial_infected, history, duration, quarantine_rate)
        simulate_screen.pyplot(simulate_fig)
        state.archive.append([live_fig, simulate_fig, isolate_fig])
        state.simulate = "Running"
    elif state.simulate == "Running":
        simulate_fig, isolate_fig, live_fig, state.people, state.distance_duration = update(
            mode=mode, contact_radius=contact_radius, recovery_chance=recovery_chance, fatality=fatality, 
            distancing_duration_countdown=state.distance_duration, gather_rate=gather_rate, symptom_showing=symptom_showing, 
            history=history, simulation_state=state.simulate, travel_rate=travel_rate, 
            vaccination_chance=vaccination_chance, expire_date=expire_date, people=state.people)
        state.archive[-1] = [live_fig, simulate_fig, isolate_fig]
    if len(history):
        st.write(R(history, population))
    
    #Encode
    people = [[someone.plot, someone.x, someone.y, someone.state, someone.quarantine_rate] for someone in state.people]
    state.history.append(people)

    #Plot
    simulate_screen.pyplot(state.archive[-1][1])
    if "Isolate" in mode:
        isolation_chamber.pyplot(state.archive[-1][2])
    live_chart.pyplot(state.archive[-1][0])
    st.write("---")
    #st.write(f"{hist[:, 0], hist[:, 1], hist[:, 2], hist[:, 3]}")


if state.simulate == "Stop" or state.simulate == "Configure":
    if state.simulate == "Stop":
        analysis_fig = False
        #analysis_fig = predict(state.history)
        state.archive[-1] = [state.archive[-1][0], analysis_fig]
    analysis_tabs = st.tabs(["Archive", "Analysis"])
    if analysis_tabs == "Archive":
        for live, _ in state.archive:
            analysis_tabs.pyplot(live) 
    elif analysis_tabs == "Analysis":
        for _, analyse in state.archive:
            analysis_tabs.pyplot(analyse)

    if state.simulate == "Stop":   
        state.simulate = "Configure"
        state.loop = 0
        state.people = []
        state.history = []
        state.distance_duration = 0
    
#BACKEND
def read_file(path):
    with open(path) as f:
        return f.read()
components.html(read_file("index.html"), height=0, width=0)
st.markdown(f'<style>{read_file("index.css")}<style/>', unsafe_allow_html = True)