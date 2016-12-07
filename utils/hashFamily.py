# Implement a family of hash functions. It hashes strings and takes an
# integer to define the member of the family.
# Return a hash function parametrized by i
import hashlib
def hashFamily(i, resultSize):
    # resultSize = 4 # how many bytes we want back
    maxLen = 20 # how long can our i be (in decimal)
    salt = str(i).zfill(maxLen)[-maxLen:]

    def hashMember(x):
        # oss: facendo .digest() ritorna '\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'
        #      se facciamo .hexdigest() ritorna 'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
        # ritorniamo un intero perche' con digest/hexdigest non funziona nulla
        return int(hashlib.sha1(x + salt).hexdigest()[-resultSize:], 16)

    return hashMember


''' how to use:
    h = hashFamily(1)
    print h('c')'''


