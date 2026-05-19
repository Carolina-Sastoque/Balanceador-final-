# Función realizada por Lizeth Sastoque

"""
En este módulo guardamos información sobre los diferentes tipos
de reacciones químicas. La idea es que el usuario pueda entender
qué significa cada reacción, cómo identificarla y ver ejemplos
de la vida real de una forma más sencilla.
"""


# Creamos un diccionario donde almacenamos toda la información
# de cada tipo de reacción química
EXPLICACIONES = {

    "Combustion": {

        # Nombre completo que se mostrará al usuario
        "nombre_completo": "Reacción de Combustión",

        # Ícono para hacer más visual la explicación
        "icono": "🔥",

        # Explicación sencilla de lo que ocurre en la reacción
        "descripcion": (
            "Una sustancia (generalmente un hidrocarburo) reacciona con oxígeno (O₂) "
            "y produce dióxido de carbono (CO₂) y agua (H₂O). "
            "Libera una gran cantidad de energía en forma de calor y luz."
        ),

        # Aquí explicamos cómo reconocer este tipo de reacción
        "como_identificarla": (
            "Busca que uno de los reactivos sea O₂, y que entre los productos "
            "aparezcan tanto CO₂ como H₂O. Si se cumplen esas tres condiciones, "
            "es una combustión."
        ),

        # Ejemplo típico de combustión
        "ejemplo": "CH₄ + 2O₂ → CO₂ + 2H₂O  (combustión del metano, el gas de cocina)",

        # Dato curioso relacionado con este tipo de reacción
        "curiosidad": (
            "La combustión que usas todos los días: motores de carros, cocinas a gas "
            "e incluso la respiración celular siguen este mismo principio."
        ),
    },

    "Sintesis": {

        # Información de las reacciones donde varias sustancias forman una sola
        "nombre_completo": "Reacción de Síntesis (o Combinación)",

        "icono": "🔗",

        "descripcion": (
            "Dos o más sustancias simples se unen para formar una sola más compleja. "
            "Es como construir una molécula nueva a partir de piezas más pequeñas."
        ),

        "como_identificarla": (
            "Hay más reactivos que productos. El patrón típico es: A + B → AB. "
            "Si ves que 'se juntan cosas' para hacer algo nuevo, es síntesis."
        ),

        "ejemplo": "2H₂ + O₂ → 2H₂O  (síntesis del agua)",

        "curiosidad": (
            "La síntesis de amoniaco (N₂ + 3H₂ → 2NH₃) es una de las reacciones "
            "más importantes de la historia: permitió fabricar fertilizantes y "
            "alimentar a miles de millones de personas."
        ),
    },

    "Descomposicion": {

        # Este tipo de reacción ocurre cuando un compuesto se divide
        "nombre_completo": "Reacción de Descomposición",

        "icono": "💥",

        "descripcion": (
            "Una sola sustancia compleja se rompe en dos o más sustancias más simples. "
            "Es el proceso contrario a la síntesis."
        ),

        "como_identificarla": (
            "Hay más productos que reactivos. El patrón típico es: AB → A + B. "
            "Si ves que 'algo se parte', es descomposición."
        ),

        "ejemplo": "2H₂O → 2H₂ + O₂  (electrólisis del agua)",

        "curiosidad": (
            "El agua oxigenada (H₂O₂) que usas para limpiar heridas se descompone "
            "espontáneamente en agua y oxígeno cuando toca la sangre, "
            "por eso hace espuma."
        ),
    },

    "Sustitucion simple": {

        # Aquí un elemento reemplaza a otro dentro de un compuesto
        "nombre_completo": "Reacción de Sustitución Simple (o Desplazamiento)",

        "icono": "🔄",

        "descripcion": (
            "Un elemento libre 'empuja' a otro que estaba dentro de un compuesto "
            "y ocupa su lugar. El elemento desplazado queda libre."
        ),

        "como_identificarla": (
            "Uno de los reactivos es un elemento puro y el otro es un compuesto. "
            "En los productos hay un nuevo compuesto y un elemento libre diferente. "
            "Patrón: A + BC → AC + B."
        ),

        "ejemplo": "Zn + 2HCl → ZnCl₂ + H₂  (zinc desplaza al hidrógeno del ácido)",

        "curiosidad": (
            "Esta reacción explica por qué algunos metales corroen más rápido que "
            "otros en presencia de ácidos. Tiene que ver con la 'reactividad' "
            "o posición en la serie electroquímica."
        ),
    },

    "Doble sustitucion": {

        # En este caso dos compuestos intercambian sus componentes
        "nombre_completo": "Reacción de Doble Sustitución (o Metátesis)",

        "icono": "🔀",

        "descripcion": (
            "Dos compuestos intercambian sus 'partes'. Es como si dos parejas "
            "se intercambiaran compañeros de baile al mismo tiempo."
        ),

        "como_identificarla": (
            "Hay exactamente 2 reactivos y 2 productos, y todos son compuestos "
            "(ninguno es un elemento puro). Patrón: AB + CD → AD + CB."
        ),

        "ejemplo": "AgNO₃ + NaCl → AgCl + NaNO₃  (precipitación del cloruro de plata)",

        "curiosidad": (
            "Muchas reacciones de precipitación, neutralización ácido-base y "
            "formación de gases caen en esta categoría. Son muy comunes en "
            "análisis químico de laboratorio."
        ),
    },

    "Desconocida": {

        # Esta opción se usa cuando el programa no logra clasificar la reacción
        "nombre_completo": "Tipo de Reacción No Determinado",

        "icono": "❓",

        "descripcion": (
            "No fue posible clasificar esta reacción en las categorías básicas. "
            "Puede ser una reacción redox, de precipitación especial, "
            "orgánica compleja, u otro tipo no cubierto por el clasificador."
        ),

        "como_identificarla": (
            "Para identificar reacciones más complejas se necesita analizar "
            "los estados de oxidación de los elementos (reacciones redox) "
            "o revisar las propiedades de los productos."
        ),

        "ejemplo": "Muchas reacciones de oxidación-reducción no encajan en los tipos básicos.",

        "curiosidad": (
            "La química tiene docenas de tipos de reacciones especializadas. "
            "Las 5 categorías básicas son solo el punto de partida."
        ),
    },
}


# Esta función busca la información del tipo de reacción solicitado
def obtener_explicacion(tipo_reaccion):

    # Buscamos el tipo de reacción dentro del diccionario
    # Si no existe devolvemos automáticamente la opción "Desconocida"
    return EXPLICACIONES.get(
        tipo_reaccion,
        EXPLICACIONES["Desconocida"]
    )
