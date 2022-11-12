"""Burrows-Wheeler transform."""


# I would normally use '\x00' for the sentinel, but doctest doesn't
# like that (because it is gods damned stupid). For this example,
# using $ will be fine, but it would not be a good choice in production
# code...

def suffixArray(x: str) -> list:
    """Given x return suffix array SA(x). 

    Args:
        x (str): input string.
    """  
    satups = sorted([(x[i:], i) for i in range(len(x))])
    return list(map(lambda t: t[1], satups))

def calc_O(bwt: str, C: dict) -> dict:
    '''
    >>>calc_O('aaba$')
    O = { '$' : [0, 0, 0, 1, 1, 1], 'a' : [0, 1, 1, 1, 2, 3], 'b' : [0, 0, 1, 1, 1, 1]}
    '''
    O = C.copy()
    for k in O.keys():
        O[k] = [0]
    
    for char in bwt:
        for k in O.keys():
            if k == char:
                O[k].append(O[k][-1]+1)
            else:
                O[k].append(O[k][-1])
    
    return O

def bucket_first(first: list) -> dict:
    '''
    >>> count_to_bucket([$,i,i,i,i,m,p,p,s,s])
    bucket = {$ : 0, i : 1, m : 5, p : 6, s : 8}
    '''
    C = {}
    for i,c in enumerate(first):
        if c in C:
            continue
        else:
            C[c] = i

    return C

def bwt(x: str) -> str:
    """
    Transform x into its Burrows-Wheeler transform.

    >>> bwt('mississippi')
    'ipssm$pissii'
    """

    sa = suffixArray(x)
    col = len(x)-1 # column at the back

    return ''.join([x[(i + col)%len(x)] for i in sa])

def rbwt(y: str) -> str:
    """
    Reverse the Burrows-Wheeler transform for y.

    >>> rbwt('ipssm$pissii')
    'mississippi'
    """
    sentinel = True
    first = sorted([l for l in y])
    if not first[0] == '$':
        sentinel = False
        first[0] = '$'

    C = bucket_first(first)
    O = calc_O(y, C)


    first = ''.join(first)
    i = y.find(first[0]) # start at sentinel in bwt
    x = [y[i]]*len(y)
    for j in range(2,len(y)+1):
        i = C[y[i]]+O[y[i]][i] # i = start of letter bucket + amount of that seen letter up to that point
        x[-j] = y[i] # fill from the back

    if sentinel == False:
        x.pop()

    return ''.join(x)

# def main():
#     x = 'aaba$'
#     y = bwt(x)
#     print(rbwt(y))

# if __name__ == '__main__':
#     main()
