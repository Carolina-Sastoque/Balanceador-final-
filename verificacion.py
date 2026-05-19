# Función realizada por Lizeth Sastoque
"""
En este módulo verificamos si una ecuación química
ya está balanceada antes de intentar resolverla.
También validamos que los elementos estén escritos
con mayúscula inicial, porque si alguien escribe h2o
el traductor no reconoce nada y da resultados incorrectos.
Aquí usamos funciones del módulo traductor
para separar la ecuación y contar los átomos
presentes en cada compuesto.
"""
from traductor import Separar_ecuacion, conocer_cantidad_moles


# Esta función revisa que cada elemento del compuesto
# empiece con mayúscula, por ejemplo H2O está bien
# pero h2o no, porque el traductor no lo reconoce
# y devuelve un diccionario vacío sin avisar nada
def validar_mayusculas(compuesto):
    i = 0
    while i < len(compuesto):
        letra = compuesto[i]

        if letra.isalpha():
            # El inicio de todo símbolo químico debe ser mayúscula
            # si encontramos una minúscula aquí, le avisamos al usuario
            if letra.islower():
                raise ValueError(
                    f"'{compuesto}' contiene '{letra}' en minúscula. "
                    f"Los elementos deben comenzar con mayúscula "
                    f"(por ejemplo: H2O, CO2, NaOH)."
                )
            i += 1
            # Saltamos la segunda letra del símbolo si es minúscula
            # por ejemplo en Na, Cl, Fe la segunda letra va en minúscula
            if i < len(compuesto) and compuesto[i].islower():
                i += 1
        else:
            i += 1


# Esta función cuenta todos los átomos presentes
# en un lado de la ecuación teniendo en cuenta
# los coeficientes de cada compuesto
def _contar_atomos(compuestos, coeficientes):
    conteo = {}
    # Recorremos cada compuesto junto con su coeficiente
    for comp, coef in zip(compuestos, coeficientes):
        # Obtenemos los elementos y cantidades del compuesto
        for elemento, cantidad in conocer_cantidad_moles(comp).items():
            # Multiplicamos la cantidad de átomos
            # por el coeficiente correspondiente
            conteo[elemento] = (
                conteo.get(elemento, 0) +
                cantidad * coef
            )
    # Devolvemos el conteo total de átomos
    return conteo


# Esta función revisa si la ecuación escrita
# por el usuario ya está balanceada
def ecuacion_ya_balanceada(ecuacion: str) -> tuple:
    # Separamos reactivos y productos
    reactivos, productos = Separar_ecuacion(ecuacion)

    # Validamos que todos los compuestos usen mayúsculas correctamente
    # si algo falla, el error llega al main y se muestra con st.error
    for comp in reactivos + productos:
        validar_mayusculas(comp)

    # Contamos los átomos de los reactivos
    # usando coeficiente 1 para todos
    atomos_r = _contar_atomos(
        reactivos,
        [1] * len(reactivos)
    )
    # Contamos los átomos de los productos
    atomos_p = _contar_atomos(
        productos,
        [1] * len(productos)
    )
    # Unimos todos los elementos presentes
    # en ambos lados de la ecuación
    elementos = set(atomos_r.keys()) | set(atomos_p.keys())

    detalle = {}
    # Suponemos inicialmente que sí está balanceada
    balanceada = True

    # Revisamos elemento por elemento
    for elem in sorted(elementos):
        cant_r = atomos_r.get(elem, 0)
        cant_p = atomos_p.get(elem, 0)
        # Verificamos si coinciden
        coincide = cant_r == cant_p
        # Si algún elemento no coincide
        # entonces la ecuación no está balanceada
        if not coincide:
            balanceada = False
        # Guardamos el detalle del análisis
        detalle[elem] = {
            "reactivos": cant_r,
            "productos": cant_p,
            "ok": coincide
        }
    # Devolvemos:
    # True/False dependiendo del balance
    # y el detalle completo de cada elemento
    return balanceada, detalle
