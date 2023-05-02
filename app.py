#SETUP
import streamlit as st, plotly as plt, matplotlib.pyplot as mat, numpy as np, base64, time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

st.set_page_config(page_title = "Rhythm Game", layout = "wide")
st.markdown("<h1 style='text-align: center'>Rhythm Game</h1>", unsafe_allow_html=True)

with st.sidebar:
    gameMode = st.radio("**Game Mode**", ["Piano", "Drum", "Catch"])

def read_html():
    with open("index.html") as f:
        return f.read()

#VARIABLES STORING
state = st.session_state
if "val" not in state:
    state.val = True
    state.play = False
    state.lives = 20
    state.score = 0
    state.difficulty = "Unknown"

#GAME MECHANICS
def audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

with st.empty():
    with st.container():        
        if state.play:
            #Screen
            fig, ax = mat.subplots()
            fig.set_figheight(3.75)
            ax.set_title(f"{state.difficulty}")
            ax.set_ylim(0, 60)
            #ax.axis("off")
            xlabels = ['I', 'II', 'III', 'IV']
            ax.set_xticks(np.arange(4), labels=xlabels)
            ax.bar(np.arange(4), np.arange(5)[1:], 1, bottom=np.arange(4), edgecolor='black')
            with st.container():
                screen, stats = st.columns((0.8, 0.2))
                screen.pyplot(fig)
                blank, but1, but2, but3, but4 = screen.columns((0.16, 0.21, 0.21, 0.21, 0.21))
                if but1.button("A"):
                    state.score += 1
                but2.button("S")
                but3.button("D")
                but4.button("F")
                stats.metric(label="**Score**", value=f"{state.score}")
                stats.metric(label="**Lives**", value=f"{state.lives}")
                
            #Keyboard event
            components.html(read_html(), height=0, width=0)
        else: 
            state.difficulty = st.select_slider("**Dificulty**", ["Very Easy", "Easy", "Normal", "Hard"])
            if st.button("**Play!**"):
                state.play = True
                st.experimental_rerun()
