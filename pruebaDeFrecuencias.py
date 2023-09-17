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

def calcular_frecuencias_esperadas(num_subintervalos, total_muestra):
    n = num_subintervalos
    N = total_muestra
    valores_fe = [None] * n
    for i in range(n):
        valores_fe[i] = (N / n)
    
    return valores_fe


def calcular_frecuencias_observadas(secuencia_de_numeros, num_subintervalos):
    n = num_subintervalos
    valores_fo = [0] * n
    interv = 1 / n
    for i in range(n):
        for valor in secuencia_de_numeros:
            if interv*i <= valor < interv*(i + 1):
                valores_fo[i] = valores_fo[i] + 1 
    
    return valores_fo


def calcular_chi2(frecuencias_esperadas, frecuencias_observadas):
    fe = frecuencias_esperadas
    fo = frecuencias_observadas
    chi2 = 0
    for i in range(len(frecuencias_esperadas)):
        chi2 = chi2 + ((fo[i] - fe[i])**2 / fe[i])
   
    return chi2


def imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas, num_subintervalos):
    subintervalos = []
    n = num_subintervalos
    print("\nFrec. Esperada: ", [round(x, 5) for x in frecuencias_esperadas])
    print("Frec. Observada:", [float(x) for x in frecuencias_observadas])
    for i in range(1, n + 1):
        subintervalos.append(i/n)
    print("\t\t", [round(x, 5) for x in subintervalos])
    print("\nChi-Cuadrado: ", round(chi2, 5))
    print("Valor Critico: ", round(valor_critico, 5))
    if chi2 < valor_critico:
        return print("\nDado que ", round(chi2, 5), "<", round(valor_critico, 5), 
                    " se dice que los numeros aleatorios pasan la prueba de uniformidad")

    return print("\nDado que ", round(chi2, 5), ">", round(valor_critico, 5), 
                " se dice que los numeros aleatorios NO pasan la prueba de uniformidad")
             

# Pedir los parametros de inicio
print("Nombre del archivo que se pondra a prueba: ")
path = input()

while True:
    print("Cuantos subintervalos desea usar (valor de n): ")
    n = int(input())

    if n > 1:
        break
    else:
        print("Por favor, ingrese un número mayor a 1.")


while True:
    print("Ingrese el Nivel de confianza (valores mas comunes: 90, 95, 99): ")
    nivel_de_confianza = float(input())

    if 90 <= nivel_de_confianza <= 99:
        break
    else:
        print("Por favor, ingrese un nivel de confianza válido entre 90 y 99.")

nivel_de_confianza = nivel_de_confianza / 100


# Crear una lista con todos los numeros aleatorios del CSV
arr_num_aleat = leer_archivo(path)

# Variables necesarias para la ejecucion del prgrama
N = len(arr_num_aleat)
grados_de_libertad = int(n - 1)

# Calculos
frecuencias_esperadas = calcular_frecuencias_esperadas(n, N)
frecuencias_observadas = calcular_frecuencias_observadas(arr_num_aleat, n)
chi2 = calcular_chi2(frecuencias_esperadas, frecuencias_observadas)
valor_critico = stats.chi2.ppf(nivel_de_confianza, grados_de_libertad)


# Imprimir por consola los resultados
imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas, n)





