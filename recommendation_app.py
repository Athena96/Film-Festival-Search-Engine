import sys
import string
from recommender import FilmRecommender
from search import FilmFestivalSearch

def print_list_of_films(films):
    print("")
    for film in films:
        print("score: {0}".format(film[1]))
        print("year: \t\t{0}".format(film[0][0]))
        print("title: \t\t{0}".format(film[0][1]))
        print("director: \t{0}".format(film[0][2]))
        print("country: \t{0}".format(film[0][3]))
        print("festival: \t{0}".format(film[0][4]))
        print("award?: \t{0}".format(film[0][5]))
        print("")

if len(sys.argv) >= 2:

    likes = sys.argv[1 : len(sys.argv) ]
    liked_film_data = []

    se = FilmFestivalSearch()
    recommender = FilmRecommender()

    for titleoflikedfilm in likes:
        result = se.search(titleoflikedfilm,"")
        liked_film_data.append(result[0][0])

    recommendations = recommender.recommend(liked_film_data)

    print("")
    print("Recommended Films")
    print("")
    print_list_of_films(recommendations)
    print("")
