# =============================================================================
#                   Display Similar Document Pairs
# ============================================================================

import time
import os
from locally_sensitive_hashing.lsh import compareMinHash
from locally_sensitive_hashing.lsh_improve import compareMinHash_improve
from minhash_signature.minhash_signature import MinHash
from nearest_neighbors.nearest_neighbors import J_nearest_neighbors
from utils import unicode_ascii_decoder
from utils.TriangleIndex import getTriangleIndex
import json

from utils.extract_info import extract_string_recipe
from utils.write_file import put_into_file

THRESHOLD = 0.7


def compare_methods(collection, debug=None):
    numDocs = len(collection)
    if debug:
        print "numDocs: " + str(numDocs)

    print "\nCalculating estJSim..."
    estJSimResult = compareMinHash_improve(MinHash(collection, True))
    estJSim = estJSimResult[0]
    estJSimsize_inter = estJSimResult[1]
    # print estJSim

    # calculate two methods
    print "\nCalculating JSim..."
    # JResult = J_nearest_neighbors(collection, True)
    JSim = [0 for x in range(int(len(collection) * (len(collection) - 1) / 2))] # JResult[0]
    Jsize_inter = [0 for x in range(int(len(collection) * (len(collection) - 1) / 2))] # JResult[1]
    # [0 for x in range(int(len(collection) * (len(collection) - 1) / 2))]
    # print JSim



    print 'Write into file...'
    put_into_file(JSim, 'JSim.txt')
    put_into_file(estJSim, 'estJSim.txt')

    print "\nList of Document Pairs with J(d1,d2) more than", THRESHOLD
    print "Values shown are the estimated Jaccard similarity and the actual"
    print "Jaccard similarity.\n"
    print "                   Est. J   Act. J"

    # For each of the document pairs...
    count = 0
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            # Retrieve the estimated similarity value for this pair.
            coordinate = getTriangleIndex(i, j, numDocs)
            estJ = estJSim[coordinate]
            J = JSim[coordinate]
            Jsi = Jsize_inter[coordinate]
            estJSimsi = estJSimsize_inter[coordinate]
            # If the similarity is above the threshold...

            if estJ >= THRESHOLD:
                # Print out the match and similarity values with pretty spacing.
                print "  %5s --> %5s   %.2f (%.2f)     %.2f (%.2f)" % (i, j, estJ,estJSimsi, J, Jsi)
                count = count + 1

    print 'document pairs founded: ' + str(count)


if __name__ == '__main__':
    # OSS: la collection deve essere nel formato collection[docID] = documento
    #      - dove docID e' l'ID del documento che nel caso delle nostre ricette e' un numero e manteniamo
    #        il mapping con il nome vero e proprio. L'id come numero ci aiuta dopo quando facciamo
    #        la matrice dove ci salviamo i risultati
    #      - documento: e' una stringa contenente il contenuto del documento

    # You can run this code for different portions of the dataset.
    # It ships with data set sizes 100, 1000, 2500, and 10000.

    dataFile = "recipes.json"
    dir = '/Users/andrea/Documents/workspace/nearest-neighbor-search/data/'

    print 'Load JSON...'
    with open(os.path.join(os.pardir, dir, dataFile)) as json_data:
        recipes = json.load(json_data)

    print "Processing JSON..."

    tot = len(recipes)
    documents = {}
    i = 0

    collection = {}
    for recipe in recipes:
        collection[i] = extract_string_recipe(recipe)
        i += 1

    print 'read '+str(len(collection))+' recipes from .json'
    min_coll = {}

    for i in range(0, 1000):
        min_coll[i] = collection[i]
        # print min_coll[i]
    print 'Compare two methods...'
    compare_methods(min_coll, True)

    # compare_methods(collection, True)


























'''numDocs = 1000
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

compare_methods(collection, True)'''