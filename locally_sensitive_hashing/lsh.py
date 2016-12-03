# Implement a class that implements the locally sensitive hashing (LSH) technique, so that,
# given a collection of minwise hash signatures of a set of documents,
# it finds the all the documents pairs that are near each other.
import time

from utils.TriangleIndex import getTriangleIndex
import math

# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.
from utils.log_calculate import log_dict


def compareMinHash(signatures, debug=None):
    numDocs = len(signatures)
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # Initialize empty list to store the similarity values.
    # 'estJSim' will be for the estimated Jaccard Similarities found by comparing the MinHash signatures.
    estJSim = [0 for x in range(numElems)]
    Intersection_matrix = [0 for x in range(numElems)]

    # 3. Compare all MinHash signatures to one another.
    print '\nComparing all signatures...'
    # Time this step.
    t0 = time.time()

    # siccome usiamo come docID degli interi sulla ns collection possiamo fare in questo modo per velocizzare:
    # For each of the test documents...

    # Count the number of positions in the minhash signature which are equal.
    n = log_dict(signatures)

    for i in range(0, numDocs):
        # Get the MinHash signature for document i.
        docID1 = i
        signature1 = signatures[docID1]

        # For each of the other test documents...
        for j in range(i + 1, numDocs):
            docID2 = j
            if debug:
                print "now we are comparing: " + str(docID1) + " with " + str(docID2)

            # Get the MinHash signature for document j.
            signature2 = signatures[docID2]

            count = 0

            for k in range(0, n):
                count = count + (signature1[k] == signature2[k])

            # Record the percentage of positions which matched.
            coord = getTriangleIndex(i, j, numDocs)
            estJSim[coord] = (float(count) / float(n))
            Intersection_matrix[coord] = float(count)

            # if (float(count) / float(NUMHASHES)) > 0:
                # print str(float(count) / float(NUMHASHES))
                # print str(float(count) / float(NUMHASHES))

    elapsed = (time.time() - t0)
    print "\nComparing MinHash signatures took %.2fsec" % elapsed

    result = []
    result.append(estJSim)
    result.append(Intersection_matrix)
    return result
