# Función realizada por Lizeth Sastoque

"""
En este módulo mostramos paso a paso cómo se balancea una ecuación química
utilizando el método algebraico y Gauss-Jordan. La idea es que el usuario
no solo vea el resultado final, sino que también entienda el procedimiento.
"""

from traductor import Separar_ecuacion, conocer_cantidad_moles
from matrices import construir_matriz, gauss_jordan, extraer_coeficientes, racionalizar_coeficientes


# Esta función se usa para mostrar los números de forma más limpia
# Por ejemplo, si el número es 2.0 se mostrará solamente como 2
def _fmt(n):
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:.4f}"


# Aquí volvemos a construir la ecuación química usando los coeficientes obtenidos
# Si el coeficiente es 1 no se escribe, porque así se manejan normalmente las ecuaciones químicas
def _escribir_ecuacion(compuestos, coeficientes, num_reactivos):

    lado_r, lado_p = [], []

    # Recorremos todos los compuestos para organizarlos en reactivos y productos
    for i, comp in enumerate(compuestos):

        coef = coeficientes[i]

        # Si el coeficiente es 1 no agregamos nada antes del compuesto
        prefijo = "" if coef == 1 else str(coef)

        termino = f"{prefijo}{comp}"

        # Dependiendo de la posición lo agregamos al lado de reactivos o productos
        if i < num_reactivos:
            lado_r.append(termino)
        else:
            lado_p.append(termino)

    # Finalmente devolvemos la ecuación completa en formato texto
    return " + ".join(lado_r) + " = " + " + ".join(lado_p)


# Esta función organiza la matriz en forma de tabla para que sea más fácil de leer
def _tabla_matriz(mat, elementos, compuestos):

    ancho = 10
    lineas = []

    # Creamos la cabecera con los nombres de los compuestos
    cab = f"{'':8s}|"

    for comp in compuestos:
        cab += f"{comp:>{ancho}}"

    lineas.append(cab)
    lineas.append("-" * (9 + ancho * len(compuestos)))

    # Recorremos cada elemento y sus valores dentro de la matriz
    for i, elem in enumerate(elementos):

        fila = f"{elem:>7s} |"

        for val in mat[i]:
            fila += f"{_fmt(val):>{ancho}}"

        lineas.append(fila)

    # Unimos todas las líneas para formar la tabla completa
    return "\n".join(lineas)


# Aquí realizamos el método de Gauss-Jordan guardando cada operación
# para poder mostrar el procedimiento paso a paso
def _gauss_jordan_con_pasos(matriz_in, elementos, compuestos):

    # Creamos una copia de la matriz para no modificar la original
    mat = [fila[:] for fila in matriz_in]

    n_f = len(mat)
    n_c = len(mat[0]) if mat else 0

    # En esta lista iremos guardando todas las operaciones realizadas
    ops = []

    # Esta función toma una "foto" de cómo queda la matriz en cada paso
    def snap():
        return _tabla_matriz(mat, elementos, compuestos)

    fila_pivote = 0

    # Recorremos cada columna de la matriz
    for col in range(n_c):

        # Buscamos una fila que tenga un valor diferente de cero
        fila_nz = None

        for f in range(fila_pivote, n_f):
            if abs(mat[f][col]) > 1e-9:
                fila_nz = f
                break

        # Si toda la columna es cero simplemente seguimos con la siguiente
        if fila_nz is None:
            continue

        # Si es necesario intercambiamos filas para subir el pivote
        if fila_nz != fila_pivote:

            mat[fila_pivote], mat[fila_nz] = mat[fila_nz], mat[fila_pivote]

            ops.append((
                f"F{fila_pivote+1} ↔ F{fila_nz+1}",
                snap()
            ))

        # Tomamos el valor pivote de la fila actual
        pivote = mat[fila_pivote][col]

        # Dividimos toda la fila para convertir el pivote en 1
        if abs(pivote - 1.0) > 1e-9:

            mat[fila_pivote] = [x / pivote for x in mat[fila_pivote]]

            ops.append((
                f"F{fila_pivote+1} ÷ {_fmt(pivote)}",
                snap()
            ))

        # Ahora hacemos ceros arriba y abajo del pivote
        for f in range(n_f):

            if f == fila_pivote:
                continue

            factor = mat[f][col]

            # Si ya es cero no hace falta modificar la fila
            if abs(factor) < 1e-9:
                continue

            mat[f] = [
                mat[f][j] - factor * mat[fila_pivote][j]
                for j in range(n_c)
            ]

            signo = f"- {_fmt(abs(factor))}" if factor > 0 else f"+ {_fmt(abs(factor))}"

            ops.append((
                f"F{f+1} = F{f+1} {signo}·F{fila_pivote+1}",
                snap()
            ))

        # Pasamos a la siguiente fila pivote
        fila_pivote += 1

    # Devolvemos todas las operaciones registradas
    return ops


# Esta es la función principal del módulo
# Recibe la ecuación química y genera toda la explicación paso a paso
def explicar_balanceo(ecuacion: str) -> list:

    pasos = []
    SEP = "---"

    # Usamos letras para representar las incógnitas de cada compuesto
    letras = list("abcdefghijklmnopqrstuvwxyz")


    # Separamos reactivos y productos de la ecuación
    reactivos, productos = Separar_ecuacion(ecuacion)

    num_reactivos = len(reactivos)

    # Unimos todos los compuestos en una sola lista
    compuestos_todos = reactivos + productos


    # Construimos la matriz del sistema de ecuaciones
    matriz_orig, elementos, compuestos = construir_matriz(reactivos, productos)

    num_compuestos = len(compuestos)


    # Aquí iremos guardando las ecuaciones en forma simbólica
    ecuaciones_escritas = []

    # Recorremos cada elemento químico
    for i, elem in enumerate(elementos):

        terminos = []

        # Recorremos los compuestos para construir la ecuación
        for j in range(num_compuestos):

            val = matriz_orig[i][j]

            if abs(val) < 1e-9:
                continue

            var = letras[j] if j < len(letras) else f"x{j}"

            coef = _fmt(abs(val))

            signo = "+" if val > 0 else "−"

            parte = var if coef == "1" else f"{coef}{var}"

            terminos.append(f"{signo} {parte}")

        expr = " ".join(terminos).lstrip("+ ").strip()

        ecuaciones_escritas.append(f"- **{elem}:** &nbsp; {expr} = 0")


    # Aplicamos Gauss-Jordan mostrando cada operación
    operaciones = _gauss_jordan_con_pasos(matriz_orig, elementos, compuestos)


    # Reducimos la matriz para obtener la solución final
    matriz_rref = gauss_jordan(matriz_orig)

    # Extraemos los coeficientes encontrados
    coef_float = extraer_coeficientes(matriz_rref, num_compuestos)


    # Convertimos los coeficientes a enteros
    coef_enteros = racionalizar_coeficientes(coef_float)

    # Construimos la ecuación ya balanceada
    ecuacion_balanceada = _escribir_ecuacion(
        compuestos,
        coef_enteros,
        num_reactivos
    )

    # Finalmente devolvemos todos los pasos generados
    return pasos
