# Función realizada por Santiago Hernández

"""
En este módulo realizamos toda la parte matemática del balanceo químico.
Aquí construimos la matriz de la ecuación, aplicamos el método de
Gauss-Jordan y finalmente obtenemos los coeficientes enteros de la reacción.
"""

# Importamos gcd para calcular el máximo común divisor
# Esto nos ayuda más adelante a simplificar los coeficientes finales
from math import gcd

# Importamos la función que cuenta los átomos de cada compuesto
from traductor import conocer_cantidad_moles


# Esta función construye la matriz de la ecuación química
# La matriz será la base para aplicar Gauss-Jordan
def construir_matriz(reactivos, productos):

    # Primero contamos los átomos de cada reactivo y producto
    atomos_reactivos = [conocer_cantidad_moles(r) for r in reactivos]
    atomos_productos = [conocer_cantidad_moles(p) for p in productos]

    # Creamos un conjunto para guardar todos los elementos sin repetirlos
    elementos = set()

    # Recorremos todos los diccionarios de átomos para extraer los elementos presentes
    for conteo in atomos_reactivos + atomos_productos:
        elementos.update(conteo.keys())

    # Organizamos los elementos en orden alfabético
    elementos = sorted(elementos)

    # Unimos reactivos y productos en una sola lista
    compuestos = reactivos + productos

    # Aquí iremos guardando toda la matriz
    matriz = []

    # Recorremos cada elemento químico
    for i in elementos:

        fila = []

        # Agregamos los valores de los reactivos como positivos
        for conteo in atomos_reactivos:
            fila.append(float(conteo.get(i, 0)))

        # Agregamos los productos como negativos
        for conteo in atomos_productos:
            fila.append(-float(conteo.get(i, 0)))

        # Guardamos la fila completa en la matriz
        matriz.append(fila)

    # Finalmente devolvemos la matriz junto con la información adicional
    return matriz, elementos, compuestos



# Esta función aplica el método de Gauss-Jordan a la matriz
def gauss_jordan(matriz):

    # Hacemos una copia para no modificar la matriz original
    matriz = [fila[:] for fila in matriz]

    num_filas = len(matriz)
    num_cols = len(matriz[0]) if matriz else 0

    # Esta variable indica en qué fila trabajaremos el pivote
    fila_pivote = 0

    # Recorremos cada columna de la matriz
    for i in range(num_cols):

        fila_no_cero = None

        # Buscamos una fila que tenga un valor diferente de cero
        for fila in range(fila_pivote, num_filas):

            if abs(matriz[fila][i]) > 1e-9:
                fila_no_cero = fila
                break

        # Si toda la columna es cero continuamos con la siguiente
        if fila_no_cero is None:
            continue

        # Intercambiamos filas si es necesario
        matriz[fila_pivote], matriz[fila_no_cero] = (
            matriz[fila_no_cero],
            matriz[fila_pivote]
        )

        # Tomamos el valor pivote
        pivote = matriz[fila_pivote][i]

        # Dividimos toda la fila para convertir el pivote en 1
        matriz[fila_pivote] = [
            x / pivote for x in matriz[fila_pivote]
        ]

        # Ahora hacemos ceros arriba y abajo del pivote
        for fila in range(num_filas):

            if fila != fila_pivote and abs(matriz[fila][i]) > 1e-9:

                factor = matriz[fila][i]

                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        # Pasamos a la siguiente fila pivote
        fila_pivote += 1

    # Devolvemos la matriz ya reducida
    return matriz



# Esta función obtiene los coeficientes a partir de la matriz reducida
def extraer_coeficientes(matriz_rref, num_compuestos):

    # Creamos una lista inicial llena de ceros
    coeficientes = [0.0] * num_compuestos

    # Tomamos el último coeficiente como 1 para poder despejar los demás
    coeficientes[num_compuestos - 1] = 1.0

    # Recorremos las filas desde abajo hacia arriba
    for fila in reversed(matriz_rref):

        col_pivote = None

        # Buscamos la columna donde está el pivote
        for j in range(num_compuestos):

            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        # Si la fila está vacía seguimos con la siguiente
        if col_pivote is None:
            continue

        valor = 0.0

        # Despejamos el valor del coeficiente correspondiente
        for j in range(num_compuestos):

            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]

        coeficientes[col_pivote] = valor

    # Devolvemos los coeficientes encontrados
    return coeficientes



# Esta función calcula el mínimo común múltiplo entre dos números
def m_c_m(a, b):

    return abs(a * b) // gcd(a, b)



# Aquí convertimos los coeficientes decimales en enteros
def racionalizar_coeficientes(
    coeficientes,
    tolerancia=1e-6,
    max_denominador=1000
):

    denominadores = []

    # Recorremos cada coeficiente decimal
    for c in coeficientes:

        mejor_error = float('inf')
        mejor_denominador = 1

        # Probamos distintos denominadores para aproximar fracciones
        for q in range(1, max_denominador + 1):

            p = round(c * q)

            error = abs(c - p / q)

            # Guardamos la mejor aproximación encontrada
            if error < mejor_error:

                mejor_error = error
                mejor_denominador = q

            # Si el error es suficientemente pequeño dejamos de buscar
            if error < tolerancia:
                break

        denominadores.append(mejor_denominador)

    # Calculamos el mínimo común múltiplo de todos los denominadores
    mcm = denominadores[0]

    for d in denominadores[1:]:
        mcm = m_c_m(mcm, d)

    # Multiplicamos todos los coeficientes para volverlos enteros
    enteros = [abs(round(c * mcm)) for c in coeficientes]

    # Calculamos el máximo común divisor para simplificarlos
    mcd_total = enteros[0]

    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    # Simplificamos los coeficientes si es posible
    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    # Devolvemos los coeficientes enteros finales
    return enteros



# Esta función ejecuta todo el proceso de balanceo
def calcular_coeficientes(reactivos, productos):

    # Construimos la matriz inicial
    matriz_original, elementos, compuestos = construir_matriz(
        reactivos,
        productos
    )

    # Aplicamos Gauss-Jordan
    matriz_rref = gauss_jordan(matriz_original)

    num_compuestos = len(compuestos)

    # Extraemos los coeficientes decimales
    coeficientes_float = extraer_coeficientes(
        matriz_rref,
        num_compuestos
    )

    # Convertimos los coeficientes a enteros
    coeficientes_enteros = racionalizar_coeficientes(
        coeficientes_float
    )

    # Devolvemos toda la información necesaria
    return (
        coeficientes_enteros,
        compuestos,
        matriz_original,
        matriz_rref,
        elementos
    )



# Esta función imprime la matriz de forma organizada
def imprimir_matriz(
    matriz,
    elementos,
    compuestos,
    titulo="Matriz"
):

    ancho_col = 10

    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    # Creamos el encabezado con los compuestos
    encabezado = f"{'Elem':>6} |"

    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"

    print(encabezado)

    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    # Recorremos cada fila de la matriz
    for i, elemento in enumerate(elementos):

        fila_str = f"{elemento:>6} |"

        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"

        print(fila_str)

    print(f"{'='*60}\n")

    # Devolvemos la matriz mostrada
    return matriz
