import hashlib
import random

def Sha(*args):
    a = ':'.join(str(a) for a in args)
    return int(hashlib.sha256(a.encode('utf-8')).hexdigest(), 16)

def randnum(n):
    return random.SystemRandom().getrandbits(n) % N

g = 2                       # generator modulo N
N = 8069496435*(10**5072)-1 # liczba pierwsza Sophie Germain
k = Sha(N, g)               # funkcja hashująca dla Sha256 i k=3

print("H = ", Sha,  "\nN = ", N, "\ng = ", g, "\nk = ", k, "\n")

I = "WAT2020" 
p = "WCY18KY2S1" 

print("REJESTRACJA:\n")
print("1.Uzytkownik wysyla LOGIN:", I, "HASLO:", p)
print("\n2.Modol uzytkownika generuje weryfikator:")

s = randnum(64)        # losowa sól
x = Sha(s, I, p)       # Klucz prywatny
v = pow(g, x, N)     
print(v, "\n\noraz klucz prywatny:", x)
print("\n3.Modol serwera zapisuje pod indeksem:", I,"salt =", s,"i weryfikator")

print("\n\nAUTORYZACJA:\n")

a = randnum(64)
A = pow(g, a, N)
print("1. Uzytkownik wysyla login:", I,"oraz krótkotrwaly klucz publiczny A =\n", A,"\n\nna podstawie losowej prywatnej liczby a =", a)

b = randnum(64)
B = (k * v + pow(g, b, N)) % N
print("\n2. Serwer wysyla salt:", s,"oraz krótkotrwaly klucz publiczny B =\n", B,"\n\nna podstawie losowej prywatnej liczby b =", b)

u = Sha(A, B)
print("\n3. Uzytkownik i serwer generuje wspolny klucz SHA(A, B) = U =", u)


print("\n4. Uzytkownik oblicza klucz sesji, a nastepnie hashuje go")

S_u = pow(B - k * pow(g, x, N), a + u * x, N)
K_u = Sha(S_u)
print("Klucz sesji: ", S_u)
print("\nHashowany klucz sesji: ", K_u)

print("\n5. Serwer oblicza klucz sesji, a nastepnie hashuje go")
S_s = pow(A * pow(v, u, N), b, N)
K_s = Sha(S_s)
print("Klucz sesji: ", S_s)
print("\nHashowany klucz sesji: ", K_s)

print("\n\nWERYFIKACJA:\n")
print("6. Uzytkownik wysyla potwierdzenie klucza sesji W_u =")
HN = Sha(N)
Hg = Sha(g)
HI = Sha(I)
W_u = Sha((HN^Hg), HI, s, A, B, K_u)
print(W_u)

print("2. Serwer wysyla potwierdzenie klucza sesji W_s =")
W_s = Sha(A, W_u, K_s)
print(W_s)
