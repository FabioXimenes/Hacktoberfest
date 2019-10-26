limit = int(input('You need primes till(give upper limit):  ').rstrip())

def soe(limit): #a generator
    """
    Uses sieve of eratosthenes algorithm for finding primes.
    """
    list_init = [0]*(limit+1)
    list_init[0], list_init[1] = 1, 1
    for i in range(limit+1):
        if i > int(limit**0.5): break
        if list_init[i] == 0:
            for k in range(2*i, limit+1, i): list_init[k] = 1
    for i, j in enumerate(list_init):
        if j == 0: yield i

print(list(soe(limit)))
