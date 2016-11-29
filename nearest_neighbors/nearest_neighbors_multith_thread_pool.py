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
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import copy

shi = []
JSim2 = []
LOAD_TH = 100 # quanti documenti per ogni thread
n_docs = 0
threadLock = None

def worker(index):
    # For every document pair...
    start = int(index.split('-')[0])
    end = int(index.split('-')[1])

    for i in range(start, end):
        '''
        # Print progress every 100 documents.
        if (i % 100) == 0:
            print "  (" + str(i) + " / " + str(n_docs) + ")"'''

        # Retrieve the set of shingles for document i.
        s1 = (shi[i])
        # print 's1: ' + str(len(s1))
        # print str(start)+'-'+str(end)+'  '+str(self.threadID)+' docID: '+ str(i)
        #  print 'i: ' + str(i) #+ '- j: ' + str(j)
        for j in range(i + 1, n_docs):
            # Retrieve the set of shingles for document j.
            s2 = (shi[j])
            # print 's2: ' + str(len(s1))+'\n'
            # Calculate and store the actual Jaccard similarity.
            #print 'start: '+str(i)+'- end: '+str(j)
            res = (float(len(s1.intersection(s2))) / float(len(s1.union(s2))))

            pos = getTriangleIndex(i, j, n_docs)
            # threadLock.acquire()
            JSim2[pos] = res
            # threadLock.release()


def J_nearest_neighbors(collection, debug=None):
    global n_docs
    global shi
    global JSim2
    global threadLock

    numDocs = len(collection)
    n_docs = numDocs
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # Initialize empty list to store the similarity values.
    # 'JSim' will be for the actual Jaccard Similarity values.
    JSim = [0 for x in range(numElems)]
    JSim2 = JSim
    print "Shingling articles..."
    t0 = time.time()
    shingles_collection = getCollectionShingles(collection)
    # Report how long shingling took.
    shi = shingles_collection
    print '\nShingling ' + str(len(collection)) + ' docs took %.2f sec.' % (time.time() - t0)

    print "\nCalculating Jaccard Similarities..."

    # Time the calculation.
    t0 = time.time()

    n_th = numDocs / LOAD_TH
    print 'n_th: '+str(n_th)
    pool = ThreadPool(n_th)  # Sets the pool size to 4
    indexs = []
    for i in range(0,n_th):
        indexs.append(str(i * LOAD_TH)+'-'+str((i + 1) * LOAD_TH))

    pool.map(worker, indexs)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
    print "Exiting Main Thread"

    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)

    print "\nCalculating all Jaccard Similarities took %.2fsec" % elapsed

    return JSim

if __name__ == '__main__':
    numDocs = 100
    n_docs = numDocs
    n_th = numDocs / LOAD_TH