import math

people = ['Charlie', 'Augustus', 'Veruca', 'Violet', 'Mike', 'Joe', 'Willy', 'Miranda']

links = [('Augustus', 'Willy'),
         ('Mike', 'Joe'),
         ('Miranda', 'Mike'),
         ('Violet', 'Augustus'),
         ('Miranda', 'Willy'),
         ('Charlie', 'Mike'),
         ('Veruca', 'Joe'),
         ('Miranda', 'Augustus'),
         ('Willy', 'Augustus'),
         ('Joe', 'Charlie'),
         ('Veruca', 'Augustus'),
         ('Miranda', 'Joe')]

def crosscount(v):
    # Convert the number list into a dictionary of person:(x,y)
    loc = dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total = 0

    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i+1, len(links)):
