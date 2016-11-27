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


# oss: il punto 1 e' fatto nel pacchetto shinghing, dobbiamo solo estenderlo a tutti i documenti della
# collezione.
import time

from shingling.shingling import shingling
import random
from utils.hashFamily import hashFamily

# K-shingle parameter
K = 3
# Shingles are mapped to shingle IDs using the hash parametrized function given by the professor with a i-parameter equal for all
I = 1
# Number of hash functions used for the Min Hash Signature
NUMHASHES = 10
# range of random.randint(A, B)
A = 0
B = 10000

#numElems
numElems = 0


# data la collezione di documenti, per ogni documento faccio partire shingling(document, k, i, print_= None)
# NB = per collezione intendo un dizionario dove il DOC_ID e' la chiave per prendere la stringa del documento associato
# poi fa tutto shingling che legge come una stringa
# ritorna un dizionario di liste, dove ogni lista e' un documento rappresentato con le shingle
def getCollectionShingles(collection, debug=None):
    shingles_collection = {}
    if debug:
        print '#number of documents: '+ str(len(collection.keys()))
    for key in collection.keys():
        shingles_collection[key] = (shingling(collection[key], K, I))

    return shingles_collection

# data la collezione, la collezione divisa per shingles, e le random_hash
# ritorna la collezione di signature
def MinHash(collection, shingles_collection, random_hash, debug=None):
    signatures = {}
    for docID in collection.keys():
        # Get the shingle set of shingles for this document.
        shingles = shingles_collection[docID]

        # The resulting minhash signature for THIS document.
        signature = []

        # For each of the random hash functions...

        for hash in random_hash:
            i = 0
            # For each shingle in the document...
            for shingle in shingles:
                if i == 0:
                    minHashCode = hash(shingle)
                    i += 1
                else:
                    value = hash(shingle)

                if value < minHashCode and i != 0:
                    minHashCode = value

            # Add the smallest hash code value as component number 'i' of the signature.
            signature.append(minHashCode)

        signatures[docID] = signature

    return signatures

# returns a list of hash function pointer
def random_hash():
    # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_funcs = []
    for j in range(NUMHASHES):
        i = random.randint(A, B)
        # load hash functions
        hash_funcs.append(hashFamily(i))
    return hash_funcs

def compareMinHash(collection, shingles_collection, signatures, debug=None):
    # For each of the test documents...

    similitary_table = []
    for docID1 in collection.keys():
        # Get the MinHash signature for document i.
        signature1 = signatures[docID1]

        # For each of the other test documents...
        for docID2 in collection.keys():

            if docID1 != docID2:
                # Get the MinHash signature for document j.
                signature2 = signatures[docID2]

                count = 0
                # Count the number of positions in the minhash signature which are equal.
                for k in range(0, NUMHASHES):
                    count = count + (signature1[k] == signature2[k])

                # Record the percentage of positions which matched.
                # potrei farmi un oggetto con doc1,doc2,percentuale
                sim_entry = SimiliratyEntry(str(docID1), str(docID2), (count / NUMHASHES))

        similitary_table.append(sim_entry)

    return similitary_table

class SimiliratyEntry:
    def __init__(self, docID1, docID2, percentage_matched):
        self.docID1 = docID1
        self.docID2 = docID2
        self.percentage_matched = percentage_matched

    def str(self):
       return  "  %5s --> %5s   %.2f" % (str(self.docID1), str(self.docID2), str(self.percentage_matched))

if __name__ == '__main__':
    # load collection
    collection = {}
    numDocs = len(collection)
    numElems = int(numDocs * (numDocs - 1) / 2)

    # 1. Convert each test file into a set of shingles hashed.
    # oss: la key per accedere ad shingles_collection o collection e' la STESSA!!!
    print "Shingling articles..."
    t0 = time.time()
    shingles_collection = getCollectionShingles(collection)
    # Report how long shingling took.
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    # 2. Calculate the MinHash signature for each document.
    # Time this step.
    t0 = time.time()
    print '\nGenerating random hash functions...'
    hash_funcs = random_hash()
    print '\nGenerating MinHash signatures for all documents...'
    signatures = MinHash(collection, shingles_collection, hash_funcs)
    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nGenerating MinHash signatures took %.2fsec" % elapsed

    # 3. Compare all MinHash signatures to one another.
    print '\nComparing all signatures...'
    # Time this step.
    t0 = time.time()
    ret = compareMinHash(collection, shingles_collection, signatures)
    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nComparing MinHash signatures took %.2fsec" % elapsed


    print ret


