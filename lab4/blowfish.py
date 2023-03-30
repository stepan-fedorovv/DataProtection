from Arrays import P, S, K


class Blowfish():

    def start(self):
        for i in range(0, 18):
            P[i] = P[i] ^ K[i % 14]

        k = 0
        data = 0
        for i in range(0, 9):
            temp =  self.encrypt(data)
            P[k] = temp >> 32
            k+=1
            P[k] = temp & 0xffffffff
            k+=1
            data = temp
        encrypt_data = int(input("Enter data to encrypt: "))
        encrypted_data = self.encrypt(encrypt_data)
        print(encrypted_data)

    def swap(self, L: int, R: int) -> tuple[int, int]:
        temp = L
        L = R
        R = L
        return L, R

    def encrypt(self, data: int) -> int:
        L = data >> 32
        R = data & 0xffffffff
        for i in range(0, 16):
            L = P[i] ^ L
            L1 = self.func(L)
            R = R ^ self.func(L1)
            L, R = self.swap(L, R)

        L, R = self.swap(L, R)
        L = L ^ P[17]
        R = R ^ P[16]
        enc = (L << 32) ^ R
        return enc

    def func(self, L):
        temp = S[0][L >> 24]
        temp = (temp + S[1][L >> 16 & 0xff]) % 2 ** 32
        temp = temp ^ S[2][L >> 8 & 0xff]
        temp = (temp + S[3][L & 0xff]) % 2 ** 32
        return temp


b = Blowfish()
b.start()