import csv
import scipy.stats as stats
import os
import sys

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


def calcular_probabilidades_subintervalos(theta, cantidad_subintervalos):
    t = theta
    n = cantidad_subintervalos
    arr = [0.0] * (n + 1)
    arr[0] = t
    arr[n] = (1 - t)**n

    for i in range(1, n):
        arr[i] = t * (1 - t)**i

    return arr


def calcular_frecuencias_esperadas(probabilidades_por_subintervalo, total_muestra):
    global esFiable
    esFiable = True
    n = len(probabilidades_por_subintervalo) - 1
    N = total_muestra 
    probs = probabilidades_por_subintervalo
    frecuencias_esperadas = [0.0] * (n + 1)
    
    for i in range(n + 1):
        frecuencias_esperadas[i] = probs[i] * N
        if frecuencias_esperadas[i] < 5:
            esFiable = False
    
    return frecuencias_esperadas



def calcular_frecuencias_observadas(arreglo_numeros_aleatorios, a, b, n):
    frecuencias_observadas = [0] * (n + 1)  # Inicializamos con 0 espacios

    contador_espacios = 0  # Contador para espacios entre valores dentro del intervalo

    for valor in arreglo_numeros_aleatorios:
        if a <= valor <= b:
            # Estamos dentro del intervalo
            if contador_espacios > n:
                # Ignoramos si hay más espacios que n
                contador_espacios = n
            frecuencias_observadas[contador_espacios] += 1
            #print("Hay" , contador_espacios, "espacios hasta el valor: ", valor)
            contador_espacios = 0
        else:
            # Estábamos fuera del intervalo
            contador_espacios += 1

    return frecuencias_observadas


def calcular_chi2(frecuencias_esperadas, frecuencias_observadas):
    fe = frecuencias_esperadas
    fo = frecuencias_observadas
    chi2 = 0
    for i in range(len(frecuencias_esperadas)):
        chi2 = chi2 + ((fo[i] - fe[i])**2 / fe[i])
   
    return chi2


def imprimir_resultados(chi2, valor_critico, probabilidades, frecuencias_esperadas, frecuencias_observadas, valor_de_n):
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


#Pedir los parametros de inicio
print("Nombre del archivo que se pondra a prueba: ")
path = input()

while True:
    print("Valores del intervalo (a; b): ")
    print("Valor inferior del intervalo (a): ")
    a = float(input())
    print("Valor superior del intervalo (b): ")
    b = float(input())
    
    if (0 <= a <= 1) and (0 <= b <= 1) and (a <= b):
        break
    else:
        print("Por favor, ingresa valores válidos. a y b deben estar en el intervalo [0, 1] y a debe ser menor o igual a b.")


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
t = b - a   #Valor de theta
N = len(arr_num_aleat) * t
grados_de_libertad = int(n)

# Calculos
probabilidades = calcular_probabilidades_subintervalos(t, n) 
frecuencias_esperadas = calcular_frecuencias_esperadas(probabilidades, N)
frecuencias_observadas = calcular_frecuencias_observadas(arr_num_aleat, a, b, n)
chi2 = calcular_chi2(frecuencias_esperadas, frecuencias_observadas)
valor_critico = stats.chi2.ppf(nivel_de_confianza, grados_de_libertad)


# Imprimir por consola los resultados
imprimir_resultados(chi2, valor_critico, probabilidades, frecuencias_esperadas, frecuencias_observadas, n)