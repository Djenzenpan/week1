#!/usr/bin/env python
# Name: Jesse Pannekeet
# Student number: 10151494
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}
with open("movies.csv", "r") as file:
        reader = csv.reader(file)
        movies = list(reader)
        # adds data from csv file to dict after skipping over header row
        for movie in movies[1:]:
            data_dict[movie[2]].append(movie[1])

# replaces movie ratings for each year in data_dict with one average rating
for movie in data_dict:
    sum = 0
    for rating in data_dict[movie]:
        sum = sum + float(rating)
    average = sum/len(data_dict[movie])
    data_dict[movie] = round(average,2)

if __name__ == "__main__":
    # sets y-limits, title and labels for linechart
    # lower y-limit is set to 5 so differences between years are more visible
    plt.ylim(5, 10)
    plt.title('Average rating of movies for each year between 2008-2017')
    plt.xlabel("Year of release")
    plt.ylabel("Average rating (0-10)")
    # creates linechart with the average rating of movies for each year
    plt.plot(range(len(data_dict)), list(data_dict.values()))
    plt.xticks(range(len(data_dict)), list(data_dict.keys()))
    # adds value to every year in the plot
    for i,j in zip(range(len(data_dict)), list(data_dict.values())):
        plt.annotate(str(j),xy=(i - 0.25,j))
    plt.show()

    # sets y-limits, title and labels for the boxplot
    # lower y-limit is set to 5 so differences between years are more visible
    plt.ylim(5, 10)
    plt.title('Average rating of movies for each year between 2008-2017')
    plt.xlabel("Year of release")
    plt.ylabel("Average rating (0-10)")
    # creates a bar plot with the average rating of movies for each year
    # bar plot was chosen because the connecting lines between years do not
    # represent any data, because it makes it easier to connect a year to an
    # average rating and because it increases visibility
    plt.bar(range(len(data_dict)), list(data_dict.values()), align='center',
            color=['green', 'blue'])
    plt.xticks(range(len(data_dict)), list(data_dict.keys()))
    # adds value to each bar in the plot
    for i,j in zip(range(len(data_dict)), list(data_dict.values())):
        plt.annotate(str(j),xy=(i - 0.25,j))
    plt.show()
