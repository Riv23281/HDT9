import pickle
from collections import Counter

class HuffmanCompression:
    @staticmethod
    def calcular_frecuencias(archivo):
        with open(archivo, 'r') as f:
            contenido = f.read()
            frecuencias = Counter(contenido)
        return frecuencias

    @staticmethod
    def generar_codigos(nodo, codigo, codigos):
        if nodo.valor:
            codigos[nodo.valor] = codigo
        else:
            HuffmanCompression.generar_codigos(nodo.izquierda, codigo + '0', codigos)
            HuffmanCompression.generar_codigos(nodo.derecha, codigo + '1', codigos)

    @staticmethod
    def comprimir(archivo_texto):
        archivo_huffman = archivo_texto + '.huff'
        archivo_arbol = archivo_texto + '.tree'

        frecuencias = HuffmanCompression.calcular_frecuencias(archivo_texto)
        arbol = HuffmanCompression.construir_arbol(frecuencias)
        codigos = {}
        HuffmanCompression.generar_codigos(arbol, '', codigos)

        with open(archivo_arbol, 'wb') as f:
            pickle.dump(arbol, f)

        with open(archivo_texto, 'r') as entrada, open(archivo_huffman, 'wb') as salida:
            contenido = entrada.read()
            codigo_huffman = ''.join(codigos[caracter] for caracter in contenido)
            while len(codigo_huffman) % 8 != 0:
                codigo_huffman += '0'
            bytes_comprimidos = bytearray([int(codigo_huffman[i:i+8], 2) for i in range(0, len(codigo_huffman), 8)])
            salida.write(bytes_comprimidos)

        print("Compresión completada. Archivos creados: {}.huff y {}.tree".format(archivo_texto, archivo_texto))

    @staticmethod
    def construir_arbol(frecuencias):
        nodos = [Nodo(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
        while len(nodos) > 1:
            nodos.sort(key=lambda x: x.frecuencia)
            izquierda = nodos.pop(0)
            derecha = nodos.pop(0)
            nuevo_nodo = Nodo(None, izquierda.frecuencia + derecha.frecuencia)
            nuevo_nodo.izquierda = izquierda
            nuevo_nodo.derecha = derecha
            nodos.append(nuevo_nodo)
        return nodos[0]

    @staticmethod
    def cargar_arbol(archivo_arbol):
        with open(archivo_arbol, 'rb') as f:
            arbol = pickle.load(f)
        return arbol

    @staticmethod
    def decodificar_mensaje(bits, arbol):
        mensaje = ''
        nodo_actual = arbol
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
            if nodo_actual.valor:
                mensaje += nodo_actual.valor
                nodo_actual = arbol
        return mensaje

    @staticmethod
    def descomprimir(archivo_huffman, archivo_arbol):
        with open(archivo_huffman, 'rb') as f:
            bits = ''.join(format(byte, '08b') for byte in f.read())

        arbol = HuffmanCompression.cargar_arbol(archivo_arbol)
        mensaje_original = HuffmanCompression.decodificar_mensaje(bits, arbol)

        archivo_descomprimido = archivo_huffman.replace('.huff', '_descomprimido.txt')
        with open(archivo_descomprimido, 'w') as f:
            f.write(mensaje_original)

        print("Descompresión completada. Archivo descomprimido creado: {}".format(archivo_descomprimido))

class Nodo:
    def __init__(self, valor, frecuencia):
        self.valor = valor
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

if __name__ == "__main__":

    #Colocar dirección del archivo .txt
    archivo_texto = "C:/Users/Eduardo/HDT9/src/texto_prueba.txt"  
    HuffmanCompression.comprimir(archivo_texto)
