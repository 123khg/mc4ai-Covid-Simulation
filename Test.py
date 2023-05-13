import streamlit as st, pygame as pg, numpy as np, matplotlib.pyplot as plt, time

people = [["normal", 1 , 1],
        ["normal", 10, 2],
        ["ehh", 5, 4],
        ["bruh", 8, 2]]
infected_coords = np.array([["infected", 0],
                            ["infected no symptoms", 2],
                            ["infected", 3]])
print(infected_coords[:, 1].astype(int))
for idx, someone in enumerate(np.array(people)[infected_coords[:, 1].astype(int)]):
    people[infected_coords[idx, 1].astype(int)][0] = infected_coords[idx, 0]
print(people)