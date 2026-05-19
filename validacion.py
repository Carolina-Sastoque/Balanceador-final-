# Función realizada por Lizeth Sastoque

# Este módulo se encarga de validar la ecuación química
# antes de que el programa intente balancearla.
#
# Aquí se revisa que:
# - Los símbolos químicos existan realmente
# - Los paréntesis estén correctamente escritos
# - La ecuación tenga una estructura válida
#
# Todo esto ayuda a evitar errores durante los cálculos.


import re


# Aquí guardamos todos los símbolos válidos
# de la tabla periódica
ELEMENTOS_VALIDOS = [
    "He", "Li", "Be", "Ne", "Na", "Mg", "Al", "Si", "Cl", "Ar",
    "Ca", "Sc", "Ti", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Zr", "Nb",
    "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
    "Te", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
    "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",
    "Ta", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
    "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "Np", "Pu",
    "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",

    # Los elementos de una sola letra van al final
    # para evitar confusiones al leer símbolos dobles
    "H", "B", "C", "N", "O", "F", "P", "S", "K", "V", "Y", "I",
    "W", "U",
]


# Convertimos la lista en set para que las búsquedas
# sean más rápidas
SET_ELEMENTOS = set(ELEMENTOS_VALIDOS)


# Esta función revisa que los paréntesis
# estén correctamente abiertos y cerrados
def _validar_parentesis(formula):

    # Este contador aumenta cuando aparece "("
    # y disminuye cuando aparece ")"
    contador = 0

    for i, caracter in enumerate(formula):

        if caracter == "(":
            contador += 1

        elif caracter == ")":
            contador -= 1

            # Si el contador baja de cero,
            # significa que se cerró un paréntesis
            # que nunca se abrió
            if contador < 0:

                return (
                    False,
                    f"Paréntesis ')' en posición {i+1} sin un '(' que lo abra."
                )

    # Si al final todavía quedan abiertos,
    # significa que faltó cerrarlos
    if contador > 0:

        return False, "Hay un '(' que nunca se cerró con ')'."

    return True, ""


# Esta función extrae los símbolos químicos
# presentes en una fórmula
def _extraer_simbolos(formula):

    simbolos = []
    i = 0

    while i < len(formula):

        letra = formula[i]

        # Todos los símbolos químicos empiezan
        # con letra mayúscula
        if letra.isupper():

            simbolo = letra
            i += 1

            # Si después hay minúsculas,
            # también pertenecen al símbolo
            while i < len(formula) and formula[i].islower():

                simbolo += formula[i]
                i += 1

            simbolos.append(simbolo)

        else:

            # Saltamos números, paréntesis
            # y otros caracteres
            i += 1

    return simbolos


# Esta función revisa que todos los símbolos
# encontrados existan en la tabla periódica
def _validar_simbolos(formula):

    simbolos = _extraer_simbolos(formula)

    invalidos = []

    for s in simbolos:

        if s not in SET_ELEMENTOS:

            invalidos.append(s)

    # Si encontramos símbolos inválidos,
    # los mostramos en el mensaje de error
    if invalidos:

        # Eliminamos repetidos para que el mensaje
        # no se vea desordenado
        invalidos_unicos = list(dict.fromkeys(invalidos))

        return (
            False,
            f"Símbolo(s) no reconocido(s): "
            f"{', '.join(invalidos_unicos)}. "
            f"Verifica que estén bien escritos."
        )

    return True, ""


# Esta función revisa que la ecuación tenga
# una estructura válida
def _validar_estructura_ecuacion(ecuacion):

    # Eliminamos espacios para analizar mejor
    ecuacion_limpia = ecuacion.replace(" ", "")

    # La ecuación debe tener un solo "="
    partes = ecuacion_limpia.split("=")

    if len(partes) != 2:

        return (
            False,
            "La ecuación debe tener exactamente un signo '=' "
            "separando reactivos y productos."
        )

    reactivos_str, productos_str = partes

    # Revisamos que ambos lados tengan contenido
    if not reactivos_str:

        return False, "No hay reactivos antes del '='."

    if not productos_str:

        return False, "No hay productos después del '='."

    # Separamos cada compuesto usando "+"
    reactivos = reactivos_str.split("+")
    productos = productos_str.split("+")

    # Revisamos que no existan espacios vacíos
    # por errores como "H2++O2"
    for r in reactivos:

        if not r:

            return False, "Hay un '+' extra o mal puesto en los reactivos."

    for p in productos:

        if not p:

            return False, "Hay un '+' extra o mal puesto en los productos."

    return True, ""


# Función principal encargada de validar
# completamente la ecuación química
def validar_ecuacion(ecuacion):

    errores = []

    # Primero revisamos la estructura general
    ok, msg = _validar_estructura_ecuacion(ecuacion)

    # Si la estructura ya está mal,
    # no tiene sentido seguir revisando
    if not ok:

        return False, [msg]

    # Eliminamos espacios y separamos
    # todos los compuestos
    limpia = ecuacion.replace(" ", "")

    partes = limpia.split("=")

    todos_compuestos = (
        partes[0].split("+") + partes[1].split("+")
    )

    # Revisamos los paréntesis de cada compuesto
    for comp in todos_compuestos:

        ok, msg = _validar_parentesis(comp)

        if not ok:

            errores.append(f"Error en '{comp}': {msg}")

    # Revisamos que todos los símbolos
    # correspondan a elementos reales
    for comp in todos_compuestos:

        ok, msg = _validar_simbolos(comp)

        if not ok:

            errores.append(f"Error en '{comp}': {msg}")

    # Si hubo errores devolvemos la lista
    if errores:

        return False, errores

    # Si todo salió bien, la ecuación es válida
    return True, []
