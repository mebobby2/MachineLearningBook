import random
import math

# The dorms, each of which has two available spaces
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

# People, along with their first and second choices
prefs = [('Toby', ('Bacchus', 'Hercules')),
         ('Steve', ('Zeus', 'Pluto')),
         ('Andrea', ('Athena', 'Zeus')),
         ('Sarah', ('Zeus', 'Pluto')),
         ('Dave', ('Athena', 'Bacchus')),
         ('Jeff', ('Hercules', 'Pluto')),
         ('Fred', ('Pluto', 'Athena')),
         ('Suzie', ('Bacchus', 'Hercules')),
         ('Laura', ('Bacchus', 'Hercules')),
         ('Neil', ('Hercules', 'Athena'))]

# Number of possible solutions
# S = I ^ P
#   = 10 ^ 5
#   = 100,000
# where I = number of students, P = number of dorms

# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
domain = [(0, (len(dorms)*2)-i-1) for i in range(0, len(dorms)*2)]

# 1. import dorm
# 2. dorm.printsolution([0,0,0,0,0,0,0,0,0,0])
def printsolution(vec):
    slots = []
    # Create two slots for each dorm
    for i in range(len(dorms)): slots += [i,i]

    # Loop over each students assignment
    for i in range(len(vec)):
        x = int(vec[i])

        # Choose the slot from the remaining ones
        dorm = dorms[slots[x]]
        # Show the student and assigned dorm
        print prefs[i][0], dorm
        # Remove this slot
        del slots[x]

def dormcost(vec):
    cost = 0
    # Create the list of slots
    slots = [0,0,1,1,2,2,3,3,4,4]

    # Lopp over each student
    for i in range(len(vec)):
        x = int(vec[i]);
        dorm = dorms[slots[x]]
        pref = prefs[i][1]

        # First choice of costs 0, second choice costs 1
        if pref[0] == dorm: cost += 0
        elif prefs[1] == dorm: cost += 1
        else: cost += 3
        # Not on the list of costs 3

        # Remove selected slot
        del slots[x]

    return cost
