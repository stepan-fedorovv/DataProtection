from Arrays import S,P,K


def func(L):
    temp = S[0][L >> 24]
    print(f"temp1: {temp}, S: {S[0]}")
    temp = (temp + S[1][L >> 16 & 0xff]) % 2 ** 32
    print(f"temp2: {temp}, S: {S[1]}")
    temp = temp ^ S[2][L >> 8 & 0xff]
    print(f"temp3: {temp}")
    temp = (temp + S[3][L & 0xff]) % 2 ** 32
    print(f"temp4: {temp}")

    return temp

data = 45
L = data >> 32
func(L)
