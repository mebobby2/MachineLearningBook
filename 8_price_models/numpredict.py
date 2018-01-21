from random import random, randint
import math

def wineset1():
    rows = []
    for i in range(300):
        # Create a random age and rating
        rating = random() * 50 + 50
        age = random() * 50

        # Get reference price
        price = wineprice(rating, age)

        # Add some noise
        price *= (random() * 0.4 + 0.8)

        # Add to the dataset
        rows.append({'input': (rating, age), 'result': price})

    return rows

def wineprice(rating, age):
    peak_age = rating - 50

    # Calculate price based on rating
    price = rating/2
    if age > peak_age:
        # Past its peak, goes bad in 5 years
        price = price * (5 - (age - peak_age))
    else:
        # Increases to 5x original value as it approaches peak
        price = price * (5 * ((age + 1)/peak_age))
    if price < 0: price = 0
    return price
