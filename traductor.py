# Función realizada por Karen González
#
# Este módulo se encarga de interpretar la ecuación química
# que escribe el usuario para convertirla en información
# que el programa pueda utilizar en los cálculos.
#
# Aquí se separan los reactivos y productos,
# y también se cuentan los átomos de cada elemento
# dentro de los compuestos químicos.


# Esta función separa la ecuación en reactivos y productos
def Separar_ecuacion(cadena):

    # Primero eliminamos los espacios que pueda escribir el usuario
    cadena = cadena.replace(" ", "")

    # Separamos la ecuación usando el símbolo "="
    lista_compuestos = cadena.split("=")

    # A la izquierda del "=" quedan los reactivos
    reactivos = lista_compuestos[0].split("+")

    # A la derecha del "=" quedan los productos
    productos = lista_compuestos[1].split("+")

    # Finalmente devolvemos ambas listas
    return reactivos, productos


# Esta función cuenta la cantidad de átomos
# que tiene cada elemento dentro de un compuesto
def conocer_cantidad_moles(sustancia):

    # Aquí guardaremos el resultado final
    dict_elementos = {}

    # Este diccionario temporal se usa cuando aparecen paréntesis
    dict_temporal_parentesis = {}

    # Esta variable ayuda a saber si estamos
    # dentro o fuera de un paréntesis
    parentesis = "Fuera"

    # Contador para recorrer el string carácter por carácter
    i = 0

    while i < len(sustancia):

        # Tomamos la letra actual
        letra = sustancia[i]

        # Si encontramos un paréntesis de apertura
        # significa que empieza un grupo especial
        if letra == "(":

            parentesis = "Dentro"

            # Reiniciamos el diccionario temporal
            dict_temporal_parentesis = {}

            i += 1

        # Si encontramos el cierre del paréntesis
        elif letra == ")":

            parentesis = "Fuera"
            i += 1

            # Después del paréntesis puede venir
            # un número multiplicador
            num = ""

            while i < len(sustancia) and sustancia[i].isdigit():

                num += sustancia[i]
                i += 1

            # Si no aparece número, el multiplicador vale 1
            if num:
                multiplicador = int(num)
            else:
                multiplicador = 1

            # Multiplicamos todos los elementos que estaban
            # dentro del paréntesis
            for elemento, cantidad in dict_temporal_parentesis.items():

                dict_elementos[elemento] = (
                    dict_elementos.get(elemento, 0)
                    + cantidad * multiplicador
                )

        # Aquí identificamos los símbolos químicos
        # que siempre empiezan con mayúscula
        elif letra.isupper():

            elemento = letra
            i += 1

            # Si la siguiente letra es minúscula,
            # también pertenece al símbolo
            while i < len(sustancia) and sustancia[i].islower():

                elemento += sustancia[i]
                i += 1

            # Ahora buscamos si el elemento tiene subíndice
            num = ""

            while i < len(sustancia) and sustancia[i].isdigit():

                num += sustancia[i]
                i += 1

            # Si no tiene número, significa que vale 1
            if num:
                cantidad = int(num)
            else:
                cantidad = 1

            # Dependiendo de si estamos dentro o fuera
            # del paréntesis, guardamos el elemento
            # en el diccionario correspondiente
            if parentesis == "Dentro":

                dict_temporal_parentesis[elemento] = (
                    dict_temporal_parentesis.get(elemento, 0)
                    + cantidad
                )

            elif parentesis == "Fuera":

                dict_elementos[elemento] = (
                    dict_elementos.get(elemento, 0)
                    + cantidad
                )

        # Si aparece otro carácter simplemente avanzamos
        # para evitar ciclos infinitos
        else:

            i += 1

    # Devolvemos un diccionario con cada elemento
    # y la cantidad de átomos encontrados
    return dict_elementos
