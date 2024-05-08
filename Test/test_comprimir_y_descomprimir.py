import unittest
import os
import sys

sys.path.append("C:/Users/2004e/HDT9/src")  
from Comprimir_Y_Descomprimir import Comprimir_y_descomprimir

class TestComprimirYDescomprimir(unittest.TestCase):
    def test_comprimir_y_descomprimir(self):
        archivo_texto = "C:/Users/2004e/HDT9/src/prueba.txt"  
        Comprimir_y_descomprimir.comprimir(archivo_texto)

        archivo_comprimido = archivo_texto + ".huff"
        archivo_arbol = archivo_texto + ".tree"

        self.assertTrue(os.path.exists(archivo_comprimido))
        self.assertTrue(os.path.exists(archivo_arbol))

        mensaje_original = Comprimir_y_descomprimir.descomprimir(archivo_comprimido, archivo_arbol)

        with open(archivo_texto, 'r') as f:
            contenido_original = f.read()

        self.assertEqual(mensaje_original, contenido_original)

    def test_calcular_frecuencias(self):
        archivo_texto = "C:/Users/2004e/HDT9/src/prueba.txt" 
        frecuencias_esperadas = {'a': 2, 'b': 1, 'c': 1, 'd': 4, '\n': 2}
        frecuencias = Comprimir_y_descomprimir.calcular_frecuencias(archivo_texto)
        self.assertEqual(frecuencias, frecuencias_esperadas)

if __name__ == '__main__':
    unittest.main()
