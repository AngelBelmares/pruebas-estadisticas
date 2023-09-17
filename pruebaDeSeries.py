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


def formar_parejas(secuencia_numeros):
    parejas = []
    
    for i in range(len(secuencia_numeros) - 1):
        pareja = (secuencia_numeros[i], secuencia_numeros[i + 1])
        parejas.append(pareja)
    
    return parejas


def calcular_frecuencias_esperadas(num_subintervalos, total_muestra):
    n = num_subintervalos
    N = total_muestra
    valores_fe = [[None] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            valores_fe[i][j] = ((N - 1) / n**2)
    
    return valores_fe


def calcular_frecuencias_observadas(parejas_de_numeros, num_subintervalos):
    pareja = parejas_de_numeros
    n = num_subintervalos
    valores_fo = [[0 for _ in range(n)] for _ in range(n)]
    interv = 1 / n
    
    for i in range(n):
        for j in range(n):
            for valor in parejas_de_numeros:
                if interv*j <= valor[0] < interv*(j + 1) and interv*i <= valor[1] < interv*(i + 1):
                    valores_fo[i][j] = valores_fo[i][j] + 1
    
    return valores_fo


def calcular_chi2(frecuencias_observadas, subintervalos, total_muestra):
    fo = frecuencias_observadas
    N = total_muestra
    n = subintervalos
    sumatoria = 0
    for i in range(n):
        for j in range(n):
            sumatoria = sumatoria + (fo[i][j] - ((N - 1) / n**2))**2
    chi2 = (n**2 / (N - 1)) * sumatoria
   
    return chi2


def imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas, num_subintervalos):
    subintervalos = []
    n = num_subintervalos
    u = n
    print("\nTabla de frecuencias Esperadas\n")
    for i in range(len(frecuencias_esperadas) - 1, -1, -1):
        print(round((1/n * u), 5) ,frecuencias_esperadas[i])
        u = u - 1
        subintervalos.append((i + 1)/n)
    print("     ", [x for x in subintervalos[::-1]])
    
    print("\nTabla de frecuencias Observadas\n")
    u = n
    for i in range(len(frecuencias_observadas) - 1, -1, -1):
        print(round((1/n * u), 1) ,frecuencias_observadas[i])
        u = u - 1
    print([x for x in subintervalos[::-1]])
    
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


# Crear una lista con todos los numeros aleatorios del CSV y despues hacer parejas
arr_num_aleat = leer_archivo(path)
parejas_numeros = formar_parejas(arr_num_aleat)

# Variables necesarias para la ejecucion del prgrama
N = len(arr_num_aleat)
grados_de_libertad = int(n**2 - 1)

# Calculos
frecuencias_esperadas = calcular_frecuencias_esperadas(n, N)
frecuencias_observadas = calcular_frecuencias_observadas(parejas_numeros, n)
chi2 = calcular_chi2(frecuencias_observadas, n, N)
valor_critico = stats.chi2.ppf(nivel_de_confianza, grados_de_libertad)


# Imprimir por consola los resultados
imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas, n)