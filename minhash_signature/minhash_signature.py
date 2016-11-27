# =============================================================================
#                 Generate MinHash Signatures
# =============================================================================


# Implement a class, that given a collection of sets of objects (e.g., strings, or numbers),
# creates a minwise hashing based signature for each set.
# HO CAPITO: qui vuole che usiamo il punto 1!! Cosi data la collection creiamo le shingles per ogni document e poi la
# signaturee

# Number of hash functions used for the Min Hash Signature
import random

import time

from shingling.shingling import shingling
from utils.hashFamily import hashFamily

# range of random.randint(A, B)
A = 0
B = 10000

# numElems
numElems = 0

# K-shingles
K = 10
I = 2

# number of random hash functions apply to perform signature
NUMHASHES = 10

# data la collezione, la collezione divisa per shingles, e le random_hash
# ritorna la collezione di signature
def MinHash(collection, debug=None):

    print "Shingling articles..."
    t0 = time.time()
    shingles_collection = getCollectionShingles(collection)
    # Report how long shingling took.
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    t0 = time.time()
    print '\nGenerating random hash functions...'
    hash_funcs = random_hash()

    print '\nGenerating MinHash signatures for all documents...'
    signatures = {}

    # oss: collection ed shingles_collection ed signatures con la stessa chiave si riferisce allo stesso oggetto
    for docID in collection.keys():
        # Print progress every 100 documents.
        if (docID % 100) == 0:
            print "  (" + str(docID) + " / " + str(len(collection)) + ")"
        # Get the shingle set of shingles for this document.
        shingles = shingles_collection[docID]

        # The resulting minhash signature for THIS document.
        signature = []

        # For each of the random hash functions...

        for hash in hash_funcs:
            i = 0
            # For each shingle in the document...
            for shingle in shingles:
                if i == 0:
                    minHashCode = hash(str(shingle))
                    value = minHashCode
                    i += 1
                else:
                    value = hash(str(shingle))

                if value < minHashCode and i != 0:
                    minHashCode = value

            # Add the smallest hash code value as component number 'i' of the signature.
            signature.append(minHashCode)

        signatures[docID] = signature

    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nGenerating MinHash signatures took %.2fsec" % elapsed

    return signatures


# returns a list of hash function pointer
def random_hash(debug=None):
    # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_funcs = []
    for j in range(NUMHASHES):
        i = random.randint(A, B)
        if debug:
            print "i: " + str(i)
        # load hash functions
        hash_funcs.append(hashFamily(i))
    return hash_funcs


# data la collezione di documenti, per ogni documento faccio partire shingling(document, k, i, print_= None)
# NB = per collezione intendo un dizionario dove il DOC_ID e' la chiave per prendere la stringa del documento associato
# poi fa tutto shingling che legge come una stringa
# ritorna un dizionario di liste, dove ogni lista e' un documento rappresentato con le shingle
def getCollectionShingles(collection, debug=None):
    shingles_collection = {}
    totalShingles = 0
    if debug:
        print '#number of documents: '+ str(len(collection.keys()))
    for key in collection.keys():
        s = shingling(collection[key], K, I)
        totalShingles = totalShingles + len(s)

        shingles_collection[key] = s
    print '\nAverage shingles per doc: %.2f' % (totalShingles / len(collection))

    return shingles_collection