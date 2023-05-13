#SETUP
import streamlit as st, plotly as plt, matplotlib.pyplot as mat, numpy as np, time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from simulation_plotting import *
# from analysis import * 


st.set_page_config(page_title = "Epidemic Simulation", layout = "wide")
st.markdown("<h1 style='text-align: center'>Epidemic Simulation</h1>", unsafe_allow_html=True)

#VARIABLES STORING
state = st.session_state
if "val" not in state:
    state.val = True
    state.simulate = "Configure"
    state.people = []
    state.history = []
    state.archive = []
    state.distance_duration = 0
    state.loop = 0

mode, population, initial_infected, contact_radius, recovery_chance, fatality, = [0]*6
distancing, duration, gather_rate, symptom_showing, = None, 0, 0, 0
infected_threshold, travel_rate, vaccination_chance, expire_date = [0]*4

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
    
    #SCENARIOS
    if "Social Distancing" in mode:
        st.subheader("Social Distancing")
        distancing = st.radio("Duration", ["Finite", "Infinite"], horizontal = True)
        if distancing == "Finite":
            duration = st.slider("Duration (days)", 5, 365, 0)
    if "Central Area" in mode:
        st.subheader("Central Area")
        gather_rate = st.slider("Gathering Rate (%)", 0, 100, 0)
    if "Isolate" in mode:
        st.subheader("Identify + Isolate")
        symptom_showing = st.slider("Symptom Showing (%)", 0, 100, 0)
        infected_threshold = st.slider("Infected threshold (ppl)", 0, 300, 150)
    if "Many Cities" in mode:
        st.subheader("Many Cities")
        travel_rate = st.slider("Travel Rate (%)", 0, 100, 0)
    if "Vaccinate" in mode:
        st.subheader("Vaccinate")
        vaccination_chance = st.slider("Vaccination Chance (%)", 0, 100, 0)
        expire_date = st.slider("Effectiveness (days)", 0, 60, 30)



#BUTTON CONTROLS
simbutt, paubutt, stobutt = st.columns(3)
if simbutt.button("Simulate"):
    if state.simulate == "Configure":
        state.simulate = "Initiate"
    elif state.simulate == "Initiate" or state.simulate == "Running":
        state.simulate == "Running"

if state.simulate != "Pause":
    if paubutt.button("Pause"):
        state.simulate = "Pause"
else:
    if paubutt.button("Continue"):
        state.simulate = "Running"

if stobutt.button('Stop'):
    state.simulate = 'Stop'

if state.simulate != "Configure" and state.simulate != "Stop":
    refresh = st_autorefresh(interval=1000, limit = 2, key=f"{state.loop}")
    state.loop += 1

#SIMULATION SCREEN
if state.simulate != "Configure":
    live_chart, simulate_screen = st.columns(2)
    if state.simulate == "Initiate":
        simulate_fig, isolate_fig, live_fig, state.people, state.history, state.distance_duration = plot_initiate(
            mode, population, initial_infected, history=state.history, distance_duration=duration)
        state.simulate = "Running"
    elif state.simulate != "Stop":
        simulate_fig, isolate_fig, live_fig, state.people, state.history, state.distance_duration = update(
            mode=mode, contact_radius=contact_radius, recovery_chance=recovery_chance, fatality=fatality, gather_rate=gather_rate,
            distancing_duration_countdown=state.distance_duration, simulation_state=state.simulate, people=state.people,
            symptom_showing=symptom_showing, history=state.history, infected_threshold=infected_threshold, 
            travel_rate=travel_rate, vaccination_chance=vaccination_chance, expire_date=expire_date)
            
    simulate_screen.pyplot(simulate_fig)
    live_chart.pyplot(live_fig)
    #live_chart.write(R(state.history, state.people))

if state.simulate == "Stop" or state.simulate == "Configure":
    if state.simulate == "Stop":
        analysis_fig = False
        #analysis_fig = predict(state.history)
        state.archive.append([live_fig, analysis_fig])

    analysis_tabs = st.tabs(["Archive", "Analysis"])
    if analysis_tabs == "Archive":
        for live, _ in state.archive:
            analysis_tabs.pyplot(live) 
    elif analysis_tabs == "Analysis":
        for _, analyse in state.archive:
            analysis_tabs.pyplot(analyse)

    if state.simulate == "Stop":   
        state.simulate = "Configure"
        state.people = []
        state.history = []
        state.distance_duration = 0
        state.loop = 0

#BACKEND
def read_file(path):
    with open(path) as f:
        return f.read()
components.html(read_file("index.html"), height=0, width=0)
st.markdown(f'<style>{read_file("index.css")}<style/>', unsafe_allow_html = True)