from random import getrandbits
from math import sqrt
from sys import exit
#from hashlib import sha256
from sha1 import *

N = 1024
L = 160

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def number_gen(p,q,g):
    c = getrandbits(N+64)
    #print("C=",c)
    k = (c % (q-1))+1
    #print("k=",k)
    try:
        k_ = inverse(k,q)
        return (k,k_)
    except:
        return number_gen(p,q,g)

# Sign operation
def sign(p,q,g, H, x, y):
    k,k_ = number_gen(p,q,g)
    #print(k,k_)
    r = pow(g,k,p) % q
    #z = long(H, 16)
    H=int(H,16)
    k_=int(k_)
    #print(H)
    #print(k_)
    u=(H+x*r)
    s = (k_*u) % q
    #print(s)
    return (r, s)

# Verify operation
def verify(p,q,g, H, y, r,s):
    if 0 < r and r < q and 0 < s and s < q:
        w = inverse(s, q)
        z = int(H, 16)
        u1 = (z*w) % q
        u2 = (r*w) % q
        v = ((pow(g,u1,p) * pow(y,u2,p)) % p) % q
        print("v =",v)
        return v == r
    raise Exception('Verify Error')

def is_valid(p,q,g):
    return  ( is_prime(p) and is_prime(q)
              #and no_bits(p) == 1024 and no_bits(q) == 160
              and (p-1) % q == 0 and pow(g,q,p) == 1 and g > 1)


# Generate a pair of keys
def gen_pair(p,q,g):
    c = getrandbits(N+64)
    x = (c % (q-1))+1
    y = pow(g,x,p)
    return (x,y)

if __name__=='__main__':

    p = int(input("Enter first prime number.      "))
    q = int(input("Enter Second prime number.     "))
    g = int(input("Enter Mod Value.               "))

    if not is_valid(p,q,g):
        print('\ninvalid_group')
        exit(-1)
    print('\nvalid_group')

    (x,y) = gen_pair(p,q,g)
    print("\nPublic Key  = " + str(x))
    print("Private Key = " + str(y))

    msg=""
    Ds = [l for l in input("\nEnter your message. ").split(" ")]
    for i in Ds:
        msg+=i

    encrypted_msg=sha1(msg)
    print("\nMessage =",msg)
    print("\nEncrypted Message =",encrypted_msg)

    (r,s) = sign(p,q,g,encrypted_msg, x,y)
    print("\nGenerating Digital Signature................\n\nGenerated Digital Signature")
    print('r='+str(r))
    print('s='+str(s))

    print("\nVerifying Digital Signature.................\n")
    if verify(p,q,g,encrypted_msg,y,r,s):
        print('\nsignature_valid(v==r)')
    else:
        print('\nsignature_invalid(v!=r)')
