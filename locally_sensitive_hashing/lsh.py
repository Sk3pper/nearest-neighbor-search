# Implement a class that implements the locally sensitive hashing (LSH) technique, so that,
# given a collection of minwise hash signatures of a set of documents,
# it finds the all the documents pairs that are near each other.
import time

from utils.TriangleIndex import getTriangleIndex


# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.
NUMHASHES = 10

def compareMinHash(signatures, debug=None):
    numDocs = len(signatures)
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # Initialize empty list to store the similarity values.
    # 'estJSim' will be for the estimated Jaccard Similarities found by comparing the MinHash signatures.
    estJSim = [0 for x in range(numElems)]

    # 3. Compare all MinHash signatures to one another.
    print '\nComparing all signatures...'
    # Time this step.
    t0 = time.time()

    # siccome usiamo come docID degli interi sulla ns collection possiamo fare in questo modo per velocizzare:
    # For each of the test documents...
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
            # Count the number of positions in the minhash signature which are equal.
            for k in range(0, NUMHASHES):
                count = count + (signature1[k] == signature2[k])

            # Record the percentage of positions which matched.
            estJSim[getTriangleIndex(i, j, numDocs)] = (float(count) / float(NUMHASHES))

    elapsed = (time.time() - t0)
    print "\nComparing MinHash signatures took %.2fsec" % elapsed

    return estJSim
