import os.path

class ReadWrite:
    '''
    Responsible for reading and writing from files
    '''

    @staticmethod
    def read_vocab(filename):
        '''
        reads a vocabulary from a file
        '''
        file = open(filename, 'r')

        vocab = {}

        for idx,line in enumerate(file):

            line = line.replace("\n","")

            parts = line.split(" ")

            vocab[parts[0]] = int(parts[1])


        return vocab

    @staticmethod
    def read_vocab_plain(filename):
        '''
        reads a vocabulary from a file, but saves in ordered array instead of
            dictionary.
        '''
        file = open(filename, 'r')

        vocab = []

        for idx,line in enumerate(file):

            line = line.replace("\n","")

            parts = line.split(" ")

            vocab.append(parts[0])

        return vocab

    @staticmethod
    def read_vocab_vectors(filename):
        '''
        reads vocabulary vecotrs from file
        '''
        file = open(filename, 'r')

        vectors = []

        for idx,line in enumerate(file):

            line = line.replace("\n","")
            vector_str_parts = line.split(",")
            vector_num_parts = [int(num_str) for num_str in vector_str_parts]
            vectors.append( vector_num_parts )

        return vectors

    @staticmethod
    def read_film_data(filename):
        '''
        reads film data from filename
        '''
        file = open(filename, 'r')

        film_data = []

        for line in file:

            line = line.replace("\n","")

            parts = line.split("#")

            film_data.append(parts)

        return film_data

    @staticmethod
    def write_film_data(filename,films):
        '''
        writes film data to filename
        '''
        fileContent = ""

        for idx, film in enumerate(films):

            fileContent += "{0}#{1}#{2}#{3}#{4}#{5}".format(film[0],film[1],film[2],film[3], film[4],film[5])

            if idx < (len(films)-1):
                fileContent += "\n"

        fileContent += "\n"
        # write the string to a file
        with open(filename, "w") as text_file:
            text_file.write("{0}".format(fileContent))


    @staticmethod
    def write_vocab(filename, vocabulary):
        '''
        writes vocabularies to filename
        '''
        fileContent = ""

        for idx, term in enumerate(vocabulary):

            fileContent += "{0} {1}".format(term,vocabulary[term])

            if idx < (len(vocabulary.keys())-1):
                fileContent += "\n"

        fileContent += "\n"
        # write the string to a file
        with open(filename, "w") as text_file:
            text_file.write("{0}".format(fileContent))

    @staticmethod
    def write_vocab_vectors(filename, vectors):
        '''
        writes vocabulary vectors to filename
        '''
        fileContent = ""

        for idx, vector in enumerate(vectors):
            #vector = [2160,300,209,299]
            vector_of_str = [str(wd) for wd in vector]
            vector_str = ",".join(vector_of_str)
            fileContent += "{0}".format(vector_str)

            if idx < (len(vectors)-1):
                fileContent += "\n"

        fileContent += "\n"
        # write the string to a file
        with open(filename, "w") as text_file:
            text_file.write("{0}".format(fileContent))
