import numpy as np, matplotlib as plt
from simulation_plotting import live_graph
from sklearn.linear_model import LinearRegression



def SIR(history):
    population = len(history[-1])
    hist = []
    for day, people in enumerate(history):
        sir_count = [0, 0, 0]

        for someone in people:
            if someone.state == "normal" or someone.state == "vaccinated": 
                sir_count[0] += 1
            if "infect" in str(someone.state): 
                sir_count[1] += 1
            if someone.state == "removed": 
                sir_count[2] += 1
            
        hist.append([day, sir_count[0], sir_count[1], sir_count[2]])
    hist = np.array(hist)
    
    itercount = hist[:, 0]
    ys = hist[:, 1]
    yi = hist[:, 2]
    yr = hist[:, 3]
    return itercount, ys, yi, yr, population

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

def R(history, population): #lol thx i was abt to change that too =))))
    from sklearn.linear_model import LinearRegression
    """
    for each infectious case:
        count # of transfers
        estimate # of transfers (based on duration)
        average (#tranfers_count, #estimated)
    """
    # history = [[Person(0, 0, 1,"normal"),
    #             Person(0, 5, 6, "infected no symptoms"),
    #             Person(0, 10, 2, "removed"),
    #             Person(0, 6, 7, "infected")],
    #             [Person(0, 0, 1,"infected"),
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
    #             Person(0, 6, 7, "removed"), 0],]
    #press Ctrl + / to uncomment many lines i made this test history when doing live_graph
    # ok but what's the people lol len(people) is population, i just forgot that we have a var for it, wait nvm, we can get it
    # my take when we forget our code is scrap everything and redo, cuz its better when we take another approach to the problem
    # 
    itercount, _, yi, _, _ = SIR(history)
    yesterday = itercount[-1]
    predicted_day = yesterday + 5
    predicted_day = np.array(predicted_day)
    predicted_day = predicted_day.reshape(-1, 1)
    itercount = np.array(itercount)
    print(itercount)
    itercount = itercount.reshape(-1, 1)
    print(itercount)
    print(yi)
    if len(yi) >= 2:
        transfer = yi[len(yi)-1]-yi[len(yi)-2] 
        print(transfer)
    else: transfer = yi[0]
    modeli = LinearRegression()
    modeli.fit(itercount, yi)
    estimate = modeli.predict(predicted_day)
    estimate = estimate[0]
    print(estimate)
    return (0.5*(transfer+estimate))/population

#from simulation_plotting import Person

# test area
# itercount, ys, yi, yr, population = SIR(    history = [[Person(0, 0, 1,"normal", 0),
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

# r = R(itercount, yi, population)
# print(r)

