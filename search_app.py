import sys
from read_write import ReadWrite
from search import FilmFestivalSearch

# Printing Data
def print_list_of_films(films):
    print("")
    for film in films:
        print("year: \t\t{0}".format(film[0]))
        print("title: \t\t{0}".format(film[1]))
        print("director: \t{0}".format(film[2]))
        print("country: \t{0}".format(film[3]))
        print("festival: \t{0}".format(film[4]))
        print("award?: \t{0}".format(film[5]))
        print("")

def format_print_for_festival_network(results):
    # assuming results = [[],[],...]
    # create dictionary from results
    byFestival = {}

    for film in results:

        if film[4] in byFestival.keys():
            byFestival[film[4]].append(film)
        else:
            byFestival[film[4]] = []
            byFestival[film[4]].append(film)

    # print
    print("")

    for fest in byFestival:
        print("{0} Film Festival".format(fest))
        print_list_of_films(byFestival[fest])

def format_print_for_director(results):
    # assuming results = [[],[],...]
    print("")
    print(results[0][2])
    print_list_of_films(results)


# MAIN

# ensure correct num arguments
if len(sys.argv) == 3:

    # init search class, loads data from database files
    se = FilmFestivalSearch()
    title = sys.argv[1]
    director = sys.argv[2]

    search_results = []

    # search by film, to show f.f. network
    if sys.argv[2] == "-":
        # by film
        (search_results,exact) = se.matching_search(title,"-")
        if exact:
            format_print_for_festival_network(search_results)
        else:
            for r in search_results[0:5]:
                print(r)

    # search by director, to show films they made
    elif sys.argv[1] == "-":
        # by director
        (search_results,exact) = se.matching_search("-",director)
        if exact:
            format_print_for_director(search_results)
        else:
            for r in search_results[0:5]:
                print(r)

    # general search
    elif sys.argv[1] != "-" and sys.argv[2] != "-":
        # film search
        search_results = se.search(title, director)
        for r in search_results[0:5]:
            print(r)

    else:
        # usage error: incorrect formatting
        print("usage error: incorrect formatting")
        sys.exit()


else:
    # usage error: not correct num arguments
    print("usage error: not correct num arguments")
    sys.exit()
