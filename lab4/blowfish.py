import struct


def F(L):
    temp = S[0][L >> 24]
    temp = (temp + S[1][L >> 16 & 0xff]) % (0x1 << 32)
    temp = temp ^ S[2][L >> 8 & 0xff]
    temp = (temp + S[3][L & 0xff]) % (0x1 << 32)
    return temp
'''
Значение каждого раундового ключа Pn (P1, P2 …) складывается по модулю 2 (XOR) с соответст- вующим элементами исходного ключа K. 
Например, выполняется XOR раундового ключа P1 с первыми 32 битами исходного ключа K, P2 со вторыми 32 битами исходного ключа K и так далее. 
Если исходный ключ K короче длины всех раундовых ключей (576 бит), то он конкатенируется сам с собой: KK, KKK и так далее.
'''


def blowfish_encrypt_block(data):
    L = data >> 32
    R = data & 0xffffffff
    for i in range(0, 16):
        L = L ^ P[i]
        L1 = F(L)
        R = R ^ F(L1)
        L, R = R, L
    L, R = R, L
    L = L ^ P[17]
    R = R ^ P[16]
    encrypted = (L << 32) ^ R
    return encrypted


def get_fixed_param(text):
    # Get P
    global FIXED_P
    FIXED_P = list()
    for i in range(18):
        FIXED_P.append(int(text[i * 8:(i + 1) * 8], 16))
    offset = 18 * 8
    # Get S[4][256]
    global FIXED_S
    FIXED_S = list()
    for i in range(4):
        FIXED_S.append(list())
        for j in range(256):
            FIXED_S[i].append(int(text[j * 8 + offset:(j + 1) * 8 + offset], 16))
        offset += 256 * 8


def key_extension(key: str):
    with open('mantissas_Pi.txt', 'r') as inp:
        text = inp.read()
    text = text.replace('\n', '')
    print(text)
    get_fixed_param(text)

    global P, S
    P = []
    S = FIXED_S
    key_byte = key.encode('utf-8')
    k = 0
    for i in range(18):
        long_key = 0
        for j in range(4):
            long_key = (long_key << 8) | key_byte[k % len(key_byte)]
            k += 1
        P.append(FIXED_P[i] ^ long_key)

    k = 0
    l = 0
    data = struct.unpack('Q', ((k << 32) + l).to_bytes(8, byteorder='big').ljust(8, b'\0'))[0]
    for i in range(0, 18, 2):
        data = blowfish_encrypt_block(data)
        P[i] = data >> 32
        P[i + 1] = data % (0x1 << 32)
    for i in range(4):
        for j in range(0, 256, 2):
            data = blowfish_encrypt_block(data)
            S[i][j] = data >> 32
            S[i][j + 1] = data % (0x1 << 32)
    return P, S

def blowfish_decrypt_block(data):
    L = data >> 32
    R = data & 0xffffffff
    for i in range(17, 1, -1):
        L = P[i] ^ L
        L1 = F(L)
        R = R ^ F(L1)
        L, R = R, L

    L, R = R, L
    L = L ^ P[0]
    R = R ^ P[1]
    decrypted = (L << 32) ^ R
    return decrypted


def encrypt(message: str, P, S):
    arr_of_64bit_numbers = []
    str_bites = message.encode('utf-8')
    for i in range((len(str_bites) + 7) // 8):
        arr_of_64bit_numbers.append(struct.unpack('Q', (str_bites[i * 8:(i + 1) * 8]).ljust(8, b'\0'))[0])

    encr = []
    for i in arr_of_64bit_numbers:
        encr.append(blowfish_encrypt_block(i))
    return encr


def decrypt(encr_message, P, S) -> str:
    decr = []
    for i in encr_message:
        decr.append(blowfish_decrypt_block(i))

    decrypt_mes = b''
    for num in decr:
        decrypt_mes += (struct.pack('Q', num))
    return decrypt_mes.decode()


message = 'Как так Тынdekц?'
key = 'smыth'

P, S = key_extension(key)

encrypt_message = encrypt(message, P, S)
mes = b''
for i in encrypt_message:
    mes += (struct.pack('Q', i))

print(f'Исходный текст - {message}\n')
print(f'Закодированная последовательность - {mes}\n')
print(f'Декодированный текст - {decrypt(encrypt_message, P, S)}')