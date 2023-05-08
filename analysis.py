import streamlit as st, plotly as plt, numpy as np, base64, time

means = []
cov = [[1, 0], [0, 1]]
n = 1
X = []
for i in range(2):
    means.append(np.random.randint(low=0, high=20, size=(2)).tolist())
    X.append(np.random.multivariate_normal(means[i], cov, n))

means = np.array(means)
X = np.array(X)
print(means,"\n", X)

