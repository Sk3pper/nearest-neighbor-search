# =============================================================================
#                 Generate MinHash Signatures
# =============================================================================


# Implement a class, that given a collection of sets of objects (e.g., strings, or numbers),
# creates a minwise hashing based signature for each set.
# HO CAPITO: qui vuole che usiamo il punto 1!! Cosi data la collection creiamo le shingles per ogni document e poi la
# signaturee

import time
from shingling.shingling import shingling
from utils.hashFamily import hashFamily
from utils.log_calculate import log_dict

# numElems
numElems = 0
# K-shingles
K = 10


# number of random hash functions apply to perform signature
# data la collezione, la collezione divisa per shingles, e le random_hash
# ritorna la collezione di signature
def MinHash(collection, debug=None):

    print "Shingling articles..."
    t0 = time.time()
    shingles_collection = getCollectionShingles(collection)
    print 'Esempio di shingling del documento 0: ' + str(shingles_collection[shingles_collection.keys()[0]])
    # Report how long shingling took.
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    t0 = time.time()
    print '\nGenerating random hash functions...'
    n = log_dict(collection)
    hash_funcs = random_hash(n)

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

        s = ''
        sig =''
        # For each of the random hash functions...

        for h in hash_funcs:
            # For each shingle in the document...
            # set minHashCode to inf
            minHashCode = float('inf')
            for shingle in shingles:

                hashcode = h(str(shingle))
                if hashcode < minHashCode:
                    if docID == 706 or docID == 707:
                        s = shingle
                    minHashCode = hashcode
            signature.append(minHashCode)

        signatures[docID] = signature

    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nGenerating MinHash signatures took %.2fsec" % elapsed

    print 'Esempio di una signatura del documento 0: ' + str(signatures[signatures.keys()[0]])
    return signatures


# returns a list of hash function pointer
def random_hash(num_hashes, debug=None):
    # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_funcs = []
    for j in range(0, num_hashes):
        if debug:
            print ": " + str(j)
        # print "j: " + str(j)
        # load hash functions
        hash_funcs.append(hashFamily(j))
    return hash_funcs


# data la collezione di documenti, per ogni documento faccio partire shingling(document, k, i, print_= None)
# NB = per collezione intendo un dizionario dove il DOC_ID e' la chiave per prendere la stringa del documento associato
# poi fa tutto shingling che legge come una stringa
# ritorna un dizionario di liste, dove ogni lista e' un documento rappresentato con le shingle
def getCollectionShingles(collection, isSet=None, debug=None):
    print 'K = '+str(K)
    shingles_collection = {}
    totalShingles = 0
    if debug:
        print '#number of documents: ' + str(len(collection.keys()))
    for key in collection.keys():
        s = shingling(collection[key], K, isSet)
        totalShingles = totalShingles + len(s)

        shingles_collection[key] = s
    print '\nAverage shingles per doc: %.2f' % (totalShingles / len(collection))

    return shingles_collection