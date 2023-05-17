import numpy as np

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

def Effective_R(history, interval):
    """
    for # number of infected people on 1st day (N0)
    check # number of infected after some interval (N1)
    divide N0 / N1 -> R0
    N1 is affected by contact chance and how people behave -> not a const, fluctuate
    R0 applies when no immunities and no one has ever got the disease (100% susceptible)
    """
    _, yi, _ = SIR(history)
    return yi[-1] / yi[-interval]