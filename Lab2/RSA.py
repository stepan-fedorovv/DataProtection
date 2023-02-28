import random
from Ciphergram import Cipher


class RSA():
    def __init__(self, p: int, q: int, e:int,word: str) -> None:
        self.word = word
        self.p = p
        self.q = q
        self.e = e

    def GetOpenKey(self) -> tuple:
        n = self.p * self.q
        open_key = (self.e, n)
        return open_key

    def GetPrivateKey(self) -> tuple:
        f_n = (self.p - 1) * (self.q - 1)
        n = self.p * self.q
        k = 0
        d = ((k * f_n) + 1) / self.e
        if d != int(d):
            while d != int(d):
                k += 1
                d = ((k * f_n) + 1) / self.e
        private_key = (int(d), n)
        return private_key

    def Encode(self) -> list:
        word_list = list(self.word)
        encode_word = []
        for i in word_list:
            c_i = Cipher[i] ** self.GetOpenKey()[0] % self.GetOpenKey()[1]
            encode_word.append(c_i)
        return encode_word

    def Decode(self) -> None:
        decode_index = []
        for i in self.Encode():
            t_i = i ** self.GetPrivateKey()[0] % self.GetPrivateKey()[1]
            decode_index.append(t_i)
        for i in decode_index:
            letters = [k for k, v in Cipher.items() if v == i]
            print(f"{''.join(letters)} - {i}")





