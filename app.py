#SETUP
import streamlit as st, plotly as plt, matplotlib.pyplot as mat, numpy as np, time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from numpy.random import default_rng

rng = default_rng()
st.set_page_config(page_title = "Rhythm Game", layout = "wide")
st.markdown("<h1 style='text-align: center'>Covid Simulation</h1>", unsafe_allow_html=True)

#VARIABLES STORING
state = st.session_state
if "val" not in state:
    state.val = True
    state.simulate = False
    state.people = []

#SIMULATION CONTROLS AND PARAMETERS
with st.sidebar:
    mode = st.multiselect("**Simulation Scenarios**", ["Social Distancing", "Central Area", "Identify + Isolate",
                                                       "Many Cities", "Vaccinate"])
    many_cities = False
    
    #GENERAL SETTINGS
    st.caption("General Settings")
    col1, col2, col3 = st.columns([1.4, 1.4, 1.25])
    population = np.abs(int(col1.number_input("Population")))
    initial_infected = np.abs(int(col2.number_input("Infected")))
    if initial_infected > population:
        st.warning("The amount of infected is bigger than the population. It is now set to equal the population.")
        initial_infected = population
    contact_radius = np.abs(col3.number_input("Interaction radius"))
    recovery_possibility = st.slider("Recovery Possibility (%)", 0, 100, 50)
    fatality = st.slider("Fatality (%)", 0, 100, 50)
    
    #SCENARIOS
    if "Social Distancing" in mode:
        st.caption("Social Distancing")
        distancing = st.radio("Duration", ["None", "Finite", "Infinite"], horizontal = True)
        if distancing == "Finite":
            duration = st.slider("Duration (days)", 5, 365, 30)
    if "Central Area" in mode:
        st.caption("Central Area")
        gather_rate = st.slider("Gathering Rate (%)", 0, 100, 50)
    if "Identify + Isolate" in mode:
        st.caption("Identify + Isolate")
        symptom_showing = st.slider("Symptom Showing (%)", 0, 100, 50)
        infected_threshold = st.slider("Infected threshold (ppl)", 0, 300, 20)
    if "Many Cities" in mode:
        st.caption("Many Cities")
        travel_rate = st.slider("Travel Rate (%)", 0, 100, 50)
        many_cities = True
    if "Vaccinate" in mode:
        st.caption("Vaccinate")
        vaccination_rate = st.slider("Vaccination Rate (%)", 0, 100, 50)
        expire_date = st.slider("Effectiveness (days)", 0, 60, 30)
    

    infect = rng.choice(population, size=initial_infected, replace=False).tolist()
    #st.text(f"{infect, population, initial_infected}")
    state.people = []
    for idx in range(population):
        plot = [np.random.randint(0, 3), np.random.randint(0, 3)] if many_cities else 0
        x = np.random.randint(0, 1000)
        y = np.random.randint(0, 1000)
        state.people.append([plot, x, y, "infected" if idx in infect else "normal"])
    
#st.text(f"{state.people}")

#SIMULATION SCREEN
if st.button("Simulate"):
    live_chart, simulate_screen = st.columns([3,2])
    
    fig, ax = mat.subplots()
    ax.set_ylim(0, 60)
    #ax.axis("off")
    xlabels = ['I', 'II', 'III', 'IV']
    ax.set_xticks(np.arange(4), labels=xlabels)
    ax.bar(np.arange(4), np.arange(5)[1:], 1, bottom=np.arange(4), edgecolor='black')
    live_chart.pyplot(fig)
    
    left, right = simulate_screen.columns(2)
    left.pyplot(fig)
    left.pyplot(fig)
    left.pyplot(fig)
    right.pyplot(fig)
    right.pyplot(fig)
    right.pyplot(fig)
#GAME MECHANICS
a = '''                 with st.container():
                screen, stats = st.columns((0.8, 0.2))
                
                blank, but1, but2, but3, but4 = screen.columns((0.16, 0.21, 0.21, 0.21, 0.21))
                if but1.button("A"):
                    state.score += 1
'''


#BACKEND
def read_file(path):
    with open(path) as f:
        return f.read()
components.html(read_file("index.html"), height=0, width=0)
st.markdown(f'<style>{read_file("index.css")}<style/>', unsafe_allow_html = True)
