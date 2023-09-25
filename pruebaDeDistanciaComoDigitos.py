import csv
import scipy.stats as stats
import os
import sys

def leer_archivo(path):
    valores = []  # Lista para almacenar los valores
    if os.path.isfile(path):  # Verificar si el archivo existe
        with open(path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')

            for fila in spamreader:
                for valor in fila:
                    valor_str = str(valor)  # Convertir el valor a cadena
                    
                    # Intentar dividir el valor por el punto decimal
                    partes = valor_str.split('.')
                    
                    if len(partes) > 1:
                        decimal_part = partes[1]
                        valor_digitos = [int(digit) for digit in decimal_part if digit.isdigit()]
                    else:
                        valor_digitos = [int(digit) for digit in valor_str if digit.isdigit()]

                    valores.extend(valor_digitos)  # Usar extend para agregar dígitos individualmente
    else:
        print(f"El archivo '{path}' no fue encontrado.")
        sys.exit(1)
    return valores



def calcular_probabilidades_huecos(n):
    arr = [0.0] * (n + 1)
    arr[0] = 0.1
    arr[n] = 0.9 ** n

    for i in range(1, n):
        arr[i] = 0.1 * (0.9 ** i)

    return arr


def calcular_frecuencias_esperadas(probabilidades_por_hueco, total_muestra):
    global esFiable
    esFiable = True
    N = total_muestra
    probs = probabilidades_por_hueco
    frecuencias_esperadas = [0.0] * (n + 1)
    
    for i in range(n + 1):
        frecuencias_esperadas[i] = probs[i] * N
        if frecuencias_esperadas[i] < 5:
            esFiable = False
    
    return frecuencias_esperadas


def calcular_frecuencias_observadas(arreglo_de_numeros, valor_de_n, tamaño_muestra):
    n = valor_de_n
    frecuencias_observadas = [0] * (n + 1)
    arr = arreglo_de_numeros
    for i in range(tamaño_muestra):
        numero_actual = arr[i]
        distancia = 0

        for j in range(i + 1, n + i + 1):
            if arr[j] == numero_actual:
                frecuencias_observadas[distancia] += 1
                break
            elif j >= i + n:
                frecuencias_observadas[n] += 1
                break
            distancia += 1

    return frecuencias_observadas


def calcular_chi2(frecuencias_esperadas, frecuencias_observadas):
    fe = frecuencias_esperadas
    fo = frecuencias_observadas
    chi2 = 0
    for i in range(len(frecuencias_esperadas)):
        chi2 = chi2 + ((fo[i] - fe[i])**2 / fe[i])
   
    return chi2


def imprimir_resultados(chi2, valor_critico, probabilidades,  frecuencias_esperadas, frecuencias_observadas, valor_de_n):
    formato = "  {:<2}   {:<10} {:<10} {:<10}"
    
    print(formato.format("i", "Pi", "Foi", "Fei"))
    for i in range(valor_de_n + 1):
        print(formato.format(i, round(probabilidades[i], 5), round(frecuencias_observadas[i], 5), round(frecuencias_esperadas[i], 5)))

    print("Total ", round(sum(probabilidades), 1), " \t ", sum(frecuencias_observadas), "\t    ", int(sum(frecuencias_esperadas)))
    
    print("\nChi-Cuadrado: ", round(chi2, 5))
    print("Valor Critico: ", round(valor_critico, 5))
    if chi2 < valor_critico:
        print("\nDado que ", round(chi2, 5), "<", round(valor_critico, 5), 
        " se dice que los numeros aleatorios pasan la prueba de uniformidad")
    else:
        print("\nDado que ", round(chi2, 5), ">", round(valor_critico, 5), 
        " se dice que los numeros aleatorios NO pasan la prueba de uniformidad")
    
    if esFiable is False:
        print("\n\n\t\t*AVISO*\nYa que hay valores de Frecuencias Esperadas menores a 5 no se debe confiar en el resultado de la prueba.")
        print("Se recomienda usar mas datos o menos subintervalos para obtener un resultado mas confiable.")
    return


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
N = len(arr_num_aleat) - n
grados_de_libertad = int(n)

# Calculos
probabilidades = calcular_probabilidades_huecos(n)
frecuencias_esperadas = calcular_frecuencias_esperadas(probabilidades, N)
frecuencias_observadas = calcular_frecuencias_observadas(arr_num_aleat, n, N)
chi2 = calcular_chi2(frecuencias_esperadas, frecuencias_observadas)
valor_critico = stats.chi2.ppf(nivel_de_confianza, grados_de_libertad)


# Imprimir por consola los resultados
imprimir_resultados(chi2, valor_critico, probabilidades, frecuencias_esperadas, frecuencias_observadas, n)