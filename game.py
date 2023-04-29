import streamlit as st, plotly as plt, numpy as np, base64, time

''' Notes for later development:
Make a code that works out a (800, st.screen_width/3) dimension plot for the Piano game mode
Create function to receive position of note, time appear and duration (length) of note to create it on the plot
Warning: do not make the plot shorter (happens when an object's coords is higher than any other which makes the plot shorten)
Hint: try drawing it right at the boundary and only gets bigger when it move downwards
Style the plot to similar ( dont copy :))) ) to Osu Mania

Later improvements would be 2 new game modes: Osu taiko
Same requirements: function that receives time appear and duration of notes (no position this time)
'''
