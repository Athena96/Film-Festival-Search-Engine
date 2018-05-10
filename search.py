import string
import math
from read_write import ReadWrite

class FilmFestivalSearch:
    '''
    Responsible for searching the film database
    '''

    def __init__(self):
        # load data
        io = ReadWrite()

        self.film_data = io.read_film_data("film_data.txt")

        self.title_vocab = io.read_vocab("title_vocab.txt")
        self.director_vocab = io.read_vocab("director_vocab.txt")

        self.title_vocab_vectors = io.read_vocab_vectors("title_vocab_vectors.txt")
        self.director_vocab_vectors = io.read_vocab_vectors("director_vocab_vectors.txt")

        # compute avg doc length for title and director
        ts = 0
        ds = 0

        for film in self.film_data:
            title_parts = film[1].split(" ")
            title_parts_lc = [title.lower() for title in title_parts]
            title_parts_lc_noPunc = [title.translate(None, string.punctuation) for title in title_parts_lc]

            director_parts = film[2].split(" ")
            director_parts_lc = [director.lower() for director in director_parts]
            director_parts_lc_npPunc = [director.translate(None, string.punctuation) for director in director_parts_lc]

            ts += len(title_parts_lc_noPunc)
            ds += len(director_parts_lc_npPunc)

        self.avg_title_dl = float(ts) / len(self.film_data)
        self.avg_director_dl = float(ds) / len(self.film_data)



    def decode_vocab_vector(self,encoded_vector):
        '''
        decodes a document/query vector from the compressed form to the
        large "0's and 1's" form to use in scoreing.
        '''
        decoded_vector = [0] * encoded_vector[0]

        for index in encoded_vector[1:len(encoded_vector)]:

            decoded_vector[index] = 1

        return decoded_vector


    def vocab_vector_from_query(self,phrase,vocabulary):
        '''
        creates a vocabulary vector using the given phrase
        this is used to convert the user's input to a vocabulary vector.
        '''
        # vocabulary = ["the","tree","it", ...]
        # phrase = ["the", "tree", ...]

        # init vocab vectors
        vocab_vector = []
        if len(phrase) == 1 and (phrase[0] == "" or phrase[0] == " "):
            vocab_vector.append(len(vocabulary))
            return vocab_vector

        for vocab_idx,word in enumerate(vocabulary):

            if word in phrase:
                if (len(vocab_vector) == 0):
                    vocab_vector.append(len(vocabulary))

                vocab_vector.append(vocab_idx)
        return vocab_vector

    def score(self,query_vector,doc_vector,vocabulary, avg_dl):
        '''
        *
        This is the main scoreing, where VSM is implemented. It also uses
        IDF Weighting and Document Length Normalization.
        *
        '''
        score = 0.0

        for i in range(0,len(vocabulary.keys())):

            # Dot product
            if query_vector[i] == 0 or doc_vector[i] == 0:
                continue

            dot = query_vector[i]*doc_vector[i]

            wd = (vocabulary.keys())[i]
            numTimesAppear = vocabulary[ wd ]
            avgDL = avg_dl

            # IDF weighting
            idf_wt = float( len(self.film_data) + 1.0 ) /  float(numTimesAppear)
            idf_wt = math.log10( idf_wt )
            toAdd = dot*(idf_wt )

            # doc length normalization
            b = 0.5
            docNorm = ( 1.0 - b + b * ( float( sum(doc_vector) ) / avgDL ) )

            toAdd = toAdd / docNorm
            score = score + toAdd

        return score


    def matching_search(self,filmTitle,director):
        '''
        the matching_search is the search algorithm used for:
        - film festival network search
        - director's films search
        it first decides which type of search it is doing, then it iterates over
          the data and if it finds exact matches, it saves the results... otherwise
          the algorithm realizes that the user is trying to search for something but
          doesnt know the exact name, so it does a general search with the given info
          to help user do correct search
         '''

        formatedDoc = ""
        id = 0

        # decide what typoe of search
        if filmTitle == "-":
            id = 2
            director_parts = director.split(" ")
            director_parts_lc = [d.lower() for d in director_parts]
            director_parts_lc_noPunc = [d.translate(None, string.punctuation) for d in director_parts_lc]
            formatedDoc = director_parts_lc_noPunc
        else:
            id = 1
            title_parts = filmTitle.split(" ")
            title_parts_lc = [d.lower() for d in title_parts]
            title_parts_lc_noPunc = [d.translate(None, string.punctuation) for d in title_parts_lc]
            formatedDoc = title_parts_lc_noPunc

        # iterate over data to get matches
        results = []
        noExactMatches = True

        for film in self.film_data:
            q_parts = film[id].split(" ")
            q_parts_lc = [d.lower() for d in q_parts]
            q_parts_lc_noPunc = [d.translate(None, string.punctuation) for d in q_parts_lc]
            formatedQuery = q_parts_lc_noPunc

            # match!
            if set(formatedQuery) == set(formatedDoc):
                noExactMatches = False
                results.append( film )


        # no exact matches
        if noExactMatches:
            # do general search
            if id == 1:
                lst = self.search(filmTitle, "")
            else:
                lst = self.search("", director)
            return (lst[0:5],False)
        else:
            return (results,True)

    def search(self,title_query,director_query):
        '''
        *
        This is the main searching function. It first formats the user's
        title/director query, creates vocabulary vectors from this data, then
        scores these vectors with each document vector from the film database.
        and finally it returns the top 5 matches.
        *
        '''
        # formate the user input
        title_query_parts = title_query.split(" ")
        title_query_parts_lc = [title.lower() for title in title_query_parts]
        title_query_parts_lc_noPunc = [title.translate(None, string.punctuation) for title in title_query_parts_lc]

        director_query_parts = director_query.split(" ")
        director_query_parts_lc = [name.lower() for name in director_query_parts]
        director_query_parts_lc_noPunc = [name.translate(None, string.punctuation) for name in director_query_parts_lc]

        # create vocab vectors from the queries
        io = ReadWrite()
        title_query_vocab_vec_enc = self.vocab_vector_from_query(title_query_parts_lc_noPunc, io.read_vocab_plain("title_vocab.txt"))
        title_query_vocab_vec = self.decode_vocab_vector(title_query_vocab_vec_enc)

        director_query_vocab_vec_enc = self.vocab_vector_from_query(director_query_parts_lc_noPunc, io.read_vocab_plain("director_vocab.txt"))
        director_query_vocab_vec = self.decode_vocab_vector(director_query_vocab_vec_enc)

        # score each film in DB, compared with the queries
        ranking = []

        for idx,film in enumerate(self.film_data):
            doc_title_vec_enc = self.title_vocab_vectors[idx]
            doc_title_vec = self.decode_vocab_vector(doc_title_vec_enc)

            doc_director_vec_enc = self.director_vocab_vectors[idx]
            doc_director_vec = self.decode_vocab_vector(doc_director_vec_enc)

            assert(len(title_query_vocab_vec) == len(doc_title_vec))
            assert(len(director_query_vocab_vec) == len(doc_director_vec))

            s1 = self.score(title_query_vocab_vec, doc_title_vec, self.title_vocab, self.avg_title_dl)
            s2 = self.score(director_query_vocab_vec, doc_director_vec, self.director_vocab, self.avg_director_dl)


            s = s1 + s2

            ranking.append((film,s))

        results = sorted(ranking, key=lambda tup: tup[1], reverse=True)
        return results[0:5]
