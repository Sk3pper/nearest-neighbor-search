
import os
from locally_sensitive_hashing.lsh_improve import compareMinHash_improve
from minhash_signature.minhash_signature import MinHash
from nearest_neighbors.nearest_neighbors import J_nearest_neighbors
from shingling.shingling import shingling
from utils.TriangleIndex import getTriangleIndex
import json
from utils.extract_info import extract_string_recipe
from utils.log_calculate import log_dict

THRESHOLD = 0.8
JRESULTS = 'j_results.txt'
JRESULTS_HASH = 'j_results_hash.txt'
dir = '/Users/andrea/Documents/workspace/nearest-neighbor-search/data/'


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

# shingling(document, k, ByteHashFamiliShingles, isSet=None, isHash=None, print_=None):
shingles= shingling(collection[2343],10, 10,None,None)
print shingles


for i in range(0,10):
    minSHi = shingles[0]
    print i
    for shingle in shingles:
        if shingle < minSHi:
            minSHi = shingle

    print minSHi
    shingle = shingles.remove(minSHi)
