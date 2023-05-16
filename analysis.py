import numpy as np, matplotlib as plt
from simulation_plotting import live_graph
from sklearn.linear_model import LinearRegression

def state_count(people):
    count = [0, 0, 0, 0, 0]
    for someone in people:
        if someone.state == "normal":
            count[0] += 1
        elif someone.state == "vaccinated": 
            count[1] += 1
        elif someone.state == "infected": 
            count[2] += 1
        elif someone.state == "infected no symptoms": 
            count[3] += 1
        else: #removed
            count[4] += 1
    return count

def SIR(history):
    hist = []
    for people in history:
        sir_count = [0, 0, 0]

        for someone in people:
            if someone.state == "normal" or someone.state == "vaccinated": 
                sir_count[0] += 1
            elif someone.state == 'infected' or someone.state == "infected no symptoms": 
                sir_count[1] += 1
            else: 
                sir_count[2] += 1
            
        hist.append([sir_count[0], sir_count[1], sir_count[2]])
    hist = np.array(hist)
    
    ys = hist[:, 0]
    yi = hist[:, 1]
    yr = hist[:, 2]
    return ys, yi, yr

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
    axs.show()
    return fig

def Effective_R(history):
    """
    for # number of infected people on 1st day (N0)
    check # number of infected after some interval (N1)
    divide N0 / N1 -> R0
    N1 is affected by contact chance and how people behave -> not a const, fluctuate
    R0 applies when no immunities and no one has ever got the disease (100% susceptible)
    """
    _, yi, _ = SIR(history)
    return yi[-1] / yi[-3]


# from simulation_plotting import Person

# Effective_R(history = [[Person(0, 0, 1,"normal", 0),
#             Person(0, 5, 6, "infected no symptoms", 0),
#             Person(0, 10, 2, "removed", 0),
#             Person(0, 6, 7, "infected", 0)],
#             [Person(0, 0, 1,"infected", 0),
#             Person(0, 5, 6, "infected no symptoms", 0),
#             Person(0, 10, 2, "removed", 0),
#             Person(0, 6, 7, "removed", 0)],
#             [Person(0, 0, 1,"normal", 0),
#             Person(0, 5, 6, "infected", 0),
#             Person(0, 10, 2, "removed", 0),
#             Person(0, 6, 7, "removed", 0)],
#             [Person(0, 0, 1,"vaccinated", 0),
#             Person(0, 5, 6, "removed", 0),
#             Person(0, 10, 2, "removed", 0),
#             Person(0, 6, 7, "removed", 0)]])




    # itercount, _, yi, _ = SIR(history)
    # yesterday = itercount[-1] 
    # predicted_day = yesterday + 5
    # predicted_day = np.array(predicted_day)
    # predicted_day = predicted_day.reshape(-1, 1)
    # itercount = np.array(itercount)
    # itercount = itercount.reshape(-1, 1)
    # if len(yi) >= 2:
    #     transfer = yi[len(yi)-1]-yi[len(yi)-2] 
    #     # print(transfer)
    # else: transfer = yi[0]
    # modeli = LinearRegression()
    # modeli.fit(itercount, yi)
    # estimate = modeli.predict(predicted_day)
    # estimate = estimate[0]
    # if estimate < 0: estimate = 0
    # return (0.5*(transfer+estimate))/yi[-2]


# # test area
# itercount, ys, yi, yr = SIR(    
#     history = [[Person(0, 0, 1,"normal", 0),
#                 Person(0, 5, 6, "infected no symptoms", 0),
#                 Person(0, 10, 2, "removed", 0),
#                 Person(0, 6, 7, "infected", 0)],
#                 [Person(0, 0, 1,"infected", 0),
#                 Person(0, 5, 6, "infected no symptoms", 0),
#                 Person(0, 10, 2, "removed", 0),
#                 Person(0, 6, 7, "removed", 0)],
#                 [Person(0, 0, 1,"normal", 0),
#                 Person(0, 5, 6, "infected", 0),
#                 Person(0, 10, 2, "removed", 0),
#                 Person(0, 6, 7, "removed", 0)],
#                 [Person(0, 0, 1,"vaccinated", 0),
#                 Person(0, 5, 6, "removed", 0),
#                 Person(0, 10, 2, "removed", 0),
#                 Person(0, 6, 7, "removed", 0)]])


