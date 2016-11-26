# perform minwise hashing for each sets of the collection

# collection = collection of document (>1)
# per calcolare la minhash dobbiamo fare:

# 1. Convert each test file into a set of shingles.
#    - The shingles are formed by combining k consecutive words together.
#    - Shingles are mapped to shingle IDs using the hash parametrized function given by the professor with a
#      i-parameter equal for all

# 2. Calculate the MinHash signature for each document.
#    - The MinHash algorithm is implemented using the random hash function given by the professor. In this
#      case we have a different i for each of the ten function

# 3. Compare all MinHash signatures to one another.
#    - Compare MinHash signatures by counting the number of components in which
#      the signatures are equal. Divide the number of matching components by
#      the signature length to get a similarity value.
#    - Display pairs of documents / signatures with similarity greater than a
#      threshold.


# oss: il punto 1 è fatto nel pacchetto shinghing, dobbiamo solo estenderlo a tutti i documenti della
# collezione.
from shingling.shingling import shingling
import random
from utils.hashFamily import hashFamily

# K-shingle parameter
K = 3
# Shingles are mapped to shingle IDs using the hash parametrized function given by the professor with a i-parameter equal for all
I = 1
# Number of hash functions used for the Min Hash Signature
H = 10
# range of random.randint(A, B)
A = 0
B = 10000


# data la collezione di documenti, per ogni documento faccio partire shingling(document, k, i, print_= None)
# NB = per collezione intendo un dizionario dove il DOC_ID è la chiave per prendere la stringa del documento associato
# poi fa tutto shingling che legge come una stringa
# ritorna un dizionario di liste, dove ogni lista è un documento rappresentato con le shingle
def getCollectionShingles(collection, debug=None):
    shingles_collection = {}
    if debug:
        print '#number of documents: '+ str(len(collection.keys()))
    for key in collection.keys():
        shingles_collection[key] = (shingling(collection[key], K, I))

    return shingles_collection

def MinHash(shingles_collection, random_hash, debug=None):





# returns a list of hash function pointer
def random_hash():
    #random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_fun = []
    for j in range(H):
        i = random.randint(A, B)
        # load hash functions
        hash_fun.append(hashFamily())
    return hash_fun


if __name__ == '__main__':
    # 1. Convert each test file into a set of shingles hashed.
    collection = {}
    shingles_collection = getCollectionShingles(collection)

    # 2. Calculate the MinHash signature for each document.
    MinHash
