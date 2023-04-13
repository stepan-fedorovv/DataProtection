import os
import sys

BMP_HEADER_SIZE = 54


def encode_image(input_img_name: str, output_img_name: str, txt_file: str, degree: int):
    text = open(txt_file, 'r')
    input_image = open(input_img_name, 'rb')
    output_image = open(output_img_name, 'wb')

    bmp_header = input_image.read(BMP_HEADER_SIZE)
    output_image.write(bmp_header)
    text_mask, img_mask = masks(degree)

    while True:
        symbol = text.read(1)
        if not symbol:
            break

        symbol = ord(symbol)

        for _ in range(0, 8, degree):
            img_bytes = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_bytes |= bits
            output_image.write(img_bytes.to_bytes(1, sys.byteorder))
            symbol <<= degree

    output_image.write(input_image.read())

    text.close()
    input_image.close()
    output_image.close()

    return True


def decode(degree: int, to_read: int):
    text = open("decode_text.txt", "w")
    code_img = open('new_img.bmp', 'rb')

    code_img.seek(54)
    text_mask, img_mask = masks(degree)
    img_mask = ~img_mask

    read = 0
    while read < to_read:
        symbol = 0

        for _ in range(0, 8, degree):
            img_bytes = int.from_bytes(code_img.read(1), sys.byteorder) & img_mask

            symbol <<= degree
            symbol |= img_bytes

        read += 1
        text.write(chr(symbol))

    text.close()
    code_img.close()


def masks(degree):
    text_mask = 0b11111111
    image_mask = 0b11111111
    text_mask <<= (8 - degree)
    text_mask %= 256  # Оставляю последние 8 битов
    image_mask >>= degree
    image_mask <<= degree

    return text_mask, image_mask


encode_image("7.bmp", "new_img.bmp", "text.txt", degree=8)
decode(8, 12)
