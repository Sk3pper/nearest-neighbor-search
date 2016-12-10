# =============================================================================
#                   Display Similar Document Pairs
# ============================================================================

import os
from locally_sensitive_hashing.lsh_improve import compareMinHash_improve
from minhash_signature.minhash_signature import MinHash
from nearest_neighbors.nearest_neighbors import J_nearest_neighbors
from utils.TriangleIndex import getTriangleIndex
import json
from utils.extract_info import extract_string_recipe

THRESHOLD = 0.8
JRESULTS = 'j_results.txt'
JRESULTS_HASH = 'j_results_hash.txt'
dir = '/Users/andrea/Documents/workspace/nearest-neighbor-search/data/'


def read_list(name, numb):
    JSim = [0 for x in range(int(numb) * (numb - 1) / 2)]

    with open(os.path.join(os.pardir, dir, name)) as jres:
        in_file = jres.read()

    for line in in_file.split('\n')[:-1]:

        ids = line.split("\t")[0]
        j = line.split("\t")[1]
        if int(ids.split('-->')[0]) < numb and int(ids.split('-->')[1]) < numb:
            JSim[getTriangleIndex(int(ids.split('-->')[0]), int(ids.split('-->')[1]), numb)] = float(j)
    return JSim

def put_into_file(content, numDocs, name):
    # save into the file
    out_file = open(dir+name, "w")
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            coordinate = getTriangleIndex(i, j, numDocs)
            J = content[coordinate]
            if J >= THRESHOLD:
                s = str(i)+'-->'+str(j)+'\t'+str(J)
                out_file.write(s + '\n')
    out_file.close()

def compare_methods(collection, ByteHashFamily, B, R, N, ByteHashFamiliShingles, isHash, debug=None):
    print "TEST with: "
    print 'ByteHashFamily: '+ str(ByteHashFamily)+' B: '+str(B)+' R: '+str(R)+ ' N: '+str(N)\
        +' ByteHashFamiliShingles: '+str(ByteHashFamiliShingles)+' isHash: '+str(isHash)
    numDocs = len(collection)

    print "\nCalculating JSim..."
    if isHash:
        if os.path.isfile(dir + JRESULTS_HASH):
            # read results from file
            print 'file {} exists'.format(JRESULTS_HASH)
            JSim = read_list(JRESULTS_HASH, len(collection))
        else:
            print 'file does not exist...'
            # calculate Jaccard similiraty
            JSim = J_nearest_neighbors(collection, ByteHashFamiliShingles, isHash, True)
            print 'Write into file...'
            put_into_file(JSim, numDocs, JRESULTS_HASH)
    else:
        if os.path.isfile(dir + JRESULTS):
            # read results from file
            print 'file {} exists'.format(JRESULTS)
            JSim = read_list(JRESULTS, len(collection))
        else:
            print 'file does not exist...'
            # calculate Jaccard similiraty
            JSim = J_nearest_neighbors(collection, ByteHashFamiliShingles, isHash, True)
            print 'Write into file...'
            put_into_file(JSim, numDocs, JRESULTS)



    print "\nCalculating estJSim..."
    # calculate min hash for each documents
    signatures = MinHash(collection, ByteHashFamily, N, ByteHashFamiliShingles, isHash, True)
    # calculate lsh
    estJSim = compareMinHash_improve(signatures, ByteHashFamily, B, R, N, True)

    print "\nList of Document Pairs with J(d1,d2) more than", THRESHOLD
    print "Values shown are the estimated Jaccard similarity and the actual"
    print "Jaccard similarity.\n"

    # For each of the document pairs...
    count = 0
    jacc_pairs = []
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            # Retrieve the estimated similarity value for this pair.
            coordinate = getTriangleIndex(i, j, numDocs)
            J = JSim[coordinate]

            if J >= THRESHOLD:
                # Print out the match and similarity values with pretty spacing.
                print "%5s --> %5s   %.2f" % (i, j, J)
                jacc_pairs.append((i, j))
                count = count + 1
                # For each of the document pairs...
    print '[JACCARD] document pairs founded: ' + str(count)
    print '###########################################\n########################################\n'

    estj_pairs = []
    count = 0
    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            # Retrieve the estimated similarity value for this pair.
            coordinate = getTriangleIndex(i, j, numDocs)
            estJ = estJSim[coordinate]
            # If the similarity is above the threshold...

            if estJ >= THRESHOLD:
                # Print out the match and similarity values with pretty spacing.
                print "%5s --> %5s   %.2f" % (i, j, estJ)
                estj_pairs.append((i, j))
                count = count + 1
    print '[ESTIMATION] document pairs founded: ' + str(count)

    print '\n ###########################################\n########################################\n' \
          'Calcualte the intersection..'
    set_pairs = set(jacc_pairs).intersection(set(estj_pairs))

    count = 0
    print "     doc1    doc2    J   estJ"
    for (doc1, doc2) in set_pairs:
            # Retrieve the estimated similarity value for this pair.
            jvalue = JSim[getTriangleIndex(doc1, doc2, numDocs)]
            estjvalue= estJSim[getTriangleIndex(doc1, doc2, numDocs)]
            print "%5s --> %5s   %.2f   %.2f" % (doc1, doc2, jvalue,estjvalue)
            count = count + 1
    print '[INTERSECTION] document founded: ' + str(count)

if __name__ == '__main__':
    dataFile = "recipes.json"

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

    print 'read ' + str(len(collection)) + ' recipes from .json'
    debug = False

    # b,r >> T
    # NO HASH SHINGLE
    print '##############################################################################################################################################################################'
    print 'TEST..... ', 1
    compare_methods(collection, ByteHashFamily=8, B=2, R=4, N=8, ByteHashFamiliShingles=8, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 2
    compare_methods(collection, ByteHashFamily=8, B=2, R=5, N=10, ByteHashFamiliShingles=6, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 3
    compare_methods(collection, ByteHashFamily=8, B=3, R=7, N=21, ByteHashFamiliShingles=8, isHash=False, debug=debug)
    print '##############################################################################################################################################################################'
    print 'TEST..... ', 4
    compare_methods(collection, ByteHashFamily=8, B=4, R=7, N=28, ByteHashFamiliShingles=6, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 5
    compare_methods(collection, ByteHashFamily=8, B=5, R=7, N=35, ByteHashFamiliShingles=6, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 6
    compare_methods(collection, ByteHashFamily=8, B=10, R=10, N=100, ByteHashFamiliShingles=6, isHash=False, debug=debug)

    #    with HASH SHINGLE
    print '##############################################################################################################################################################################'
    print 'TEST..... ', 7
    compare_methods(collection, ByteHashFamily=8, B=2, R=4, N=8, ByteHashFamiliShingles=8, isHash=True, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 8
    compare_methods(collection, ByteHashFamily=8, B=2, R=5, N=10, ByteHashFamiliShingles=6, isHash=True, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 9
    compare_methods(collection, ByteHashFamily=8, B=3, R=7, N=21, ByteHashFamiliShingles=6, isHash=True, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 10
    compare_methods(collection, ByteHashFamily=8, B=4, R=7, N=28, ByteHashFamiliShingles=8, isHash=True, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 11
    compare_methods(collection, ByteHashFamily=8, B=10, R=10, N=100, ByteHashFamiliShingles=6, isHash=True, debug=debug)

    # b,r << T
    print '##############################################################################################################################################################################'
    print 'TEST..... ', 12
    compare_methods(collection, ByteHashFamily=8, B=5, R=2, N=10, ByteHashFamiliShingles=8, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 13
    compare_methods(collection, ByteHashFamily=8, B=7, R=3, N=21, ByteHashFamiliShingles=6, isHash=False, debug=debug)

    print '##############################################################################################################################################################################'
    print 'TEST..... ', 14
    compare_methods(collection, ByteHashFamily=8, B=10, R=4, N=40, ByteHashFamiliShingles=6, isHash=False, debug=debug)
