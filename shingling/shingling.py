# Implement a class that, given a document, creates its set of character shingles of some length k.
# Then represent the document as the set of the hashes of the shingles, for some hash function.
from utils.hashFamily import hashFamily

#  print_= None serve per debug purpose
def shingling(document, k, i, print_= None):

    # prima facciamo le "tegole"
    shingles = [document[i:i + k] for i in range(len(document) - k + 1)]

    if print_:
        print shingles

    # poi per ogni tegola faciamo l'hash
    hash_shingles = []

    # load hash function
    hash_fun = hashFamily(i)

    for s in shingles:
        hash_shingles.append(hash_fun(s))

    if print_:
        print hash_shingles

    return hash_shingles



if __name__ == '__main__':
    shingling("ciao come va??", 4, 8)