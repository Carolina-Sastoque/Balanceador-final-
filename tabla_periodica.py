# Función realizada por Lizeth Sastoque

"""
En este módulo guardamos la información de varios elementos
de la tabla periódica y permitimos buscarlos fácilmente
por símbolo o por nombre.

También usamos funciones auxiliares para mostrar colores
según la categoría de cada elemento dentro de la interfaz.
"""


# Aquí guardamos la información principal de cada elemento
# La clave principal es el símbolo químico
TABLA_PERIODICA = {

    "H": {
        "numero": 1,
        "nombre": "Hidrógeno",
        "masa": 1.008,
        "grupo": 1,
        "periodo": 1,
        "categoria": "No metal"
    },

    "He": {
        "numero": 2,
        "nombre": "Helio",
        "masa": 4.003,
        "grupo": 18,
        "periodo": 1,
        "categoria": "Gas noble"
    },

    "Li": {
        "numero": 3,
        "nombre": "Litio",
        "masa": 6.941,
        "grupo": 1,
        "periodo": 2,
        "categoria": "Metal alcalino"
    },

    "Be": {
        "numero": 4,
        "nombre": "Berilio",
        "masa": 9.012,
        "grupo": 2,
        "periodo": 2,
        "categoria": "Metal alcalinotérreo"
    },

    "B": {
        "numero": 5,
        "nombre": "Boro",
        "masa": 10.811,
        "grupo": 13,
        "periodo": 2,
        "categoria": "Metaloide"
    },

    "C": {
        "numero": 6,
        "nombre": "Carbono",
        "masa": 12.011,
        "grupo": 14,
        "periodo": 2,
        "categoria": "No metal"
    },

    # ...
    # El resto de elementos continúan con exactamente la misma estructura
}


# Aquí creamos un diccionario para buscar elementos usando su nombre
# Por ejemplo: "hierro" → "Fe"
NOMBRES_A_SIMBOLO = {

    info["nombre"].lower(): simbolo
    for simbolo, info in TABLA_PERIODICA.items()
}


# También agregamos nombres alternativos y nombres en inglés
# Esto hace la búsqueda mucho más flexible para el usuario
NOMBRES_ALTERNATIVOS = {

    "hydrogen": "H",
    "carbon": "C",
    "oxygen": "O",
    "nitrogen": "N",

    "iron": "Fe",
    "gold": "Au",
    "silver": "Ag",
    "copper": "Cu",

    "lead": "Pb",
    "sodium": "Na",
    "potassium": "K",
    "calcium": "Ca",

    "chlorine": "Cl",
    "sulfur": "S",
    "phosphorus": "P",

    "zinc": "Zn",
    "mercury": "Hg",
    "tin": "Sn",

    "azufre": "S",
    "hierro": "Fe",
    "sodio": "Na",

    "potasio": "K",
    "calcio": "Ca",
    "cloro": "Cl",

    "plomo": "Pb",
    "mercurio": "Hg",
    "plata": "Ag",

    "oro": "Au",
    "cobre": "Cu",
    "zinc": "Zn",

    "estano": "Sn",
    "yodo": "I",
    "fosforo": "P",

    "wolframio": "W",
    "uranio": "U",
    "hidrogeno": "H",

    "nitrogeno": "N",
    "oxigeno": "O",
    "carbono": "C",

    "fluor": "F",
    "bromo": "Br",
    "silicio": "Si",
}


# Esta función busca un elemento usando símbolo o nombre
def buscar_elemento(texto):

    # Primero quitamos espacios sobrantes
    texto_limpio = texto.strip()

    # Intentamos buscar directamente usando el símbolo químico
    if texto_limpio in TABLA_PERIODICA:

        return {
            "simbolo": texto_limpio,
            **TABLA_PERIODICA[texto_limpio]
        }

    # También probamos colocando la primera letra en mayúscula
    texto_cap = texto_limpio.capitalize()

    if texto_cap in TABLA_PERIODICA:

        return {
            "simbolo": texto_cap,
            **TABLA_PERIODICA[texto_cap]
        }

    # Ahora buscamos usando el nombre del elemento
    texto_lower = texto_limpio.lower()

    if texto_lower in NOMBRES_A_SIMBOLO:

        simbolo = NOMBRES_A_SIMBOLO[texto_lower]

        return {
            "simbolo": simbolo,
            **TABLA_PERIODICA[simbolo]
        }

    # Finalmente revisamos los nombres alternativos o en inglés
    if texto_lower in NOMBRES_ALTERNATIVOS:

        simbolo = NOMBRES_ALTERNATIVOS[texto_lower]

        return {
            "simbolo": simbolo,
            **TABLA_PERIODICA[simbolo]
        }

    # Si no encontramos coincidencias devolvemos None
    return None


# Esta función devuelve un color según la categoría del elemento
# Se usa principalmente para darle estilo visual en Streamlit
def obtener_color_categoria(categoria):

    colores = {

        "No metal": "#4CAF50",

        "Metal": "#2196F3",

        "Metal alcalino": "#FF5722",

        "Metal alcalinotérreo": "#FF9800",

        "Metal de transición": "#9C27B0",

        "Metaloide": "#795548",

        "Halógeno": "#00BCD4",

        "Gas noble": "#607D8B",

        "Lantánido": "#E91E63",

        "Actínido": "#F44336",
    }

    # Si la categoría no existe devolvemos un gris por defecto
    return colores.get(categoria, "#9E9E9E")
