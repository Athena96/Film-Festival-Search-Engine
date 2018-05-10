import sys
import string
from read_write import ReadWrite

class FilmRecommender:
    '''
    This class recommends films to users, given as input a list of tilm titles
        the user likes.
    '''
    def __init__(self):
        # load data
        io = ReadWrite()
        self.data = io.read_film_data("film_data.txt")

    def sim(self,film1, film2):
        '''
        scores the similarity between two films
        '''

        # year similarity
        sy = 0
        diff = abs(int(film1[0]) - int(film2[0]))
        if diff == 0:
            sy = 1.0
        else:
            sy = 1.0/float(diff)

        # Director similarity
        dMatch = 0.0
        if film1[2] == film2[2]:
            dMatch = 1.0
        else:
            dMatch = 0.0

        # country similarity
        cMatch = 0.0
        if film1[3] == film2[3]:
            cMatch = 1.0
        else:
            cMatch = 0.0

        # festival similarity
        fMatch = 0.0
        if film1[4] == film2[4]:
            fMatch = 1.0
        else:
            fMatch = 0.0

        return (sy + dMatch + cMatch + fMatch) / 4.0

    def film_in_list(self,film,list):
        '''
        helper func, check to see if a film is in a list
        '''
        for f in list:
            if f[1] == film[1]:
                return True
        return False

    def recommend(self,likes):
        '''
        takes user likes array and scores each like with each film in database
        returns top 5
        '''
        scored = []

        for film in self.data:

            if self.film_in_list(film,likes):
                continue

            sim = 0

            for liked_film in likes:

                sim += self.sim(liked_film,film)

            scored.append((film,sim))

        # returns top 5 similar
        s = sorted(scored, key=lambda tup: tup[1], reverse=True)
        return s[0:5]
