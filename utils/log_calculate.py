import math

def log_dict(dict):
    n = math.log((len(dict)), math.e)
    # upperbound n
    n = int(math.ceil(n))
    n = 10
    # n = n*10
    print 'signature length: ' + str(n)

    return n