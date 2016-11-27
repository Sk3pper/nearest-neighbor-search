# =============================================================================
#                     Define Triangle Matrices
# =============================================================================

# Define virtual Triangle matrices to hold the similarity values. For storing
# similarities between pairs, we only need roughly half the elements of a full
# matrix. Using a triangle matrix requires less than half the memory of a full
# matrix, and can protect the programmer from inadvertently accessing one of
# the empty/invalid cells of a full matrix.

import sys

# Define a function to map a 2D matrix coordinate into a 1D index.
def getTriangleIndex(i, j, numDocs):
    # If i == j that's an error.
    if i == j:
        sys.stderr.write("Can't access triangle matrix with i == j")
        sys.exit(1)
    # If j < i just swap the values.
    if j < i:
        temp = i
        i = j
        j = temp

    # Calculate the index within the triangular array.
    # This fancy indexing scheme is taken from pg. 211 of:
    # http://infolab.stanford.edu/~ullman/mmds/ch6.pdf
    # But I adapted it for a 0-based index.
    # Note: The division by two should not truncate, it
    #       needs to be a float.
    k = int(i * (numDocs - (i + 1) / 2.0) + j - i) - 1

    return k

