'''
 ISEL - Instituto Superior de Engenharia de Lisboa.

 LEIC - Licenciatura em Engenharia Informatica e de Computadores.

 PIB - Processamento de Imagem e Biometria.

 dct2d.py

 Script python que representa a implementação da transformada DCT
 para duas dimensões.

 Tipos de inputs aceites:

    Por matriz:
        dct2d.py --matrix 3,5,16,5;1,16,4,6;14,7,0,4;2,4,11,10

    Por nome de ficheiro:
        dct2d.py --filename cameraman.tif

 Dependencias:

     Numpy and PIL

 @author Pedro Gabriel
'''

from PIL import Image, ImageDraw
import sys, os, math
from numpy import *

#global vars - Rows and Columns
M = 0
N = 0

def Cu(idx):
    '''
    coeficiente U
    '''
    if idx>0:
        return math.sqrt(2/M)
    return 1/math.sqrt(M)

def Cv(idx):
    '''
    coeficiente V
    '''
    if idx>0:
        return math.sqrt(2/N)
    return 1/math.sqrt(N)

def sum_of_sum(matrix, M,N,r,s):
    '''
    Soma ponto a ponto, seguida da formula da DCT2D
    '''
    return sum([sum([matrix[i,j] * math.cos(((2*i+1)*r*math.pi)/(2*M))*math.cos(((2*j+1)*s*math.pi)/(2*N)) for j in range(N)]) for i in range(M)])

def isum_of_sum(matrix, M,N,r,s):
    '''
    Soma ponto a ponto, seguida da formula da iDCT2D
    '''
    return sum([sum([Cu(i)*Cv(j)*matrix[i,j]*math.cos(((2*r+1)*i*math.pi)/(2*M)) * math.cos(((2*s+1)*j*math.pi)/(2*N)) for j in range(N)]) for i in range(M)])

def dct2(args):
    '''
    script principal para a aplicação da dct2d sobre uma matriz
    '''
    if len(args) != 3:
        sys.exit("Utilizacao: \ndct2d.py --filenam <filename> \dct2d.py --matrix <first_row;second_row;nth_row>")

    global M
    global N
    if args[1] == '--filename':
        image = parse_filename(args)
        original_matrix = image.load()
        M,N = image.size
    if args[1] == '--matrix':
        temp = (parse_matrix(args))
        M = len(temp)
        N = len(temp[0])
        original_matrix = matrix(temp)

    dct_matrix = zeros([M,N])#[[0]*n]*2
    for r in range(M):
        for s in range(N):
            dct_matrix[r,s] = Cu(r)*Cv(s)* sum_of_sum(original_matrix, M, N, r, s)
    return dct_matrix


def idct2(matrix_after_dct):
    idct_matrix = zeros([M,N])
    for r in range(M):
        for s in range(N):
            idct_matrix[r,s] = int(isum_of_sum(matrix_after_dct, M, N, r, s))
    return idct_matrix

def parse_filename(args):
    '''
    Parse de argumentos quando introduzido um "filename"
    '''
    filename = args[2]
    size = os.path.getsize(filename)
    print("Ficheiro \'{0}\' com um total de {1} bytes.".format(filename, size))
    try:
        image = Image.open(filename)
    except IOError as ioerr:
        sys.exit("Nao foi possivel abrir a imagem para leitura.\n" + str(ioerr))
    return image

def parse_matrix(args):
    '''
    Parse de argumentos quando introduzida uma matriz
    '''
    final = []
    separated_one = args[2].split(';')
    for i in range(len(separated_one)):
        separated_twice = separated_one[i].split(',')
        temp = []
        for j in range(len(separated_twice)):
            temp.append(float(separated_twice[j]))
        final.append(temp)
    return final

#para efeitos de 'print' da matriz
set_printoptions(formatter={'float': '{: 0.3f}'.format})

matrix_after_dct = dct2(sys.argv)
print(matrix_after_dct)
print("\n")
print(idct2(matrix_after_dct))
