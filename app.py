#SETUP
import streamlit as st, plotly as plt, matplotlib.pyplot as mat, numpy as np, time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from simulation_plotting import *

mode, population, initial_infected, contact_radius, recovery_chance, fatality, = [0]*6
distancing, distancing_duration, center_gather_rate, symptom_showing, = None, 0, 0, 0
infected_threshold, travel_rate, vaccination_chance, expire_date = [0]*4

st.set_page_config(page_title = "Rhythm Game", layout = "wide")
st.markdown("<h1 style='text-align: center'>Covid Simulation</h1>", unsafe_allow_html=True)

#VARIABLES STORING
state = st.session_state
if "val" not in state:
    state.val = True
    state.simulate = False
    state.people = []
    state.history = []

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
    recovery_chance = st.slider("Recovery Chance (%)", 0, 100, 50)
    fatality = st.slider("Fatality (%)", 0, 100, 50)
    
    #SCENARIOS
    if "Social Distancing" in mode:
        st.subheader("Social Distancing")
        distancing = st.radio("Duration", ["Finite", "Infinite"], horizontal = True)
        if distancing == "Finite":
            duration = st.slider("Duration (days)", 5, 365, 30)
    if "Central Area" in mode:
        st.subheader("Central Area")
        gather_rate = st.slider("Gathering Rate (%)", 0, 100, 50)
    if "Isolate" in mode:
        st.subheader("Identify + Isolate")
        symptom_showing = st.slider("Symptom Showing (%)", 0, 100, 50)
        infected_threshold = st.slider("Infected threshold (ppl)", 0, 300, 20)
    if "Many Cities" in mode:
        st.subheader("Many Cities")
        travel_rate = st.slider("Travel Rate (%)", 0, 100, 50)
    if "Vaccinate" in mode:
        st.subheader("Vaccinate")
        vaccination_chance = st.slider("Vaccination Chance (%)", 0, 100, 50)
        expire_date = st.slider("Effectiveness (days)", 0, 60, 30)
    
#st.text(f"{state.people}")

#SIMULATION SCREEN
if st.button("Simulate"):
    live_chart, simulate_screen = st.columns(2)
    
    hh = '''fig, ax = mat.subplots()
    ax.set_ylim(0, 60)
    #ax.axis("off")
    xlabels = ['I', 'II', 'III', 'IV']
    ax.set_xticks(np.arange(4), labels=xlabels)
    ax.bar(np.arange(4), np.arange(5)[1:], 1, bottom=np.arange(4), edgecolor='black')
    live_chart.pyplot(fig)'''
    left, right = simulate_screen.columns(2)
    
    if not state.simulate:
        (simulate_fig, isolate_fig), live_fig, state.people, state.history = plot_initiate(
            mode, population, initial_infected, contact_radius, recovery_chance, fatality,
            distancing=None, distancing_duration=0, center_gather_rate=0, symptom_showing=0,
            infected_threshold=0, travel_rate=0, vaccination_chance=0, expire_date=0)
        state.simulate = True
    else:
        (simulate_fig, isolate_fig), live_fig, state.people, state.history = plot_initiate(
            mode, population, initial_infected, contact_radius, recovery_chance, fatality,
            distancing=None, distancing_duration=0, center_gather_rate=0, symptom_showing=0,
            infected_threshold=0, travel_rate=0, vaccination_chance=0, expire_date=0)

    simulate_screen.pyplot(simulate_fig)
    live_chart.pyplot(live_fig)

#BACKEND
def read_file(path):
    with open(path) as f:
        return f.read()
components.html(read_file("index.html"), height=0, width=0)
st.markdown(f'<style>{read_file("index.css")}<style/>', unsafe_allow_html = True)
