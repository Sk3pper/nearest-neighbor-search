# Implement a class that, given a document, creates its set of character shingles of some length k.
# Then represent the document as the set of the hashes of the shingles, for some hash function.
import binascii

from utils.hashFamily import hashFamily


#  print_= None serve per debug purpose
def shingling(document, k, print_= None):
    # prima facciamo le "tegole"
    shingles = [document[i:i + k] for i in range(len(document) - k + 1)]

    if print_:
        print shingles

    return shingles

if __name__ == '__main__':
    print shingling("ciao come va", 4, True)