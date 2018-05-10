import sys
import string
from recommender import FilmRecommender
from search import FilmFestivalSearch

# Helper function
def print_list_of_films(films):
    '''
    pretty prints a list of films, with their similarity score.
    '''
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

# correcto argumen num
if len(sys.argv) >= 2:

    # read user likes
    likes = sys.argv[1 : len(sys.argv) ]
    liked_film_data = []

    # get a Search engine and recommender
    se = FilmFestivalSearch()
    recommender = FilmRecommender()

    # match user liked films (to get exact titles)
    for titleoflikedfilm in likes:
        result = se.search(titleoflikedfilm,"")
        liked_film_data.append(result[0][0])

    # recomemnd films
    recommendations = recommender.recommend(liked_film_data)

    # print
    print("")
    print("Recommended Films")
    print("")
    print_list_of_films(recommendations)
    print("")
