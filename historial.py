# Función realizada por Lizeth Sastoque
"""
En este módulo manejamos el historial de ecuaciones balanceadas.
Aquí guardamos las operaciones realizadas por el usuario, mostramos
el historial almacenado y también permitimos exportarlo.
Ahora se puede descargar en formato TXT o PDF directamente
desde el navegador, sin que el archivo quede guardado en el servidor.
"""
from datetime import datetime
from fpdf import FPDF

# Nombre del archivo donde se guarda el historial en el servidor
ARCHIVO_HISTORIAL = "historial.txt"


# Esta función guarda cada ecuación procesada por el usuario
def guardar_en_historial(ecuacion, balanceada, tipo):
    # Abrimos el archivo en modo append para agregar información
    # sin borrar lo que ya estaba guardado anteriormente
    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
        # Guardamos la ecuación original ingresada
        archivo.write("Ecuacion: " + ecuacion + "\n")
        # Guardamos la ecuación ya balanceada
        archivo.write("Balanceada: " + balanceada + "\n")
        # También guardamos el tipo de reacción encontrado
        archivo.write("Tipo: " + tipo + "\n")
        # Guardamos la fecha y hora en la que se realizó la operación
        archivo.write(
            "Fecha: " +
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
            "\n"
        )
        # Agregamos una línea divisoria para organizar mejor el historial
        archivo.write("-" * 40 + "\n")


# Esta función se encarga de leer y mostrar el historial completo
def mostrar_historial():
    try:
        # Abrimos el archivo en modo lectura
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            # Si el archivo está vacío mostramos un mensaje
            if contenido.strip() == "":
                print("\nNo hay historial todavia")
            # Si sí hay contenido mostramos todo organizado
            else:
                print("\n===== HISTORIAL =====")
                print(contenido)
    except FileNotFoundError:
        # Si el archivo todavía no existe evitamos que el programa falle
        print("\nNo hay historial todavia")


# Esta función lee el historial y lo devuelve como texto
# Si no existe el archivo devuelve un string vacío
def _leer_historial():
    try:
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return ""


# Esta función prepara el historial como bytes de texto plano
# Streamlit lo recibe y lo manda al navegador como descarga directa
def exportar_como_txt():
    contenido = _leer_historial()
    # Si no hay nada guardado devolvemos None para desactivar el botón
    if not contenido.strip():
        return None
    return contenido.encode("utf-8")


# Esta función genera un PDF con el historial y lo devuelve como bytes
# Usamos fpdf2 que es sencilla y no necesita dependencias externas
def exportar_como_pdf():
    contenido = _leer_historial()
    # Si no hay nada guardado devolvemos None para desactivar el botón
    if not contenido.strip():
        return None

    pdf = FPDF()
    pdf.add_page()

    # Titulo del reporte
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(
        0, 10,
        "Historial - Balanceador de Ecuaciones Quimicas",
        ln=True, align="C"
    )
    pdf.ln(4)

    # Fecha en que se exporto
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0, 8,
        "Exportado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ln=True, align="C"
    )
    pdf.ln(6)

    # Separamos el contenido en entradas individuales
    # cada entrada está dividida por la línea de guiones
    entradas = contenido.strip().split("-" * 40)

    for entrada in entradas:
        entrada = entrada.strip()
        # Saltamos entradas vacías
        if not entrada:
            continue

        # Recorremos cada línea de la entrada
        for linea in entrada.splitlines():
            linea = linea.strip()
            if not linea:
                continue

            # Si la línea tiene etiqueta ponemos la etiqueta en negrita
            if ":" in linea:
                etiqueta, _, valor = linea.partition(":")
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(30, 7, etiqueta + ":", ln=False)
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(0, 7, valor.strip(), ln=True)
            else:
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(0, 7, linea, ln=True)

        # Línea divisoria entre entradas
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
        pdf.ln(6)

    # Devolvemos el PDF como bytes para que Streamlit lo descargue
    return bytes(pdf.output())
