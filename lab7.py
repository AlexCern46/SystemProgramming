import ctypes
import random


def get_random_chr_matrix():
    matrix = []
    for i in range(10):
        matrix.append([])
        for j in range(10):
            symbol = chr(random.randint(97, 122))
            matrix[i].append(symbol)
    return matrix


def convert(matrix):
    c_array = (ctypes.POINTER(ctypes.c_char) * len(matrix))()
    for i in range(len(matrix)):
        row = ''.join(matrix[i]).encode('utf-8')
        c_array[i] = ctypes.create_string_buffer(row)
    return c_array


def main():
    dll = ctypes.CDLL('./DLL_Project.dll')

    matrix = get_random_chr_matrix()
    for row in matrix:
        print(row)

    chr_matrix = convert(matrix)

    string = ctypes.c_char_p(input('Enter string: ').encode('utf-8'))

    dll.SearchStr(chr_matrix, string)
