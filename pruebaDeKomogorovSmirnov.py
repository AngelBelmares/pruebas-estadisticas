import os
import sys
import csv
import scipy.stats as stats


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


def calcular_distribucion_acumulada(secuencia_de_numeros):
    
    for indice in range(len(secuencia_de_numeros)):
        secuencia_de_numeros[indice] = indice / secuencia_de_numeros[indice]
    
    return secuencia_de_numeros


def calcular_estadistico(distribucion_acumulada, secuencia_de_numeros):
    max_diferencia = 0.0
    da_max = 0
    se_max = 0
    
    for i in range(len(secuencia_de_numeros)):
        diferencia = abs(distribucion_acumulada[i] - secuencia_de_numeros[i])
        if diferencia > max_diferencia:
            max_diferencia = diferencia
            da_max = distribucion_acumulada[i]
            se_max = secuencia_de_numeros[i]
            
    print(f"\nDn = {da_max} - {se_max} = {max_diferencia}")
    return max_diferencia
    

def imprimir_resultados(Dn, d):

    if Dn < d:
        return print("\nDado que ", round(Dn, 5), "<", round(d, 5), 
                    " se dice que los numeros aleatorios pasan la prueba de uniformidad")

    return print("\nDado que ", round(Dn, 5), ">", round(d, 5), 
                " se dice que los numeros aleatorios NO pasan la prueba de uniformidad")
             

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

# calcular alpha
alpha = 1.0 - (nivel_de_confianza / 100) 


# Crear una lista con todos los numeros aleatorios del CSV
arr_num_aleat = leer_archivo(path)
N = len(arr_num_aleat)

# Ordenar los numeros en orden ascendente
arr_num_aleat.sort()

# Calcular la distribucion acumulada de los numeros generados
distribucion_acumulada = [i / N for i in range(1, N + 1)]

# Calcular el estaditico Kolmogorov-Smirnov
valor_maximo = calcular_estadistico(distribucion_acumulada, arr_num_aleat)

# Calcular el los grados de libertad y nivel de confianza
grados_de_libertad = int(N - 1)
valor_critico = stats.ksone.ppf(1 - alpha / 2, N)

# Imprimir por consola los resultados
imprimir_resultados(valor_maximo, valor_critico)