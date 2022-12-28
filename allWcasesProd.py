"""The first part of the code is M21AAIC.py---a modification
of the code 21AAIC.py. The key change is the introduction of
parity 'p' in lines 8, 26 and 27 of the code 21AAIC.py.
---
For p=1 this is precisely the code 21AAIC.py (except for
printing [0,0] in the "w even" case)---it counts the number 
P(n) of [k1,k2,...,kw]-admissible colored partitions of n <= N
on the array Nw of w rows of natural numbers, with odd numbers 
in the top row.
---
For p=0 the code counts the number P(n) of [k1, ..., kw]-admissible
colored partitions of n <= N on the array Nw of w rows of natural 
numbers, with even numbers in the top row.
---
We input by hand p and k1,k2,...,kw as the list 'highest_weight' on 
lines 75 and 76. The result is a list 'result' of pairs [n,P(n)].
---
In the second part of the code Euler's factoring algorithm is applied
to determine the conjectured infinite periodic product with the period 
mod = 2*k+w+1."""

def get_row(i, w):
    return [max(0, x) for x in range(i*2 - p, i*2 - w - p, -1)]

def all_subfrequencies(c, r):
    for g0 in range(r + 1):
        if c == 1:
            yield [g0]
        else:
            for gs in all_subfrequencies(c - 1, max(0, r - g0)):
                yield [g0] + gs

def all_frequencies(i, *ks):
    rest = []
    for x in reversed(ks):
        rest.append(x)
    if i > w//2:
        for gs in all_subfrequencies(w, k):
            yield gs
    else:
        for gs in all_subfrequencies(i*2-p, sum(ks[-i*2+p:])):
            yield gs + rest[2 * i-p:]

def filter_frequencies(fs, ms1, *ks):
    k = sum(ks)
    ms = []
    for j, f in enumerate(fs):
        if j:
            m = ms1[j - 1]
            m0 = ms[-1]
            if m0 > m:
                m = m0
            m += f
            if m > k:
                return None
            ms.append(m)
        else:
            ms.append(f)
    return ms

def row_fs_value(row, fs):
    s = 0
    for v, f in zip(row, fs):
        s += v * f
    return s

if __name__ == '__main__':

    """One should put by hand 'p' and the 'highest wight'. For conjectured
    Rogers-Ramanujan type identities the 'highest weight' depends on p and w:
    for p=1, w=2n+1 and (k0,k1,...,kn) put [k0,0,k1,0,...,0,k(n-1),0,kn];
    for p=1, w=2n and (k0,k1,...,kn)e put [k0,k1,0,...,0,kn];
    for p=0, w=2n-1 and (k0,k1,...,kn)'odd' put [k0,k1,0,k2,0,...,0,k(n-1),kn];
    for p=0, w=2n and (k0,k1,...,kn)e put [k0,0,k1,0,...,0,k(n-1),kn];"""

    p = 0
    highest_weight = [1, 1, 0, 0, 0]
    #print("highest_weight =", highest_weight)
    print("the first row parity p =", p,", the highest_weight =", highest_weight,",")
    w = len(highest_weight)
    k = sum(highest_weight)
    #print('k =', k, 'w =', w, 'p =', p)

    """One should put by hand 'big enough' N, or set N = 2*k+w+1 if only the list
    'firstqpowers' is needed."""

    N = 2*k+w+1
    #N = 30
    #print("N =", N)

    i = 1
    frequencies = {}
    result = []
    ms0 = []
    for j in range(0, len(highest_weight)):
        ms0.append(sum(highest_weight[-j-1:]))
    all_total_ms0 = [(0, ms0)]
    while True:
        all_total_ms1 = []
        row1 = get_row(i, w)
        #print( 'i =', i, 'row1 =', row1)
        min_next_row = get_row(i + 1, w)[-1]
        all_fs = list(all_frequencies(i, *highest_weight))
        #print( 'i =', i, 'all_fs =', all_fs)
        for total0, ms0 in all_total_ms0:
            for fs1 in all_fs:
                ms = filter_frequencies(fs1, ms0, *highest_weight)
                if ms is None:
                    continue
                total1 = row_fs_value(row1, fs1) + total0
                if total1 <= N:
                    if total1 > total0:
                        frequencies[total1] = 1 + frequencies.get(total1, 0)
                    if total1 <= N - min_next_row:
                        all_total_ms1.append((total1, ms))
        if row1[-2] > 0:
            result.append([row1[-1], frequencies.get(row1[-1], 0)])
            result.append([row1[-2], frequencies.get(row1[-2], 0)])
        if max(row1[-2:]) >= N:
            break
        i += 1
        all_total_ms0 = all_total_ms1

#print(result)

coeff = [1]
for pair in result:
    if pair[0] > 0:
        coeff = coeff +[pair[1]]
#print(coeff)  

"""For a given list 'coeff' of coefficients of a power series c(q)
we apply Euler's factorization algorithm to to express c(q) as an
infinite product P(q). The result is a list 'qpowers' of positive 
integer exponents m for factors (1-q^m) in the denomimator of P(q).
The negative integers -m in the list 'qpowers' stand for a factors 
(1-q^m) in the numerator of P(q)."""    

n = len(coeff)-1
mod = 2*k+w+1
mzeros = []
qpowers = []
qmodpowers = []
for m in range (1, n):
    mzeros = []
    if coeff[m] != 0:
        for x in range(1,m+1):
            mzeros = mzeros + [0]
        if coeff[m] > 0:
            while coeff[m] > 0:
                coeff1 = []
                shmcoeff = mzeros+coeff
                for j in range(0,n):
                    coeff1 = coeff1 + [coeff[j]-shmcoeff[j]]   
                coeff = coeff1
                qpowers = qpowers + [m]
                qmodpowers = qmodpowers +[m % mod]

        if coeff[m] < 0:
            while coeff[m] < 0:
                shmcoeff = mzeros+coeff
                i = 1
                while i*m < n:
                    coeff1 = []
                    for j in range(0,n):
                        coeff1 = coeff1 + [coeff[j]+shmcoeff[j]] 
                    shmcoeff = mzeros+shmcoeff
                    coeff = coeff1
                    i = i + 1
                qpowers = qpowers + [-m]
                qmodpowers = qmodpowers +[-(m % mod)]

"""It is conjectured that for certain initial conditions given by the 'highest weight'
(and p= 0 or 1) the power series c(q) (with the list of coeficients 'coeff') factorizes
into the conjectured infinite periodic product P(q) with the period mod = 2*k+w+1. The list
'firstqmodpowers' of positive integers m (or negative -m) gives the factors (1-q^m) in the
denominator (or numerator) of P(q)."""

firstqmodpowers = []
for x in qpowers:
    if abs(x) < mod:
       firstqmodpowers = firstqmodpowers + [x] 
#print(firstqmodpowers,"mod", mod)
print("the exponents of the conjectured periodic product:", firstqmodpowers,"mod", mod)

"""It is also conjectured that for certain choices of the 'highest weight' c(q) cannot be
factorized into a periodic infinite product. This case is better seen by taking a 'big enough'
N and by printing the lists 'qpowers' and/or 'qmodpowers'."""

#print(qpowers)
#print(qmodpowers,"mod", mod) 
    
