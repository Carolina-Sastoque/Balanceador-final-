import streamlit as st
import pandas as pd

from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_como_txt, exportar_como_pdf
from explicacion_balanceo import explicar_balanceo
from verificar_atomos import tabla_verificacion
from verificacion import ecuacion_ya_balanceada
from validacion import validar_ecuacion
from explicacion_reacciones import obtener_explicacion
from tabla_periodica import buscar_elemento, obtener_color_categoria
from quiz import obtener_pregunta_aleatoria, verificar_respuesta

st.set_page_config(
    page_title="Balanceador Químico ",
    page_icon="⚗",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

:root {
    --navy-950: #060e1a;
    --navy-900: #0b1827;
    --navy-800: #0f2238;
    --navy-700: #152d4a;
    --navy-600: #1d3d62;
    --navy-500: #28527e;
    --navy-400: #3a6fa0;
    --blue-400: #4a8bc4;
    --blue-300: #6aa5d8;
    --blue-200: #93c0e6;
    --blue-100: #bcd8f0;
    --blue-50:  #dceef9;
    --text-primary: #dce8f4;
    --text-secondary: #8aadc8;
    --text-muted: #5a7a96;
    --border: rgba(74,139,196,0.18);
    --border-strong: rgba(74,139,196,0.32);
    --surface: rgba(15,34,56,0.9);
    --surface-hover: rgba(21,45,74,0.95);
    --accent: #4a8bc4;
    --accent-glow: rgba(74,139,196,0.12);
}

html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background-color: var(--navy-900) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stMainBlockContainer"] {
    max-width: 860px !important;
    padding: 2.5rem 2rem 4rem !important;
    margin: 0 auto !important;
}
footer { display: none !important; }

/* ── Marca principal ── */
.app-header {
    text-align: center;
    padding: 2.4rem 0 1.6rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.app-header .label {
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--blue-300);
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 500;
    margin-bottom: 0.6rem;
}
.app-header h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: var(--blue-50) !important;
    margin: 0 !important;
    line-height: 1.2 !important;
    letter-spacing: -0.01em !important;
}
.app-header .subtitle {
    font-size: 0.92rem;
    color: var(--text-secondary);
    margin-top: 0.6rem;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    margin-bottom: 1.8rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.2rem !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    transition: color 0.2s, border-color 0.2s !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--blue-200) !important;
    border-bottom-color: var(--blue-300) !important;
}
[data-testid="stTabs"] [aria-selected="false"]:hover {
    color: var(--text-primary) !important;
}
div[data-baseweb="tab-highlight"] { display: none !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label { display: none !important; }

[data-testid="stTextInput"] input {
    background: var(--navy-800) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-muted) !important; }

/* ── Botones ── */
[data-testid="stButton"] > button {
    background: var(--navy-700) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    color: var(--blue-200) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--navy-600) !important;
    border-color: var(--blue-400) !important;
    color: var(--blue-100) !important;
}

/* ── Botón primario (Analizar) ── */
[data-testid="stButton"]:first-of-type > button {
    background: var(--navy-600) !important;
    border-color: var(--blue-400) !important;
    color: var(--blue-50) !important;
    font-weight: 600 !important;
    padding: 0.65rem 2rem !important;
}
[data-testid="stButton"]:first-of-type > button:hover {
    background: var(--blue-400) !important;
    color: #fff !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
    background: var(--navy-800) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--blue-400) !important;
    color: var(--blue-200) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--navy-800) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Alerts / info / success / warning / error ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}
.stSuccess {
    background: rgba(28, 58, 42, 0.5) !important;
    border-color: rgba(46, 132, 85, 0.4) !important;
    color: #7ecb9e !important;
}
.stInfo {
    background: rgba(15, 40, 68, 0.6) !important;
    border-color: var(--border-strong) !important;
    color: var(--blue-100) !important;
}
.stWarning {
    background: rgba(58, 44, 12, 0.5) !important;
    border-color: rgba(160, 110, 30, 0.4) !important;
    color: #e2b96a !important;
}
.stError {
    background: rgba(58, 18, 18, 0.5) !important;
    border-color: rgba(160, 50, 50, 0.4) !important;
    color: #e28a8a !important;
}

/* ── Métricas ── */
[data-testid="stMetric"] {
    background: var(--navy-800) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--blue-100) !important;
    font-size: 1.6rem !important;
    font-family: 'Playfair Display', serif !important;
}

/* ── Código ── */
[data-testid="stCodeBlock"] pre, code {
    background: var(--navy-800) !important;
    border: 1px solid var(--border) !important;
    color: var(--blue-100) !important;
    border-radius: 8px !important;
    font-size: 0.96rem !important;
}

/* ── Tablas ── */
[data-testid="stTable"] table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 0.88rem !important;
}
[data-testid="stTable"] thead th {
    background: var(--navy-700) !important;
    color: var(--blue-200) !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1rem !important;
    border-bottom: 1px solid var(--border-strong) !important;
}
[data-testid="stTable"] tbody td {
    color: var(--text-primary) !important;
    padding: 0.55rem 1rem !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stTable"] tbody tr:hover td {
    background: var(--accent-glow) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--navy-800) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* ── Divisores ── */
hr { border: none; border-top: 1px solid var(--border); margin: 1.6rem 0; }

/* ── Componentes personalizados ── */
.section-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--blue-400);
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--blue-50);
    margin-bottom: 1.2rem;
}
.result-card {
    background: var(--navy-800);
    border: 1px solid var(--border-strong);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.result-card .rc-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
    font-weight: 500;
}
.result-card .rc-value {
    font-size: 1.05rem;
    color: var(--text-primary);
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 500;
    min-height: 1.4rem;
    word-break: break-word;
}
.result-card .rc-value.highlight {
    color: var(--blue-100);
    font-weight: 600;
    font-size: 1.1rem;
}
.atom-table-wrap {
    background: var(--navy-800);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.atom-table-wrap table { width: 100%; border-collapse: collapse; }
.atom-table-wrap thead th {
    background: var(--navy-700);
    color: var(--blue-200);
    font-size: 0.74rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
    padding: 0.6rem 0.9rem;
    text-align: left;
    border-bottom: 1px solid var(--border-strong);
}
.atom-table-wrap tbody td {
    padding: 0.55rem 0.9rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.88rem;
    color: var(--text-primary);
    vertical-align: middle;
}
.atom-table-wrap tbody tr:last-child td { border-bottom: none; }
.bar-cell { display: flex; align-items: center; gap: 8px; }
.bar-bg {
    flex: 1; background: var(--navy-600);
    border-radius: 3px; height: 8px;
    overflow: hidden; min-width: 50px;
}
.bar-fill { height: 100%; border-radius: 3px; transition: width 0.4s ease; }
.explanation-box {
    background: var(--navy-800);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    min-height: 160px;
    color: var(--text-secondary);
    font-size: 0.93rem;
    line-height: 1.8;
}
.masa-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--navy-700);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.35rem 0.8rem;
    margin: 0.2rem;
    font-size: 0.88rem;
    color: var(--text-primary);
}
.masa-pill strong { color: var(--blue-200); font-weight: 600; }
.masa-pill span { color: var(--text-muted); font-size: 0.82rem; }
.export-row {
    display: flex; gap: 10px; margin-top: 1rem; align-items: stretch;
}
.export-label {
    flex: 1;
    background: var(--navy-700);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    display: flex; align-items: center;
}
.input-hint {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    text-align: center;
}
.quiz-question-box {
    background: var(--navy-800);
    border: 1px solid var(--border-strong);
    border-left: 3px solid var(--blue-400);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
}
.hist-entry {
    background: var(--navy-800);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    font-family: 'Source Sans 3', monospace;
}
.hist-entry .he-eq { color: var(--blue-200); font-weight: 600; margin-bottom: 0.2rem; }
.hist-entry .he-bal { color: var(--text-primary); margin-bottom: 0.15rem; }
.hist-entry .he-meta { color: var(--text-muted); font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)


# ── Encabezado ──
col_gato, col_titulo = st.columns([1, 3])

with col_gato:
    st.image("https://i.pinimg.com/736x/83/81/24/83812467a64518774d9f595efe4adc9b.jpg", use_container_width=True)

with col_titulo:
    st.markdown("""
    <div class="app-header" style="text-align:left; border-bottom:none; padding-top:1rem">
        <h1>Balanceador de Ecuaciones Químicas ꉂ(˵˃ ᗜ ˂˵)⋆˚꩜｡</h1>
        <div class="subtitle">꒷꒦︶꒷꒦︶ ๋ ࣭ ⭑꒷꒦</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Pestañas ─────────────────────────────────────────────
pestanas = st.tabs(["(⸝⸝> ᴗ•⸝⸝) Balanceador", "(˶˃𐃷˂˶) Tabla Periódica", "(⸝⸝๑﹏๑⸝⸝) Quiz", "₍^. .^₎⟆ Historial"])


# ══════════════════════════════════════════════════════════
# PESTAÑA 1 — Balanceador
# ══════════════════════════════════════════════════════════
with pestanas[0]:

    # Input centrado
    col_void1, col_mid, col_void2 = st.columns([0.5, 6, 0.5])
    with col_mid:
        ecuacion = st.text_input(
            "eq", label_visibility="collapsed",
            placeholder="Ej: Al(OH)3 + H2SO4 = Al2(SO4)3 + H2O",
            key="eq_input"
        )
        st.markdown(
            "<div class='input-hint'>Separa reactivos y productos con  =  · usa + entre compuestos</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns([2, 2, 2])
    with col_b2:
        analizar = st.button("Analizar ecuación", use_container_width=True)

    # ── Resultados ──────────────────────────────────────
    eq_bal = ""
    tipo_str = ""
    datos_tabla = None
    bloques_exp = []
    masas = {}

    if analizar:
        if not ecuacion.strip():
            st.warning("Escribe una ecuación primero.")
        else:
            es_valida, errores = validar_ecuacion(ecuacion)
            if not es_valida:
                st.error("Ecuación inválida: " + " · ".join(errores))
            else:
                try:
                    reactivos, productos = Separar_ecuacion(ecuacion)
                    coeficientes, compuestos, _, _, _ = calcular_coeficientes(reactivos, productos)
                    n_r = len(reactivos)
                    partes = [
                        comp if coeficientes[i] == 1 else f"{coeficientes[i]}{comp}"
                        for i, comp in enumerate(compuestos)
                    ]
                    eq_bal = " + ".join(partes[:n_r]) + " = " + " + ".join(partes[n_r:])
                    tipo_raw = clasificar_reaccion(ecuacion)
                    info_tipo = obtener_explicacion(tipo_raw)
                    tipo_str = f"{info_tipo['icono']}  {info_tipo['nombre_completo']}"
                    datos_tabla = tabla_verificacion(reactivos, productos, coeficientes, compuestos)
                    bloques_exp = explicar_balanceo(ecuacion)
                    masas = {comp: calculo_masa_molar(comp) for comp in compuestos}
                    guardar_en_historial(ecuacion, eq_bal, tipo_raw)

                    ya_bal, _ = ecuacion_ya_balanceada(ecuacion)
                    if ya_bal:
                        st.info("ℹ  La ecuación ya estaba balanceada.")
                except Exception as e:
                    st.error(f"Error al procesar: {e}")

    if eq_bal:
        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Resultado principal ──
        st.markdown("<div class='section-eyebrow'>Resultado</div><div class='section-title'>Ecuación balanceada</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
          <div class="rc-label">Ecuación</div>
          <div class="rc-value highlight">{eq_bal}</div>
        </div>
        <div class="result-card">
          <div class="rc-label">Tipo de reacción</div>
          <div class="rc-value">{tipo_str}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Masas molares ──
        if masas:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-eyebrow'>Cálculo</div><div class='section-title'>Masas molares</div>", unsafe_allow_html=True)
            pills = "".join(
                f"<span class='masa-pill'><strong>{c}</strong><span>{m} g/mol</span></span>"
                for c, m in masas.items()
            )
            st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px'>{pills}</div>", unsafe_allow_html=True)

        # ── Tipo: descripción expandible ──
        if analizar and tipo_str:
            try:
                tipo_raw2 = clasificar_reaccion(ecuacion)
                info2 = obtener_explicacion(tipo_raw2)
                with st.expander("Ver descripción del tipo de reacción"):
                    st.markdown(f"**¿Qué es?**\n\n{info2['descripcion']}")
                    st.markdown(f"**¿Cómo identificarla?**\n\n{info2['como_identificarla']}")
                    st.markdown(f"**Ejemplo clásico:** `{info2['ejemplo']}`")
                    st.markdown(f"**Curiosidad:** {info2['curiosidad']}")
            except:
                pass

        # ── Tabla de átomos ──
        if datos_tabla:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-eyebrow'>Verificación</div><div class='section-title'>Conteo de átomos</div>", unsafe_allow_html=True)

            def render_tabla(datos, modo):
                col_r = datos["antes_reactivos"] if modo == "antes" else datos["despues_reactivos"]
                col_p = datos["antes_productos"]  if modo == "antes" else datos["despues_productos"]
                elementos = datos["elementos"]
                max_v = max([col_r.get(e,0) for e in elementos] + [col_p.get(e,0) for e in elementos] + [1])
                titulo = "Antes del balanceo (coef. = 1)" if modo == "antes" else "Después del balanceo"
                filas = ""
                for elem in elementos:
                    r, p = col_r.get(elem,0), col_p.get(elem,0)
                    igual = "✓" if r == p else "✗"
                    color_igual = "#4a9e6e" if r == p else "#c05050"
                    pct_r = int(r/max_v*100)
                    pct_p = int(p/max_v*100)
                    c_bar_p = "#3a6fa0" if r == p else "#8b3030"
                    filas += f"""
                    <tr>
                      <td><strong style="color:var(--blue-200)">{elem}</strong></td>
                      <td><div class="bar-cell">
                          <span style="min-width:20px;text-align:right;font-weight:600">{r}</span>
                          <div class="bar-bg"><div class="bar-fill" style="width:{pct_r}%;background:#28527e"></div></div>
                      </div></td>
                      <td><div class="bar-cell">
                          <span style="min-width:20px;text-align:right;font-weight:600">{p}</span>
                          <div class="bar-bg"><div class="bar-fill" style="width:{pct_p}%;background:{c_bar_p}"></div></div>
                      </div></td>
                      <td style="text-align:center;color:{color_igual};font-weight:700;font-size:0.9rem">{igual}</td>
                    </tr>"""
                return f"""
                <div class="atom-table-wrap" style="margin-bottom:1rem">
                  <div style="padding:0.6rem 0.9rem 0;font-size:0.74rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-muted);font-weight:600">{titulo}</div>
                  <table>
                    <thead><tr>
                      <th>Elemento</th><th>Reactivos</th><th>Productos</th>
                      <th style="text-align:center">¿Igual?</th>
                    </tr></thead>
                    <tbody>{filas}</tbody>
                  </table>
                </div>"""

            st.markdown(render_tabla(datos_tabla, "antes"),   unsafe_allow_html=True)
            st.markdown(render_tabla(datos_tabla, "despues"), unsafe_allow_html=True)

        # ── Explicación ──
        if bloques_exp:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-eyebrow'>Paso a paso</div><div class='section-title'>Explicación del balanceo</div>", unsafe_allow_html=True)
            st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
            for bloque in bloques_exp:
                st.markdown(bloque)   # Streamlit procesa el Markdown nativamente
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Exportar ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>Exportar</div>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        datos_txt = exportar_como_txt()
        st.download_button(
            "↓  Descargar historial TXT",
            data=datos_txt if datos_txt else b"Sin historial",
            file_name="historial_balanceo.txt",
            mime="text/plain",
            disabled=datos_txt is None,
            use_container_width=True,
        )
    with col_e2:
        datos_pdf = exportar_como_pdf()
        st.download_button(
            "↓  Descargar historial PDF",
            data=datos_pdf if datos_pdf else b"Sin historial",
            file_name="historial_balanceo.pdf",
            mime="application/pdf",
            disabled=datos_pdf is None,
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════
# PESTAÑA 2 — Tabla periódica
# ══════════════════════════════════════════════════════════
with pestanas[1]:
    st.markdown("<div class='section-eyebrow'>Consulta</div><div class='section-title'>Tabla periódica</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--text-secondary);font-size:0.9rem;margin-bottom:1.2rem'>Busca por símbolo (<code>Fe</code>, <code>O</code>) o nombre en español/inglés.</p>", unsafe_allow_html=True)

    busqueda = st.text_input("elem", label_visibility="collapsed",
                             placeholder="Ejemplo: Fe · Hierro · Calcium · O")

    if busqueda.strip():
        elemento = buscar_elemento(busqueda.strip())
        if elemento is None:
            st.error(f"No se encontró ningún elemento con '{busqueda}'.")
        else:
            color = obtener_color_categoria(elemento["categoria"])
            st.markdown("<hr>", unsafe_allow_html=True)
            col_izq, col_der = st.columns([1, 2])
            with col_izq:
                st.markdown(f"""
                <div style="background:{color};border-radius:12px;padding:1.6rem 1rem;
                            text-align:center;font-family:'Source Sans 3',sans-serif">
                  <div style="font-size:0.75rem;opacity:0.75;font-weight:600;letter-spacing:0.1em;
                              text-transform:uppercase;margin-bottom:0.3rem;color:white">
                    Z = {elemento['numero']}
                  </div>
                  <div style="font-size:3.6rem;font-weight:700;line-height:1;color:white;
                              font-family:'Playfair Display',serif">
                    {elemento['simbolo']}
                  </div>
                  <div style="font-size:1rem;margin-top:0.5rem;color:white;font-weight:500">
                    {elemento['nombre']}
                  </div>
                  <div style="font-size:0.85rem;opacity:0.8;margin-top:0.2rem;color:white">
                    {elemento['masa']} g/mol
                  </div>
                </div>""", unsafe_allow_html=True)
            with col_der:
                st.markdown(f"<div class='section-title' style='font-size:1.2rem;margin-bottom:0.8rem'>{elemento['nombre']}</div>", unsafe_allow_html=True)
                st.table(pd.DataFrame({
                    "Propiedad": ["Número atómico","Masa atómica","Grupo","Período","Categoría"],
                    "Valor": [
                        elemento["numero"], f"{elemento['masa']} g/mol",
                        elemento["grupo"], elemento["periodo"], elemento["categoria"]
                    ],
                }).set_index("Propiedad"))


# ══════════════════════════════════════════════════════════
# PESTAÑA 3 — Quiz
# ══════════════════════════════════════════════════════════
with pestanas[2]:
    st.markdown("<div class='section-eyebrow'>Práctica</div><div class='section-title'>Quiz de balanceo</div>", unsafe_allow_html=True)

    for k, v in [("quiz_pregunta",None),("quiz_pista_idx",0),
                 ("quiz_puntos",0),("quiz_intentos",0),("quiz_respondida",False)]:
        if k not in st.session_state:
            st.session_state[k] = v

    col_d, col_b = st.columns([3, 1])
    with col_d:
        dificultad = st.selectbox("dif", label_visibility="collapsed",
                                  options=["Cualquiera","Fácil","Media","Difícil"],
                                  key="quiz_dif")
    with col_b:
        if st.button("Nueva →", use_container_width=True):
            nivel = None if dificultad == "Cualquiera" else dificultad
            st.session_state.quiz_pregunta   = obtener_pregunta_aleatoria(nivel)
            st.session_state.quiz_pista_idx  = 0
            st.session_state.quiz_respondida = False

    if st.session_state.quiz_intentos > 0:
        pct = int(st.session_state.quiz_puntos / st.session_state.quiz_intentos * 100)
        c1, c2, c3 = st.columns(3)
        c1.metric("Correctas", st.session_state.quiz_puntos)
        c2.metric("Intentos", st.session_state.quiz_intentos)
        c3.metric("Precisión", f"{pct}%")

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.session_state.quiz_pregunta is None:
        st.markdown("<div class='explanation-box' style='text-align:center;color:var(--text-muted)'>Presiona <strong style=\"color:var(--blue-200)\">Nueva</strong> para comenzar una pregunta</div>", unsafe_allow_html=True)
    else:
        p = st.session_state.quiz_pregunta
        st.markdown(f"""
        <div class="quiz-question-box">
          <div style="font-size:0.74rem;letter-spacing:0.12em;text-transform:uppercase;
                      color:var(--blue-400);font-weight:600;margin-bottom:0.5rem">
            Nivel · {p['dificultad']}
          </div>
          <div style="font-family:'Source Sans 3',monospace;font-size:1.05rem;
                      color:var(--text-primary);font-weight:500">
            {p['sin_balancear']}
          </div>
          <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.4rem">
            Balancea esta ecuación
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.quiz_respondida:
            st.success("¡Correcto! Genera una nueva pregunta para continuar.")
        else:
            respuesta = st.text_input("resp", label_visibility="collapsed",
                                      placeholder="Ej: 2H2 + O2 = 2H2O", key="quiz_resp")
            cv, cp = st.columns(2)
            with cv:
                if st.button("Verificar", use_container_width=True):
                    if not respuesta.strip():
                        st.warning("Escribe tu respuesta.")
                    else:
                        ok, msg = verificar_respuesta(p["sin_balancear"], respuesta)
                        st.session_state.quiz_intentos += 1
                        if ok:
                            st.success(msg)
                            st.session_state.quiz_puntos += 1
                            st.session_state.quiz_respondida = True
                        else:
                            st.error(f"Incorrecto: {msg}")
            with cp:
                if st.button("Pedir pista", use_container_width=True):
                    idx = st.session_state.quiz_pista_idx
                    if idx < len(p["pistas"]):
                        st.info(f"Pista {idx+1}: {p['pistas'][idx]}")
                        st.session_state.quiz_pista_idx += 1
                    else:
                        st.warning("No hay más pistas disponibles.")

            if st.session_state.quiz_pista_idx > 0:
                for i in range(st.session_state.quiz_pista_idx):
                    st.markdown(f"<div style='font-size:0.85rem;color:var(--text-muted);margin-top:0.3rem'>💡 Pista {i+1}: {p['pistas'][i]}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PESTAÑA 4 — Historial
# ══════════════════════════════════════════════════════════
with pestanas[3]:
    st.markdown("<div class='section-eyebrow'>Registro</div><div class='section-title'>Historial de ecuaciones</div>", unsafe_allow_html=True)

    try:
        with open("historial.txt", "r", encoding="utf-8") as f:
            raw = f.read().strip()
        if not raw:
            st.markdown("<div class='explanation-box' style='text-align:center;color:var(--text-muted)'>No hay entradas registradas todavía.</div>", unsafe_allow_html=True)
        else:
            entradas = raw.split("----------------------------------------")
            for entrada in entradas:
                entrada = entrada.strip()
                if not entrada:
                    continue
                lineas = {
                    l.split(":")[0].strip(): ":".join(l.split(":")[1:]).strip()
                    for l in entrada.splitlines() if ":" in l
                }
                eq    = lineas.get("Ecuacion", "")
                bal   = lineas.get("Balanceada", "")
                tipo  = lineas.get("Tipo", "")
                fecha = lineas.get("Fecha", "")
                if eq or bal:
                    st.markdown(f"""
                    <div class="hist-entry">
                      <div class="he-eq">{eq}</div>
                      <div class="he-bal">→ {bal}</div>
                      <div class="he-meta">{tipo}  ·  {fecha}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("<div class='explanation-box' style='text-align:center;color:var(--text-muted)'>No hay entradas registradas todavía.</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        datos_txt = exportar_como_txt()
        st.download_button("↓  Descargar TXT", data=datos_txt if datos_txt else b"Sin historial",
                           file_name="historial_balanceo.txt", mime="text/plain",
                           disabled=datos_txt is None, use_container_width=True)
    with col_e2:
        datos_pdf = exportar_como_pdf()
        st.download_button("↓  Descargar PDF", data=datos_pdf if datos_pdf else b"Sin historial",
                           file_name="historial_balanceo.pdf", mime="application/pdf",
                           disabled=datos_pdf is None, use_container_width=True)
