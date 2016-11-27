# =============================================================================
#                   Display Similar Document Pairs
# ============================================================================

import time
import os
from locally_sensitive_hashing.lsh import compareMinHash
from minhash_signature.minhash_signature import MinHash
from nearest_neighbors.nearest_neighbors import J_nearest_neighbors
from utils.TriangleIndex import getTriangleIndex

THRESHOLD = 0.8

def compare_methods(collection, debug=None):

    numDocs = len(collection)
    if debug:
        print "numDocs: " + str(numDocs)

    # calculate two methods

    print "\nCalculating estJSim..."
    estJSim = compareMinHash(MinHash(collection, True))

    print "\nCalculating JSim..."
    JSim = J_nearest_neighbors(collection, True)

    print "\nList of Document Pairs with J(d1,d2) more than", THRESHOLD
    print "Values shown are the estimated Jaccard similarity and the actual"
    print "Jaccard similarity.\n"
    print "                   Est. J   Act. J"

    # For each of the document pairs...
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            # Retrieve the estimated similarity value for this pair.
            estJ = estJSim[getTriangleIndex(i, j, numDocs)]
            J = JSim[getTriangleIndex(i, j, numDocs)]
            # If the similarity is above the threshold...

            if estJ > THRESHOLD:
                # Print out the match and similarity values with pretty spacing.
                print "  %5s --> %5s   %.2f     %.2f" % (i, j, estJ, J)


if __name__ == '__main__':
    # OSS: la collection deve essere nel formato collection[docID] = documento
    #      - dove docID e' l'ID del documento che nel caso delle nostre ricette e' un numero e manteniamo
    #        il mapping con il nome vero e proprio. L'id come numero ci aiuta dopo quando facciamo
    #        la matrice dove ci salviamo i risultati
    #      - documento: e' una stringa contenente il contenuto del documento

    # You can run this code for different portions of the dataset.
    # It ships with data set sizes 100, 1000, 2500, and 10000.
    numDocs = 1000
    dataFile = "/data/articles_" + str(numDocs) + ".train"
    dir = '/Users/andrea/Documents/workspace/nearest-neighbor-search/'
    # Open the data file.
    f = open(dir+dataFile, "rU")

    collection = {}

    for i in range(0, numDocs):

        # Read all of the words (they are all on one line) and split them by white
        # space.
        doc = f.readline()

        # Retrieve the article ID, which is the first word on the line.
        docID = i
        collection[docID] = doc
       # print docID,doc

    #print collection
    # Close the data file.
    f.close()

    compare_methods(collection, True)
