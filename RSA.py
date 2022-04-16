from math import gcd

N = 329159
e = 7 #public
d = 46543 #secret
p = 101
q = 3259
'''
N = p * q　(coprime)
L = lcm(p-1, q-1)
e which gcd(E, L) = 1
d which (E, D) mod L = 1
encryption : Crypto = Plain^e mod N
    pow(P, E, N) => C
decryption : Plain = Crypto^d mod N
    pow(C, D, N) => P
'''

plain = 'Please encrypt me!'
dec_text = [253630, 393, 27573, 318532, 209682, 27573, 146994, 27573, 181510, 94307, 287693, 141332, 193545, 179374, 146994, 25541, 27573, 252293]


def encrypt_before(plaintext, public):
    enc_text = [ord(char) for char in plaintext]
    binary_e = format(public, 'b')
    return(enc_text, binary_e)

def r_enc(enc_text, binary_e):
    T = [1] * len(enc_text)
    flage = 0
    for it in enc_text:
        for jt in reversed(binary_e):
            T[flage] = (T[flage] * T[flage]) % N
            if jt == '1':
                T[flage] = (it * T[flage]) % N
        flage += 1
    print(T)
    return T

def decrypt_before(d):
    binary_d = format(d, 'b')
    return(binary_d)

def r_dec(dec_text, binary_d):
    S = [1] * len(dec_text)
    flagd = 0
    for i in dec_text:
        for j in (binary_d):
            S[flagd] = (S[flagd] * S[flagd]) % N
            if j == '1':
                S[flagd] = (i * S[flagd]) % N
                b = S[flagd]
                for a in range(10000000):
                   ( i * b )% N
                print("Y")
            else:
                 print("N")
        flagd += 1
    return S
    

#(enc_text, binary_e) = encrypt_before(plain, e)
#dec_text = r_enc(enc_text, binary_e)
#print(dec_text)

binary_d = decrypt_before(d)
decrypted_text = r_dec(dec_text, binary_d)
print(decrypted_text)
