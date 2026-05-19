# Función realizada por Julian Ruiz

"""
En este módulo verificamos visualmente el balanceo
de una ecuación química contando los átomos de cada
elemento antes y después del balanceo.

La idea es comparar ambos lados de la ecuación
para demostrar si realmente quedó balanceada.

Aquí se generan los conteos necesarios para luego
mostrar tablas comparativas en la interfaz.
"""

from traductor import conocer_cantidad_moles


# Esta función cuenta los átomos presentes
# en un lado de la ecuación química
def contar_atomos_lado(compuestos, coeficientes):

    conteo = {}

    # Recorremos cada compuesto junto con su coeficiente
    for comp, coef in zip(compuestos, coeficientes):

        # Obtenemos los elementos y cantidades del compuesto
        atomos = conocer_cantidad_moles(comp)

        # Multiplicamos cada cantidad de átomos
        # por el coeficiente correspondiente
        for elemento, cantidad in atomos.items():

            conteo[elemento] = (
                conteo.get(elemento, 0) +
                cantidad * coef
            )

    # Devolvemos el conteo total de átomos
    return conteo


# Esta función organiza toda la información
# necesaria para verificar el balanceo
def tabla_verificacion(
    reactivos,
    productos,
    coeficientes,
    compuestos
):

    # Guardamos cuántos reactivos hay
    n_reactivos = len(reactivos)

    # Separamos los coeficientes
    # de reactivos y productos
    coef_react_bal = coeficientes[:n_reactivos]

    coef_prod_bal = coeficientes[n_reactivos:]

    # Antes del balanceo todos los coeficientes
    # se consideran iguales a 1
    antes_react = contar_atomos_lado(
        reactivos,
        [1] * n_reactivos
    )

    antes_prod = contar_atomos_lado(
        productos,
        [1] * len(productos)
    )

    # Después del balanceo usamos
    # los coeficientes calculados
    desp_react = contar_atomos_lado(
        reactivos,
        coef_react_bal
    )

    desp_prod = contar_atomos_lado(
        productos,
        coef_prod_bal
    )

    # Unimos todos los elementos encontrados
    # y los organizamos alfabéticamente
    elementos = sorted(
        set(antes_react) |
        set(antes_prod)
    )

    # Devolvemos toda la información organizada
    return {

        "antes_reactivos": antes_react,

        "antes_productos": antes_prod,

        "despues_reactivos": desp_react,

        "despues_productos": desp_prod,

        "elementos": elementos,
    }
