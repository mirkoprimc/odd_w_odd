# odd_w_odd

The first part of the code is M21AAIC.py---a modification
of the code [21AAIC.py](https://github.com/aprimc/new-partition-identities/blob/main/21AAIC.py). The key change is the introduction of
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
mod = 2*k+w+1.
