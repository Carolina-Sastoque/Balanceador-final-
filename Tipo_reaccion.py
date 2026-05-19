# Función realizada por Julian Ruiz
#
# En este módulo se encuentran todas las funciones encargadas
# de identificar y clasificar los diferentes tipos de reacciones químicas.
#
# Aquí se revisa si una reacción corresponde a:
# combustión, síntesis, descomposición,
# sustitución simple o doble sustitución.
#
# También se usan funciones auxiliares para analizar
# los compuestos y determinar sus características.

from traductor import conocer_cantidad_moles, Separar_ecuacion


# Esta función obtiene todos los elementos presentes
# dentro de un compuesto químico
def contar_elementos(compuesto):

    return set(conocer_cantidad_moles(compuesto).keys())


# Esta función revisa si una sustancia está formada
# por un solo elemento químico
def es_elemento_puro(compuesto):

    return len(contar_elementos(compuesto)) == 1


# Esta función verifica si una sustancia tiene
# más de un elemento y por lo tanto es un compuesto
def es_compuesto(compuesto):

    return len(contar_elementos(compuesto)) > 1


# Aquí verificamos si el compuesto es un hidrocarburo,
# es decir, si solamente contiene carbono e hidrógeno
def es_hidrocarburo(compuesto):

    elems = contar_elementos(compuesto)
    return elems.issubset({"C", "H"}) and "C" in elems


# Esta función revisa si dentro de los reactivos
# aparece oxígeno molecular (O2)
def contiene_oxigeno_molecular(lista):

    return "O2" in lista


# Esta función analiza si la reacción corresponde
# a una combustión
def es_combustion(reactivos, productos):

    # Primero verificamos que exista O2 en los reactivos
    if not contiene_oxigeno_molecular(reactivos):
        return False

    # Revisamos si alguno de los reactivos es un hidrocarburo
    hidrocarburo = any(es_hidrocarburo(r) for r in reactivos)

    # También comprobamos que se formen CO2 y H2O
    produce_CO2 = any("CO2" in p for p in productos)
    produce_H2O = any("H2O" in p for p in productos)

    return hidrocarburo and produce_CO2 and produce_H2O


# Esta función identifica reacciones de síntesis,
# donde varias sustancias forman una más compleja
def es_sintesis(reactivos, productos):

    return len(reactivos) > len(productos)


# Esta función revisa si la reacción es de descomposición,
# es decir, cuando un compuesto se separa en sustancias más simples
def es_descomposicion(reactivos, productos):

    return len(reactivos) < len(productos)


# Aquí identificamos reacciones de sustitución simple,
# donde un elemento reemplaza a otro dentro de un compuesto
def es_sustitucion_simple(reactivos, productos):

    react_elemento = any(es_elemento_puro(r) for r in reactivos)
    react_compuesto = any(es_compuesto(r) for r in reactivos)

    prod_elemento = any(es_elemento_puro(p) for p in productos)
    prod_compuesto = any(es_compuesto(p) for p in productos)

    return react_elemento and react_compuesto and prod_elemento and prod_compuesto


# Esta función revisa si la reacción corresponde
# a una doble sustitución
def es_doble_sustitucion(reactivos, productos):

    # Para este tipo deben existir exactamente
    # dos reactivos y dos productos
    if len(reactivos) != 2 or len(productos) != 2:
        return False

    # También verificamos que todas las sustancias
    # sean compuestos
    return all(es_compuesto(x) for x in reactivos + productos)


# Función principal encargada de clasificar la reacción química
def clasificar_reaccion(ecuacion):

    # Primero separamos la ecuación en reactivos y productos
    reactivos, productos = Separar_ecuacion(ecuacion)

    # Se revisa cada tipo de reacción hasta encontrar coincidencia
    if es_combustion(reactivos, productos):
        return "Combustion"

    if es_sintesis(reactivos, productos):
        return "Sintesis"

    if es_descomposicion(reactivos, productos):
        return "Descomposicion"

    if es_sustitucion_simple(reactivos, productos):
        return "Sustitucion simple"

    if es_doble_sustitucion(reactivos, productos):
        return "Doble sustitucion"

    # Si no coincide con ningún caso conocido,
    # se devuelve como desconocida
    return "Desconocida"
