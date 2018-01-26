import random
import math

def annealingoptimize(domain, costf, T = 10000.0, cool = 0.95, step = 1):
    # Initialize the values randomly
    vec = [int(random.randint(domain[i][0], domain[i][1]))
            for i in range(len(domain))]

    while T > 0.1:
        # Choose one of the indices
        i = random.randint(0, len(domain)-1)

        # Choose a direction to change it
        dir = random.randint(-step, step)

        # Create a new list with one the values changed
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]: vecb[i] = domain[i][1]

        # Calculate the current cost and the new cost
        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e,(-eb-ea)/T)

        # Is is better, or does it make the probability cutoff?
        if (eb < ea or random.random() < p):
            vec = vecb

        # Decrease the temperature
        T = T * cool
    return vec

def geneticoptimize(domain, costf, popsize = 50, step = 1, mutprod=0.2, elite=0.2, maxiter=100):
    # Mutation Operation
    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        if random.random() < 0.5 and vec[i] >= domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i] <= domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]

    # Crossover Operation
    def crossover(r1,r2):
        i = random.randint(1, len(domain)-2)
        return r1[0:i]+r2[i:]

    # Build the initial population
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1])
                for i in range(len(domain))]
        pop.append(vec)

    # How many winners from each generation?
    topelite = int(elite*popsize)

    # Main loop
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked = [v for (s,v) in scores]

        # Start with the pure winners
        pop = ranked[0:topelite]

        # Add the mutated and bred forms of the winners
        while len(pop) < popsize:
            if random.random() < mutprod:
                # Mutation
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                # Crossover
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        # Print the current best score
        print scores[0][0]

    return scores[0][1]
