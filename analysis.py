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




# code for analysis, might gonna need some changes for it to be compatible w/ streamlit (also how to get hist into this file for the regression thing)
from simulation_plotting import live_graph

fig = live_graph(hist)

X = [i for i in range(len(hist))]
ys = hist[:,1]
yi = hist[:,2]
yr = hist[:,3]

def predict(X, ys, yi, yr):
    from sklearn.linear_model import LinearRegression
    models = LinearRegression()
    modeli = LinearRegression()
    modelr = LinearRegression()
    models.fit(X, ys)
    modeli.fit(X, yi)
    modelr.fit(X, yr)

    when_to_predict = int(input())
    fig.scatter(when_to_predict, models.predict(when_to_predict))
    fig.scatter(when_to_predict, modeli.predict(when_to_predict))
    fig.scatter(when_to_predict, modelr.predict(when_to_predict))
    fig.show()
    return fig

predict(X, ys, yi, yr)


