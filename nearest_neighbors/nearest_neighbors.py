# =============================================================================
#                 Calculate Jaccard Similarities
# =============================================================================
# In this section, we will directly calculate the Jaccard similarities by
# comparing the sets. This is included here to show how much slower it is than
# the MinHash approach.

# Calculating the Jaccard similarities gets really slow for large numbers
# of documents.
import time

from minhash_signature.minhash_signature import getCollectionShingles
from utils.TriangleIndex import getTriangleIndex


def J_nearest_neighbors(collection, debug=None):

    numDocs = len(collection)
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # Initialize empty list to store the similarity values.
    # 'JSim' will be for the actual Jaccard Similarity values.
    JSim = [0 for x in range(numElems)]

    print "Shingling articles..."
    t0 = time.time()
    shingles_collection = getCollectionShingles(collection)
    # Report how long shingling took.
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    print "\nCalculating Jaccard Similarities..."

    # Time the calculation.
    t0 = time.time()

    # For every document pair...
    for i in range(0, numDocs):

        # Print progress every 100 documents.
        if debug:
            if (i % 100) == 0:
              print "  (" + str(i) + " / " + str(numDocs) + ")"

        # Retrieve the set of shingles for document i.
        s1 = set(shingles_collection[i])

        for j in range(i + 1, numDocs):
            # Retrieve the set of shingles for document j.
            s2 = set(shingles_collection[j])

            # Calculate and store the actual Jaccard similarity.
            JSim[getTriangleIndex(i, j, numDocs)] = (float(len(s1.intersection(s2))) / float(len(s1.union(s2))))

            '''if debug:
                if len(s1.intersection(s2)) / float(len(s1.union(s2))) > 0:
                    print 'len(s1.intersection(s2)): '+str(len(s1.intersection(s2)))+' len(s1.union(s2)): '+str(len(s1.union(s2)))+\
                      ' JSim: '+str((len(s1.intersection(s2)) / len(s1.union(s2))))

                    print str((len(s1.intersection(s2)) / float(len(s1.union(s2)))))'''
            # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)

    print "\nCalculating all Jaccard Similarities took %.2fsec" % elapsed

    return JSim