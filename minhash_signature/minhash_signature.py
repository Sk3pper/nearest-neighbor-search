# =============================================================================
#                 Generate MinHash Signatures
# =============================================================================
# Implement a class, that given a collection of sets of objects (e.g., strings, or numbers),
# creates a minwise hashing based signature for each set.
# HO CAPITO: qui vuole che usiamo il punto 1!! Cosi data la collection creiamo le shingles per ogni document e poi la
# signaturee
import random
import time

import sys

from shingling.shingling import shingling
from utils.hashFamily import hashFamily
from utils.log_calculate import log_dict

# K-shingles
K = 10


# number of random hash functions apply to perform signature
# data la collezione, la collezione divisa per shingles, e le random_hash
# ritorna la collezione di signature
def MinHash(collection, ByteHashFamily, N, ByteHashFamiliShingles, isHash, debug=None):
    print "Shingling articles..."
    t0 = time.time()

    shingles_collection = getCollectionShingles(collection, ByteHashFamiliShingles, isHash)
    print 'Esempio di shingling del documento 0: ' + str(shingles_collection[shingles_collection.keys()[0]])
    # Report how long shingling took.
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    t0 = time.time()
    print '\nGenerating random hash functions...'
    n = N  # log_dict(collection)
    hash_funcs = random_hash(n, ByteHashFamily)

    print '\nGenerating MinHash signatures for all documents...'
    signatures = {}

    # oss: collection ed shingles_collection ed signatures con la stessa chiave si riferisce allo stesso oggetto
    for docID in range(0, len(collection)):
        # Print progress every 100 documents.
        if (docID % 2000) == 0:
            print "  (" + str(docID) + " / " + str(len(collection)) + ")"
        # Get the shingle set of shingles for this document.
        shingles = shingles_collection[docID]

        # The resulting minhash signature for THIS document.
        signature = []
        s = []
        '''
        minHashCode = [float('inf') for j in range(N)]
        for shingle in shingles:

            i = 0
            for h in hash_funcs:
                hashcode = h(str(shingle))
                if hashcode < minHashCode[i]:
                    minHashCode[i] = hashcode
                i += 1

        signatures[docID] = minHashCode
        # print signatures[docID]
        if docID == 2343:
            print signatures[docID]
        '''

        # For each of the random hash functions..
        for h in hash_funcs:
            # For each shingle in the document...
            # set minHashCode to inf
            minHashCode = float('inf')
            for shingle in shingles[]:
                hashcode = h(str(shingle))
                if hashcode < minHashCode:
                    if (docID == 2343 or docID == 3860) or (docID == 6507 or docID == 6508) or (docID == 8289 or docID == 8290):
                        shi = shingle
                    minHashCode = hashcode

            signature.append(minHashCode)

            if (docID == 2343 or docID == 3860) or (docID == 6507 or docID == 6508) or (docID == 8289 or docID == 8290):
                s.append(shi)
        signatures[docID] = signature

        if (docID == 2343 or docID == 3860) or (docID == 6507 or docID == 6508) or (
                    docID == 8289 or docID == 8290):
            print 'docID:', docID
            print 'shingles: ' + str(s)
            print 'signatures: ' + str(signature)



    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nGenerating MinHash signatures took %.2fsec" % elapsed

    print 'Esempio di una signatura del documento 0: ' + str(signatures[signatures.keys()[0]])
    return signatures


# returns a list of hash function pointer
def random_hash(num_hashes, ByteHashFamily, debug=None):
    # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_funcs = []
    random_numb = []
    for j in range(0, num_hashes):
        if debug:
            print ": " + str(j)
        # print "j: " + str(j)
        # load hash functions
        random_numb.append(random.randint(1, sys.maxint - 1))
        hash_funcs.append(hashFamily(i, ByteHashFamily))
    print random_numb
    return hash_funcs


# data la collezione di documenti, per ogni documento faccio partire shingling(document, k, i, print_= None)
# NB = per collezione intendo un dizionario dove il DOC_ID e' la chiave per prendere la stringa del documento associato
# poi fa tutto shingling che legge come una stringa
# ritorna un dizionario di liste, dove ogni lista e' un documento rappresentato con le shingle
def getCollectionShingles(collection, ByteHashFamiliShingles, isHash, isSet=None, debug=None):
    print 'K = ' + str(K)
    shingles_collection = {}
    totalShingles = 0
    if debug:
        print '#number of documents: ' + str(len(collection.keys()))
    for key in collection.keys():
        s = shingling(collection[key], K, ByteHashFamiliShingles, isSet, isHash)
        totalShingles = totalShingles + len(s)

        shingles_collection[key] = s
    print '\nAverage shingles per doc: %.2f' % (totalShingles / len(collection))

    return shingles_collection
