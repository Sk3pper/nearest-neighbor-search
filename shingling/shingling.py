# Implement a class that, given a document, creates its set of character shingles of some length k.
# Then represent the document as the set of the hashes of the shingles, for some hash function.
import binascii

from utils.hashFamily import hashFamily


def shingling(document, k, ByteHashFamiliShingles, isHash=None, print_=None):

    shingles = [document[i:i + k] for i in range(len(document) - k + 1)]

    if print_:
        print shingles

    if isHash:
        hash = hashFamily(123, ByteHashFamiliShingles)
        hash_shingles = []
        for s in shingles:
            hash_shingles.append(hash(s))
        return set(hash_shingles)

        return hash_shingles

    return set(shingles)
