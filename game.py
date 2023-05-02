import streamlit as st, plotly as plt, numpy as np, base64, time

''' Notes for later development:
Create function to receive position of note, time appear and duration (length) of note to create it on the plot
Style the plot to similar ( dont copy :))) ) to Osu Mania

Later improvements would be 2 new game modes: Osu taiko
Same requirements: function that receives time appear and duration of notes (no position this time)
'''

#The part for screen is already made over on app.py so it will be copied here later
#Only need to make a function that takes in these and output a figure that app.py can use to plot
#width and height are floats;
#notes is a list that has 4 elements which indicates the position of the note on the plot
#duration is a list that also has 4 elements which has the y-length of the note
'''
Heres a hint: use matplotlib plt.bar(x, height, width, y_coord, edge_color = "black"
'''
def Piano(width, height, notes, duration):
    pass
    return fig
    
    
    
def Drums(width, height, notes, duration):
    pass
    return fig
    
    
def Catch(): pass