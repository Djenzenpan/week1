#!/usr/bin/env python
# Name: Jesse Pannekeet
# Student number: 10151494
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'

def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    # creates list of lists of actors in each movie
    # initialises moviesactors list for storage
    moviesactors = []
    # determines when the program should start adding to the moviesactors list
    actortime = False
    for i in dom.find_all('p'):
        actors = []
        # leaves first value for each movie out of the list as this is the director
        first = True
        director_and_actors = i.find_all('a', href=True)
        for director_or_actor in director_and_actors:
            if director_or_actor.string != None and first == False:
                actors.append(director_or_actor.string)
            first = False
        # only appends to moviesactors list if first movie is found and actors are found
        if len(actors) > 0:
            if actortime == True:
                moviesactors.append(actors)
            if actors[0] == 'Community':
                actortime=True

    # finds all movie ratings and puts them in list
    allratings = []
    # determines when movies are found
    ratings = False
    for rating in dom.find_all('strong'):
        # appends rating to ratings list when first movie is found
        if ratings == True:
            allratings.append(rating.string)
        if 'User Rating' == rating.string:
            ratings = True

    # adds all relevant movie details to the movie list
    movies = []
    # moves over each movie's rating, year, title, actors and runtime
    for rating, year, title, actors, runtime in zip(allratings,
                                                    dom.find_all('span', 'lister-item-year text-muted unbold'),
                                                    dom.find_all('h3'), moviesactors,
                                                    dom.find_all('span', 'runtime')):
        # removes unused characters from release year
        if '(I)' in year.string:
            year.string = year.string[5:9]
        elif '(II)' in year.string:
            year.string = year.string[6:10]
        else:
            year.string = year.string[1:5]
        # removes unused characters from runtime
        runtime.string = runtime.string[:3]

        # adds relevant movie date to a list of movies
        movie = title.a.string, rating, year.string, actors, runtime.string
        movies.append(movie)


    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT
    return[movies]   # REPLACE THIS LINE AS WELL IF APPROPRIATE

def has_class_but_no_id(tag):
    return tag.has_attr('href')

def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])


    # adds all movies to the csv file
    for movie in movies:
        for value in movie:
            writer.writerow(value)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
