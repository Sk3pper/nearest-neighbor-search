import math

def log_dict(dict):
    n = math.log((len(dict)), math.e)
    # upperbound n
    n = int(math.ceil(n))
    # n = n*10
    print 'signature length: ' + str(n)

    return 10