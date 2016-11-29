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
import threading
import copy

shi = []
JSim2 = []
LOAD_TH = 100 # quanti documenti per ogni thread
n_docs = 0
threadLock = None

class myThread(threading.Thread):
    def __init__(self, threadID, start_index, end, shingles_collection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.start_index = start_index
        self.end = end
        self.shingles_collection = shingles_collection

    def run(self):
        # print "Starting " + self.name
        self.worker(self.start_index, self.end)
        # print "Exiting " + self.name


    def worker(self, start, end):
        # For every document pair...

        for i in range(start, end):
            '''
            # Print progress every 100 documents.
            if (i % 100) == 0:
                print "  (" + str(i) + " / " + str(n_docs) + ")"'''

            # Retrieve the set of shingles for document i.
            s1 = self.shingles_collection[i]
            # print 's1: ' + str(len(s1))
            # print str(start)+'-'+str(end)+'  '+str(self.threadID)+' docID: '+ str(i)

            for j in range(i + 1, n_docs):
                # Retrieve the set of shingles for document j.
                s2 = self.shingles_collection[j]
                # print 's2: ' + str(len(s1))+'\n'
                # Calculate and store the actual Jaccard similarity.
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

    threadLock = threading.Lock()

    threads = []

    for i in range(0, n_th):
        # print str(i * LOAD_TH) + '-' + str((i + 1) * LOAD_TH)
        # Create new threads
        print 'start thread',i

        #x = copy.deepcopy(y)    # crea una copia profonda di y
        th = myThread(str(i), i * LOAD_TH, (i + 1) * LOAD_TH, copy.deepcopy(shingles_collection) )
        threads.insert(i, th)

    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    # print JSim
    print "Exiting Main Thread"

    # Calculate the elapsed time (in seconds)
    elapsed = (time.time() - t0)

    print "\nCalculating all Jaccard Similarities took %.2fsec" % elapsed

    return JSim

if __name__ == '__main__':
    numDocs = 100
    n_docs = numDocs
    n_th = numDocs / LOAD_TH

    threadLock = threading.Lock()
    threads = []

    for i in range(0, n_th):
        print str(i * LOAD_TH) + '-' + str((i+1)*LOAD_TH-1)
        # Create new threads
        th = myThread(str(i), i * LOAD_TH, (i+1)*LOAD_TH-1)
        threads.insert(i, th)
        threads[i].start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print "Exiting Main Thread"

