# Implement a class that implements the locally sensitive hashing (LSH) technique, so that,
# given a collection of minwise hash signatures of a set of documents,
# it finds the all the documents pairs that are near each other.
import time
from utils.TriangleIndex import getTriangleIndex
from utils.hashFamily import hashFamily

# https://www.wolframalpha.com/input/?i=b*r%3D10,+(1%2Fb)%5E(1%2Fr)%3E0.8

def compareMinHash_improve(signatures, ByteHashFamily, B, R, N, debug=None):
    numDocs = len(signatures)

    print 'B: ', B
    print 'R: ', R
    if debug:
        print "numDocs: " + str(numDocs)
    # Calculate the number of elements needed in our triangle matrix
    numElems = int(numDocs * (numDocs - 1) / 2)

    # i need a hash function
    h = hashFamily(0, ByteHashFamily)

    # Initialize empty list to store the similarity values.
    # 'estJSim' will be for the estimated Jaccard Similarities found by comparing the MinHash signatures.
    estJSim = [0 for x in range(numElems)]

    # qui abbiamo salvato per ogni documento le vaire bande, che ci costruiamo mentre facciamo facciamo
    # girare perche' puo' accadere casi in cui non e' necessario calcolarsi tutte le bande per ogni documento
    # doc_i = b1 | b2 | b3
    # dove bi = r1 | r2 | r3 | r4 | r5
    # e ri = una signature delle minhash

    band_signatures = {}
    possibile_pairs_dataset = {}
    possible_pairs = []
    # calculate the possible pairs
    print '\nCalculate the possible pairs...'
    # Time this step.
    t0 = time.time()

    for i in range(0, numDocs):
        docID1 = i

        # Print progress every 100 documents.
        if (docID1 % 1000) == 0:
            print "  (" + str(docID1) + " / " + str(numDocs) + ")"
        signature1 = signatures[docID1]

        # The method get() returns a value for the given key. If key is not available then returns default value None.
        bs1 = band_signatures.get(docID1)
        if bs1 == None:
            bs1 = []

        # For each of the other test documents...
        for j in range(i + 1, numDocs):
            docID2 = j
            # Get the MinHash signature for document j.
            signature2 = signatures[docID2]

            # we go in Band in Band, here we compare band a band for
            # doc1 and doc2

            bs2 = band_signatures.get(docID2)
            if bs2 == None:
                bs2 = []

            # cicliamo per ogni banda, appena ne troviamo una uguale usciamo dal ciclo
            # qua vado di coppia in coppia
            for k in range(0, B):
                if safe_list_get(bs1, k) != None:
                    # we have yet the k-band
                    band1 = str(bs1[k])
                else:
                    # we don't have the k-band, we have to calculate
                    band1 = str(h(str(signature1[k * R:(k + 1) * R])))
                    bs1.append(band1)
                    band_signatures[docID1] = bs1

                if safe_list_get(bs2, k) != None:
                    # we have yet the k-band
                    band2 = str(bs2[k])
                else:
                    # we don't have the k-band, we have to calculate
                    band2 = str(h(str(signature2[k * R:(k + 1) * R])))
                    bs2.append(band2)
                    band_signatures[docID2] = bs2

                # after this line we have the two band and we have to compare
                # if they are equal we can skip to the next pair
                if len(band1) != 0 and len(band2) != 0:
                    if band1 == band2:
                        # add for the deep compare
                        # save the info
                        if possibile_pairs_dataset.get(docID1) == None:
                            possibile_pairs_dataset[docID1] = signature1
                        if possibile_pairs_dataset.get(docID2) == None:
                            possibile_pairs_dataset[docID2] = signature2

                        # save the key of the pair
                        possible_pairs.append(docID1)
                        possible_pairs.append(docID2)

                        # we can go out of the loop
                        break
                else:
                    print 'ERRORREE band1 o band2 sono a zero, perche?'
                    print band1
                    print band2
    # print possible_pairs
    elapsed = (time.time() - t0)
    print "\nCalculate the possible pairs... took %.2fsec" % elapsed
     # 3. Compare all MinHash signatures to one another.
    print '\nComparing the possible pairs found...'

    numPossiblePair = len(possible_pairs)/2
    # Time this step.
    t0 = time.time()

    # siccome usiamo come docID degli interi sulla ns collection possiamo fare in questo modo per velocizzare:
    # For each of the test documents...

    # Count the number of positions in the minhash signature which are equal.
    n = N  # log_dict(signatures)

    for i in range(0, numPossiblePair):
        # Get the MinHash signature for document i.
        docID1 = possible_pairs[i*2]
        docID2 = possible_pairs[i*2+1]
        # print str(docID1)+'-'+str(docID2)

        signature1 = possibile_pairs_dataset[docID1]
        signature2 = possibile_pairs_dataset[docID2]
        # print 'signature1 :'+str(signature1)
        # print 'signature2:' + str(signature2)
        count = 0
        for k in range(0, n):
            # print signature1[k]
            # print signature2[k]
            count = count + (signature1[k] == signature2[k])
            # print 'count: ', count

        # print "  %5s --> %5s   %.2f" % (docID1, docID2, (float(count) / float(n)))

        # Record the percentage of positions which matched.
        coord = getTriangleIndex(docID1, docID2, numDocs)
        estJSim[coord] = (float(count) / float(n))

    elapsed = (time.time() - t0)
    print "\nComparing MinHash signatures took %.2fsec" % elapsed

    return estJSim


def safe_list_get(l, idx, default=None):
  try:
    return l[idx]
  except IndexError:
    return default