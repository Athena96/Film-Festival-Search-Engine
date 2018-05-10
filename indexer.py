import string
from read_write import ReadWrite

class FilmFestivalDataIndexer:

    def create_vocabulary(self,data):
        # data = [ ["the","tree","of","life"], ["iron","man"] ]
        vocab = {}

        for vector in data:
            for word in vector:
                if word != " " and word != "":
                    if word in vocab.keys():
                        vocab[word] = vocab[word] + 1
                    else:
                        vocab[word] = 1
                else:
                    print("SKIP",vector)
        return vocab

    def create_vocabulary_vectors(self,vocabulary,data):
        # vocabulary = ["the","tree","it", ...]
        # data = [ ["the","tree","of","life"], ["iron","man"] ]

        # init vocab vectors
        vocab_vectors = []
        for i in range(0,len(data)):
        	vocab_vectors.append([])

        # iterate over data, creating vocab vector for each

        for data_id,vector in enumerate(data):
            # find matches and record the '1' index

            for vocab_idx,word in enumerate(vocabulary):

                if word in vector:
                    if (len(vocab_vectors[data_id]) == 0):
                        vocab_vectors[data_id].append(len(vocabulary))
                    vocab_vectors[data_id].append(vocab_idx)

        return vocab_vectors

    def index(self):
        print("")
        print("Reading in scraped film data...")
        io = ReadWrite()
        film_data = io.read_film_data("film_data.txt") # film_data = [(year,title,director,country,festival,award),...,]

        # 1. Create Film title Vocabulary, write to file
            # Format
        title_strings = [film[1] for film in film_data]
        title_strings_lc = [film.lower() for film in title_strings]
        title_strings_lc_noPunc = [film.translate(None, string.punctuation) for film in title_strings_lc]
        title_parts = [titleStr.split(" ") for titleStr in title_strings_lc_noPunc]

            # compute Vocab
        print("")
        print("Creating Film Title Vocabulary...")
        title_vocab = self.create_vocabulary(data=title_parts)

            # write to file
        print("Writing Film Title Vocabulary to file: title_vocab.txt")
        io.write_vocab("title_vocab.txt", title_vocab)


        # 2. Create Film Director Vocabulary, write to file
            # format
        director_strings = [film[2] for film in film_data]
        director_strings_lc = [film.lower() for film in director_strings]
        director_strings_lc_noPunc = [film.translate(None, string.punctuation) for film in director_strings_lc]
        director_parts = [directorStr.split(" ") for directorStr in director_strings_lc_noPunc]

            # compute vocab
        print("")
        print("Creating Film Director Vocabulary...")
        director_vocab = self.create_vocabulary(data=director_parts)

            # write to file
        print("Writing Film Director Vocabulary to file: director_vocab.txt")
        io.write_vocab("director_vocab.txt", director_vocab)

        # 3. Create vocabulary vectors for each title document, write to file
            # create vectors
        print("")
        print("Creating Film Title Vocabulary Vectors...")
        print("")
        title_vocab_vectors = self.create_vocabulary_vectors(title_vocab.keys(),title_parts)

            # write vectors
        print("Writing Film Title Vocabulary Vectors to file: title_vocab_vectors.txt")
        io.write_vocab_vectors("title_vocab_vectors.txt", title_vocab_vectors)

        # 4. Create vocabulary vectors for each director document, write to file
            # create vectors
        print("")
        print("Creating Film Director Vocabulary Vectors...")
        director_vocab_vectors = self.create_vocabulary_vectors(director_vocab.keys(),director_parts)

            # write vectors
        print("Writing Film Director Vocabulary Vectors to file: director_vocab_vectors.txt")
        io.write_vocab_vectors("director_vocab_vectors.txt", director_vocab_vectors)

i = FilmFestivalDataIndexer()
i.index()
