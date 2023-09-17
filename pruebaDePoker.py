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
                        valores.append(valor)
                except ValueError:
                    print(f"Valor no numérico o fuera del rango en la fila: {valor}")
                pass  # Ignorar valores no numéricos y fuera del rango

    return valores


def probabilidades_de_manos():
    tabla_probabilidades = {
        'todosDiferentes': 0.30240,
        'unPar': 0.50400,
        'dosPares': 0.10800,
        'tercia': 0.07200,
        'full': 0.00900,
        'poker': 0.00450,
        'quintilla': 0.00010
    }
    return tabla_probabilidades


def calcular_m(frecuencias_esperadas):
    m = 0
    for clave, valor in frecuencias_esperadas.items():
        if valor < 5:
            return m  # Si algún valor es menor a 5, sal del bucle
        m += 1


def calcular_frecuencias_esperadas(probabilidades_de_mano, total_muestra):
    N = total_muestra
    valores_fe = {}
    
    for mano, probabilidad in probabilidades_de_mano.items():
        valores_fe[mano] = probabilidad * N

    return valores_fe


def calcular_frecuencias_observadas(secuencia_de_numeros_str): 
    frecuencias_observadas = {  # Diccionario con valores en 0
        'todosDiferentes': 0,
        'unPar': 0,
        'dosPares': 0,
        'tercia': 0,
        'full': 0,
        'poker': 0,
        'quintilla': 0
    }
    
    for numero in secuencia_de_numeros_str:
        parte_decimal = str(numero).split(".")[1]  # Obtener la parte decimal
        
        frecuencias = {}  # Diccionario para almacenar las frecuencias de los dígitos

        # Contar la frecuencia de cada dígito
        for digito in parte_decimal:
            frecuencias[digito] = frecuencias.get(digito, 0) + 1
            
            
        valores_frecuencia = list(frecuencias.values())
        num_valores_diferentes = len(valores_frecuencia)

        if num_valores_diferentes == 5:
            frecuencias_observadas['todosDiferentes'] += 1
        elif num_valores_diferentes == 4:
            frecuencias_observadas['unPar'] += 1
        elif num_valores_diferentes == 3:
            if 3 in frecuencias.values():
                frecuencias_observadas['tercia'] += 1
            else:
                frecuencias_observadas['dosPares'] += 1
        elif num_valores_diferentes == 2:
            if 4 in frecuencias.values():
                frecuencias_observadas['poker'] += 1
            else:
                frecuencias_observadas['full'] += 1
        elif num_valores_diferentes == 1:
            frecuencias_observadas['quintilla'] += 1
        else:
            print("Valor no válido")

    return frecuencias_observadas


def calcular_chi_cuadrado(frecuencias_esperadas, frecuencias_observadas):
    chi2 = 0
    fe = list(frecuencias_esperadas.values())
    fo = list(frecuencias_observadas.values())
    fe_agrupada = 0
    fo_agrupada = 0
    num_intervalos = 0

    for i in range(len(fo)):
        siguiente_frecuencia_esperada = fe[i + 1] if i + 1 < len(fe) else None

        if siguiente_frecuencia_esperada is not None and siguiente_frecuencia_esperada > 5:
            chi2 += (fo[i] - fe[i]) ** 2 / fe[i]
            num_intervalos += 1
        else:
            fe_agrupada += fe[i]
            fo_agrupada += fo[i]

    chi2 += (fo_agrupada - fe_agrupada) ** 2 / fe_agrupada
    return chi2


def imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas):
    print("\n\tFrec. Esperada:")
    for key, value in frecuencias_esperadas.items():
        print(key, round(value, 5))
    print("\n\tFrec. Observada:")
    for valor in frecuencias_observadas.items():
        print(valor)

        
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


# Calculos
probabilidades = probabilidades_de_manos() 
frecuencias_esperadas = calcular_frecuencias_esperadas(probabilidades, N)
frecuencias_observadas = calcular_frecuencias_observadas(arr_num_aleat)
m = calcular_m(frecuencias_esperadas)


grados_de_libertad = (m - 1)
chi2 = calcular_chi_cuadrado(frecuencias_esperadas, frecuencias_observadas)
valor_critico = stats.chi2.ppf(nivel_de_confianza, grados_de_libertad)


# Imprimir por consola los resultados
imprimir_resultados(chi2, valor_critico, frecuencias_esperadas, frecuencias_observadas)
