# =============================================================================
#                   Display Similar Document Pairs
# ============================================================================

import time

from locally_sensitive_hashing.lsh import compareMinHash
from minhash_signature.minhash_signature import MinHash
from nearest_neighbors.nearest_neighbors import J_nearest_neighbors
from utils.TriangleIndex import getTriangleIndex

THRESHOLD = 0.8

def compare_methods(collection, debug=None):

    numDocs = len(collection)
    if debug:
        print "numDocs: " + str(numDocs)

    # calculate
    estJSim = compareMinHash(MinHash(collection, True))
    JSim = J_nearest_neighbors(collection)

    print "\nList of Document Pairs with J(d1,d2) more than", THRESHOLD
    print "Values shown are the estimated Jaccard similarity and the actual"
    print "Jaccard similarity.\n"
    print "                   Est. J   Act. J"

    # For each of the document pairs...
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            # Retrieve the estimated similarity value for this pair.
            estJ = estJSim[getTriangleIndex(i, j)]
            J = JSim[getTriangleIndex(i, j)]
            # If the similarity is above the threshold...
            if estJ > THRESHOLD:
                # Print out the match and similarity values with pretty spacing.
                print "  %5s --> %5s   %.2f     %.2f" % (collection[i], collection[j], estJ, J)