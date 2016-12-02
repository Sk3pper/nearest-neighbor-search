# Implement a class that implements the locally sensitive hashing (LSH) technique, so that,
# given a collection of minwise hash signatures of a set of documents,
# it finds the all the documents pairs that are near each other.
import time

from minhash_signature.minhash_signature import random_hash
from utils.TriangleIndex import getTriangleIndex
import math
import math

# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.

# https://www.wolframalpha.com/input/?i=b*r%3D10,+(1%2Fb)%5E(1%2Fr)%3E0.8
from utils.hashFamily import hashFamily
from utils.log_calculate import log_dict

B = 2
R = 5

def compareMinHash_improve(signatures, debug=None):
    numDocs = len(signatures)
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # i need a hash function
    h = hashFamily(int(986))

    # Initialize empty list to store the similarity values.
    # 'estJSim' will be for the estimated Jaccard Similarities found by comparing the MinHash signatures.
    estJSim = [0 for x in range(numElems)]
    Intersection_matrix = [0 for x in range(numElems)]

    # qui abbiamo salvato per ogni documento le vaire bande, che ci costruiamo mentre facciamo facciamo
    # girare perche' puo' accadere casi in cui non e' necessario calcolarsi tutte le bande per ogni documento
    # doc_i = b1 | b2 | b3
    # dove bi = r1 | r2 | r3 | r4 | r5
    # e ri = una signature delle minhash

    band_signatures = {}
    possibile_pairs_dataset = {}
    possible_pairs = []
    # calculate the possible pairs
    print '\nCalculate the possible pairs...'
    # Time this step.
    t0 = time.time()

    for i in range(0, numDocs):
        docID1 = i

        # Print progress every 100 documents.
        if (docID1 % 100) == 0:
            print "  (" + str(docID1) + " / " + str(numDocs) + ")"
        signature1 = signatures[docID1]

        # The method get() returns a value for the given key. If key is not available then returns default value None.
        bs1 = band_signatures.get(docID1)
        if bs1 == None:
            bs1 = []
        # For each of the other test documents...
        for j in range(i + 1, numDocs):
            docID2 = j
            # Get the MinHash signature for document j.
            signature2 = signatures[docID2]

            # we go in Band in Band, here we compare band a band for
            # doc1 and doc2

            bs2 = band_signatures.get(docID2)
            if bs2 == None:
                bs2 = []

            for k in range(0, B):
                bs1_length = len(bs1)

                # se non abbiamo quella bada dobbiamo calcolarla
                if bs1_length <= k:

                    # print 'signature1: ' + str(signature1)
                    # we have to calculate this band
                    band1 = ''
                    for y in range(0, R):
                        # k give us the base of the band
                        # print 'k: ', k
                        # print 'y: ', y
                        band1 += str(signature1[(k + 1) * y])
                    # print band1
                    bs1.append(h(band1))
                    # print 'bs1 ' + str(bs1)

                bs2_length = len(bs2)
                if bs2_length <= k:

                    # print 'signature2: '+ str(signature2)
                    # we have to calculate this band
                    band2 = ''
                    for y in range(0, R):
                        # k give us the base of the band
                        band2 += str(signature2[(k + 1) * y])

                    #print band2
                    bs2.append(h(band2))
                    # print 'bs2: ' + str(bs2)
                # after this line we have the two band and we have to compare
                # if they are equal we can skip to the next pair
                if band1 == band2:
                    print 'found pair..'
                    # add for the deep compare
                    # save the info
                    if possibile_pairs_dataset.get(docID1) == None:
                        possibile_pairs_dataset[docID1] = signature1
                    if possibile_pairs_dataset.get(docID2) == None:
                        possibile_pairs_dataset[docID2] = signature2

                    # save the key of the pair
                    possible_pairs.append(docID1)
                    possible_pairs.append(docID2)

    elapsed = (time.time() - t0)
    print "\nCalculate the possible pairs... took %.2fsec" % elapsed
     # 3. Compare all MinHash signatures to one another.
    print '\nComparing the possible pairs found...'

    numPossiblePair = len(possible_pairs)/2
    # Time this step.
    t0 = time.time()

    # siccome usiamo come docID degli interi sulla ns collection possiamo fare in questo modo per velocizzare:
    # For each of the test documents...

    # Count the number of positions in the minhash signature which are equal.
    n = log_dict(signatures)

    for i in range(0, numPossiblePair):
        # Get the MinHash signature for document i.
        docID1 = possible_pairs[i]
        docID2 = possible_pairs[i+1]
        i = docID1
        j = docID2

        signature1 = possibile_pairs_dataset[docID1]
        signature2 = possibile_pairs_dataset[docID2]
        count = 0
        for k in range(0, n):

            # print signature1[k]
            # print signature2[k]
            count = count + (signature1[k] == signature2[k])
            # print 'count: ', count

        print "  %5s --> %5s   %.2f" % (docID1, docID2, (float(count) / float(n)))

        # Record the percentage of positions which matched.
        coord = getTriangleIndex(i, j, numDocs)
        estJSim[coord] = (float(count) / float(n))
        Intersection_matrix[coord] = float(count)

    elapsed = (time.time() - t0)
    print "\nComparing MinHash signatures took %.2fsec" % elapsed

    result = []
    result.append(estJSim)
    result.append(Intersection_matrix)
    return result
