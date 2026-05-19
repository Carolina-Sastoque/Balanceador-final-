# Programa principal realizado por el equipo del proyecto

"""
Este archivo es el nucleo principal de la aplicacion.

Aqui conectamos todos los modulos del proyecto
para construir la interfaz interactiva en Streamlit.

El sistema permite:

- Balancear ecuaciones quimicas
- Verificar atomos antes y despues del balanceo
- Identificar el tipo de reaccion
- Calcular masas molares
- Consultar elementos de la tabla periodica
- Practicar con un quiz interactivo
- Guardar y exportar historial de resultados

Cada funcionalidad esta organizada en pestanas
para que la aplicacion sea mas clara y facil de usar.
"""

import streamlit as st
import pandas as pd

# Importamos los modulos principales del proyecto
from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_como_txt, exportar_como_pdf
from explicacion_balanceo import explicar_balanceo
from verificar_atomos import tabla_verificacion
from verificacion import ecuacion_ya_balanceada

# Importamos modulos adicionales
from validacion import validar_ecuacion
from explicacion_reacciones import obtener_explicacion
from tabla_periodica import (
    buscar_elemento,
    obtener_color_categoria
)
from quiz import (
    obtener_pregunta_aleatoria,
    verificar_respuesta
)


# Configuracion general de la pagina
st.set_page_config(
    page_title="Balanceador Quimico",
    page_icon="",
    layout="wide"
)

# Titulo principal de la aplicacion
st.title("Balanceador de Ecuaciones Quimicas")


# Creamos las pestanas principales del sistema
pestanas = st.tabs([
    "Balanceador",
    "Tabla Periodica",
    "Quiz",
    "Historial",
])


# ============================================================
# PESTANA 1 - Balanceador principal
# ============================================================
with pestanas[0]:

    st.write(
        "Escribe una ecuacion usando '=' para separar "
        "reactivos y productos, y '+' entre compuestos."
    )

    # Campo donde el usuario escribe la ecuacion
    ecuacion = st.text_input(
        "Ejemplo: H2 + O2 = H2O",
        key="ecuacion_input"
    )

    # Boton principal para analizar la ecuacion
    if st.button("Analizar"):

        # Verificamos que el usuario haya escrito algo
        if ecuacion.strip() == "":

            st.warning("Escribe una ecuacion primero.")

        else:

            # Validamos la ecuacion antes de procesarla
            es_valida, errores = validar_ecuacion(ecuacion)

            if not es_valida:

                st.error("La ecuacion tiene errores.")

                # Mostramos todos los errores encontrados
                for error in errores:
                    st.write(f"- {error}")

            else:

                try:

                    # Verificamos si ya estaba balanceada
                    ya_balanceada, detalle = (
                        ecuacion_ya_balanceada(ecuacion)
                    )

                    if ya_balanceada:
                        st.success(
                            "Esta ecuacion ya esta balanceada."
                        )
                    else:
                        st.info(
                            "La ecuacion no esta balanceada."
                        )

                    # Separamos reactivos y productos
                    reactivos, productos = (
                        Separar_ecuacion(ecuacion)
                    )

                    # Calculamos los coeficientes
                    coeficientes, compuestos, _, _, _ = (
                        calcular_coeficientes(
                            reactivos,
                            productos
                        )
                    )

                    # Construimos la ecuacion balanceada
                    ecuacion_balanceada = ""

                    for i, comp in enumerate(compuestos):

                        coef = coeficientes[i]

                        if coef == 1:
                            ecuacion_balanceada += comp
                        else:
                            ecuacion_balanceada += f"{coef}{comp}"

                        # Agregamos simbolos de separacion
                        if i == len(reactivos) - 1:
                            ecuacion_balanceada += " = "
                        elif i < len(compuestos) - 1:
                            ecuacion_balanceada += " + "

                    # Resultado principal
                    st.subheader("Ecuacion balanceada")
                    st.success(ecuacion_balanceada)

                    # Clasificamos el tipo de reaccion
                    tipo = clasificar_reaccion(ecuacion)
                    st.subheader("Tipo de reaccion")

                    # Obtenemos la explicacion del tipo
                    info_tipo = obtener_explicacion(tipo)
                    st.info(
                        f"{info_tipo['nombre_completo']}"
                    )

                    # Explicacion expandible
                    with st.expander("Ver explicacion"):

                        st.markdown(
                            f"**Que es?**\n\n"
                            f"{info_tipo['descripcion']}"
                        )
                        st.markdown(
                            f"**Como identificarla?**\n\n"
                            f"{info_tipo['como_identificarla']}"
                        )
                        st.markdown(
                            f"**Ejemplo clasico:**\n\n"
                            f"`{info_tipo['ejemplo']}`"
                        )
                        st.markdown(
                            f"**Curiosidad:**\n\n"
                            f"{info_tipo['curiosidad']}"
                        )

                    # Mostramos masas molares
                    st.subheader("Masas molares")

                    for comp in compuestos:
                        masa = calculo_masa_molar(comp)
                        st.write(f"**{comp}:** {masa} g/mol")

                    # Conteo de atomos
                    st.subheader("Conteo de atomos")

                    datos = tabla_verificacion(
                        reactivos,
                        productos,
                        coeficientes,
                        compuestos
                    )

                    # Tabla antes del balanceo
                    st.markdown("**Antes del balanceo**")

                    filas_antes = []

                    for elem in datos["elementos"]:
                        filas_antes.append({
                            "Elemento": elem,
                            "Reactivos": datos["antes_reactivos"].get(elem, 0),
                            "Productos": datos["antes_productos"].get(elem, 0),
                            "Igual?":
                            "Si"
                            if datos["antes_reactivos"].get(elem, 0)
                            == datos["antes_productos"].get(elem, 0)
                            else "No"
                        })

                    st.table(
                        pd.DataFrame(filas_antes)
                        .set_index("Elemento")
                    )

                    # Tabla despues del balanceo
                    st.markdown("**Despues del balanceo**")

                    filas_despues = []

                    for elem in datos["elementos"]:
                        filas_despues.append({
                            "Elemento": elem,
                            "Reactivos": datos["despues_reactivos"].get(elem, 0),
                            "Productos": datos["despues_productos"].get(elem, 0),
                            "Igual?":
                            "Si"
                            if datos["despues_reactivos"].get(elem, 0)
                            == datos["despues_productos"].get(elem, 0)
                            else "No"
                        })

                    st.table(
                        pd.DataFrame(filas_despues)
                        .set_index("Elemento")
                    )

                    # Explicacion paso a paso
                    st.subheader("Explicacion del balanceo")

                    with st.expander("Ver pasos"):
                        for bloque in explicar_balanceo(ecuacion):
                            st.markdown(bloque)

                    # Guardamos el resultado en historial
                    guardar_en_historial(
                        ecuacion,
                        ecuacion_balanceada,
                        tipo
                    )

                except Exception as e:
                    st.error(f"Error al procesar la ecuacion: {e}")


# ============================================================
# PESTANA 2 - Tabla periodica
# ============================================================
with pestanas[1]:

    st.header("Consulta de Elementos")
    st.write("Busca un elemento usando su simbolo o nombre.")

    # Campo de busqueda
    busqueda = st.text_input(
        "Buscar elemento:",
        placeholder="Ejemplo: Fe, Hierro, Carbon"
    )

    if busqueda.strip():

        # Buscamos el elemento
        elemento = buscar_elemento(busqueda.strip())

        if elemento is None:
            st.error(
                f"No se encontro ningun elemento con '{busqueda}'."
            )
        else:

            # Obtenemos el color de la categoria
            color = obtener_color_categoria(
                elemento["categoria"]
            )

            st.markdown("---")

            col_izq, col_der = st.columns([1, 2])

            with col_izq:

                # Tarjeta visual del elemento
                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        color: white;
                        border-radius: 12px;
                        padding: 20px;
                        text-align: center;
                        font-family: monospace;
                    ">
                        <div style="font-size: 14px;">
                            {elemento['numero']}
                        </div>
                        <div style="font-size: 60px; font-weight: bold;">
                            {elemento['simbolo']}
                        </div>
                        <div style="font-size: 18px;">
                            {elemento['nombre']}
                        </div>
                        <div style="font-size: 14px;">
                            {elemento['masa']} g/mol
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_der:

                st.markdown(
                    f"### {elemento['nombre']} ({elemento['simbolo']})"
                )

                st.table(
                    pd.DataFrame({
                        "Propiedad": [
                            "Numero atomico",
                            "Masa atomica",
                            "Grupo",
                            "Periodo",
                            "Categoria"
                        ],
                        "Valor": [
                            elemento["numero"],
                            f"{elemento['masa']} g/mol",
                            elemento["grupo"],
                            elemento["periodo"],
                            elemento["categoria"],
                        ]
                    }).set_index("Propiedad")
                )


# ============================================================
# PESTANA 3 - Quiz interactivo
# ============================================================
with pestanas[2]:

    st.header("Quiz de Balanceo")
    st.write("Practica balanceando ecuaciones quimicas.")

    # Inicializamos variables de sesion
    if "quiz_pregunta" not in st.session_state:
        st.session_state.quiz_pregunta = None

    if "quiz_pista_idx" not in st.session_state:
        st.session_state.quiz_pista_idx = 0

    if "quiz_puntos" not in st.session_state:
        st.session_state.quiz_puntos = 0

    if "quiz_intentos" not in st.session_state:
        st.session_state.quiz_intentos = 0

    if "quiz_respondida" not in st.session_state:
        st.session_state.quiz_respondida = False

    # Selector de dificultad
    col_dif, col_btn = st.columns([2, 1])

    with col_dif:
        dificultad = st.selectbox(
            "Dificultad:",
            ["Cualquiera", "Facil", "Media", "Dificil"],
            key="quiz_dificultad"
        )

    with col_btn:
        st.write("")
        # Boton para generar nueva pregunta
        if st.button("Nueva pregunta"):
            nivel = (
                None if dificultad == "Cualquiera"
                else dificultad
            )
            st.session_state.quiz_pregunta = (
                obtener_pregunta_aleatoria(nivel)
            )
            st.session_state.quiz_pista_idx = 0
            st.session_state.quiz_respondida = False

    # Mostrar puntuacion
    if st.session_state.quiz_intentos > 0:
        porcentaje = int(
            st.session_state.quiz_puntos /
            st.session_state.quiz_intentos * 100
        )
        st.metric(
            label="Puntuacion",
            value=(
                f"{st.session_state.quiz_puntos} / "
                f"{st.session_state.quiz_intentos}"
            ),
            delta=f"{porcentaje}% de aciertos"
        )

    st.markdown("---")

    # Mostrar pregunta actual
    if st.session_state.quiz_pregunta is None:
        st.info("Presiona 'Nueva pregunta' para empezar.")

    else:

        pregunta = st.session_state.quiz_pregunta

        st.markdown(f"**Nivel:** {pregunta['dificultad']}")
        st.code(pregunta["sin_balancear"])

        if st.session_state.quiz_respondida:
            st.success("Correcto. Genera otra pregunta.")

        else:

            # Campo de respuesta
            respuesta = st.text_input(
                "Tu respuesta:",
                placeholder="Ejemplo: 2H2 + O2 = 2H2O",
                key="quiz_respuesta_input"
            )

            col_verificar, col_pista = st.columns([1, 1])

            with col_verificar:
                if st.button("Verificar"):
                    if not respuesta.strip():
                        st.warning("Escribe una respuesta.")
                    else:
                        es_correcta, mensaje = (
                            verificar_respuesta(
                                pregunta["sin_balancear"],
                                respuesta
                            )
                        )
                        st.session_state.quiz_intentos += 1
                        if es_correcta:
                            st.success(mensaje)
                            st.session_state.quiz_puntos += 1
                            st.session_state.quiz_respondida = True
                        else:
                            st.error(f"Incorrecto: {mensaje}")

            with col_pista:
                if st.button("Pedir pista"):
                    idx = st.session_state.quiz_pista_idx
                    pistas = pregunta["pistas"]
                    if idx < len(pistas):
                        st.info(
                            f"**Pista {idx + 1}:** {pistas[idx]}"
                        )
                        st.session_state.quiz_pista_idx += 1
                    else:
                        st.warning("Ya no hay mas pistas.")

            # Mostrar pistas usadas
            pistas_usadas = st.session_state.quiz_pista_idx

            if pistas_usadas > 0:
                st.markdown("**Pistas mostradas:**")
                for i in range(pistas_usadas):
                    st.write(
                        f"- Pista {i+1}: {pregunta['pistas'][i]}"
                    )


# ============================================================
# PESTANA 4 - Historial
# ============================================================
with pestanas[3]:

    st.header("Historial de ecuaciones")

    try:
        with open("historial.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            if contenido.strip() == "":
                st.write("No hay historial todavia.")
            else:
                st.text(contenido)

    except FileNotFoundError:
        st.write("No hay historial todavia.")

    # Botones de descarga lado a lado
    col_txt, col_pdf = st.columns(2)

    with col_txt:

        datos_txt = exportar_como_txt()

        # Si hay datos el boton descarga, si no se desactiva
        st.download_button(
            label="Descargar TXT",
            data=datos_txt if datos_txt else b"Sin historial",
            file_name="historial_balanceo.txt",
            mime="text/plain",
            disabled=datos_txt is None
        )

    with col_pdf:

        datos_pdf = exportar_como_pdf()

        # Si hay datos el boton descarga, si no se desactiva
        st.download_button(
            label="Descargar PDF",
            data=datos_pdf if datos_pdf else b"Sin historial",
            file_name="historial_balanceo.pdf",
            mime="application/pdf",
            disabled=datos_pdf is None
        )
