import numpy as np, matplotlib as plt
from sklearn.linear_model import LinearRegression

def SIR(history):
    hist = []
    for i, people in enumerate(history):
        for human in people:
            s_count = 0
            i_count = 0
            r_count = 0
            if human.state == "normal" or human.state == "vaccinated": s_count+=1
            if human.state == "infected" or human.state == "infected no symptoms": i_count+=1
            if human.state == "removed": r_count+=1
        hist.append([i, s_count, i_count, r_count])
    hist = np.array(hist)
    
    itercount = hist[:, 0]
    ys = hist[:, 1]
    yi = hist[:, 2]
    yr = hist[:, 3]
    return itercount, ys, yi, yr

def predict(history):
    itercount, ys, yi, yr = SIR(history)
    models = LinearRegression()
    modeli = LinearRegression()
    modelr = LinearRegression()
    models.fit(itercount, ys)
    modeli.fit(itercount, yi)
    modelr.fit(itercount, yr)

    fig, axs = plt.subplots()
    when_to_predict = 5
    axs.scatter(when_to_predict, models.predict(when_to_predict))
    axs.scatter(when_to_predict, modeli.predict(when_to_predict))
    axs.scatter(when_to_predict, modelr.predict(when_to_predict))

    return fig

def R(history, people):
    from sklearn.linear_model import LinearRegression
    """
    for each infectious case:
        count # of transfers
        estimate # of transfers (based on duration)
        average (#tranfers_count, #estimated)
    """
    itercount, _, yi, _ = SIR(history)
    transfer = yi[-1]-yi[-2]
    modeli = LinearRegression()
    modeli.fit(itercount, yi)
    estimate = modeli.predict(itercount[-1]+1)
    return (len(people)**(-1))*(0.5*(transfer+estimate))
