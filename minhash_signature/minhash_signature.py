# =============================================================================
#                 Generate MinHash Signatures
# =============================================================================
import random
import time
import sys
from shingling.shingling import shingling
from utils.hashFamily import hashFamily

# K-shingles
K = 10

def MinHash(collection, ByteHashFamily, N, ByteHashFamiliShingles, isHash, debug=None):
    print "Shingling articles..."
    t0 = time.time()

    shingles_collection = getCollectionShingles(collection, ByteHashFamiliShingles, isHash)
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)


    print '\nGenerating random hash functions...'
    n = N
    hash_funcs = random_hash(n, ByteHashFamily)

    print '\nGenerating MinHash signatures for all documents...'
    signatures = {}
    t0 = time.time()

    for docID in range(0, len(collection)):
        # Get the shingle set of shingles for this document.
        shingles = shingles_collection[docID]

        # The resulting minhash signature for THIS document.
        signature = []

        # For each of the random hash functions..
        for h in hash_funcs:
            # For each shingle in the document...
            # set minHashCode to inf
            minHashCode = float('inf')
            for shingle in shingles:
                hashcode = h(str(shingle))
                if hashcode < minHashCode:
                    minHashCode = hashcode

            signature.append(minHashCode)
        signatures[docID] = signature

    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)
    print "\nGenerating MinHash signatures took %.2fsec" % elapsed

    # print 'Esempio di una signatura del documento 0: ' + str(signatures[signatures.keys()[0]])
    return signatures


# returns a list of hash function pointer
def random_hash(num_hashes, ByteHashFamily, debug=None):
    # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1)
    hash_funcs = []
    random_numb = []
    for j in range(0, num_hashes):
        if debug:
            print ": " + str(j)
        # load hash functions
        i = random.randint(1, sys.maxint - 1)
        random_numb.append(i)
        hash_funcs.append(hashFamily(i, ByteHashFamily))
    # print random_numb
    return hash_funcs

def getCollectionShingles(collection, ByteHashFamiliShingles, isHash, debug=None):
    shingles_collection = {}
    totalShingles = 0
    if debug:
        print '#number of documents: ' + str(len(collection.keys()))
    for key in collection.keys():
        s = shingling(collection[key], K, ByteHashFamiliShingles, isHash)
        totalShingles = totalShingles + len(s)

        shingles_collection[key] = s
    print '\nAverage shingles per doc: %.2f' % (totalShingles / len(collection))

    return shingles_collection
