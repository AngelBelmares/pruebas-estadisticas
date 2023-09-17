import os
import sys
import csv
import scipy.stats as stats
import numpy as np
import math


def leer_archivo(path):
    valores = []  # Lista para almacenar los valores válidos

    if not os.path.isfile(path):
        print(f"El archivo '{path}' no fue encontrado.")
        sys.exit(1)  # Salir del programa con un código de error

    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        for fila in spamreader:
            for valor in fila:
                try:
                    valor_float = float(valor)
                    if 0 <= valor_float < 1:
                        valores.append(valor_float)
                except ValueError:
                    print(f"Valor no numérico o fuera del rango en la fila: {valor}")
                    pass  # Ignorar valores no numéricos y fuera del rango

    return valores


def calcular_Zo(promedio, total_muestra):
    x = promedio
    N = total_muestra
    
    Zo = ((x - 1/2) * math.sqrt(N)) / math.sqrt(1/12)
    return Zo


def calcular_valor_critico(alpha):
    Zc = stats.norm.ppf(1 - alpha/2)
    return Zc


def imprimir_resultados(promedio, Zo, Zc):
    print("Promedio de la muestra: ", promedio)
    print("\nZo ", round(Zo, 5))
    print("Zc: ", round(Zc, 5))
    
    if abs(Zo) < Zc:
        return print("\nDado que", round(abs(Zo), 5), "<", round(Zc, 5), 
                    " entonces no se puede rechazar la hipotesis de que los numeros pseudoaleatorios tienen una media de 0.5")

    return print("\nDado que", round(abs(Zo), 5), ">", round(Zc, 5),
                "se puede rechazar la hipotesis de que los numeros pseudoaleatorios tienen una media de 0.5")
             

# Pedir los parametros de inicio
print("Nombre del archivo que se pondra a prueba: ")
path = input()

while True:
    print("Ingrese el Nivel de confianza (valores mas comunes: 90, 95, 99): ")
    nivel_de_confianza = float(input())

    if 90 <= nivel_de_confianza <= 99:
        break
    else:
        print("Por favor, ingrese un nivel de confianza válido entre 90 y 99.")


# Crear una lista con todos los numeros aleatorios del CSV
arr_num_aleat = leer_archivo(path)

# Variables necesarias para la ejecucion del prgrama
N = len(arr_num_aleat)
alpha = 1 - (nivel_de_confianza / 100)

# Calculos
promedio = np.mean(arr_num_aleat)
Zo = calcular_Zo(promedio, N)
Zc = calcular_valor_critico(alpha)


# Imprimir por consola los resultados
imprimir_resultados(promedio, Zo, Zc)