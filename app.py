import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Calculadora Lagrange", layout="wide")

st.title("🧮 Calculadora del Método Numérico de Lagrange")
st.write("Inserta tus puntos, define el valor a interpolar y observa el procedimiento paso a paso.")

# --- SECCIÓN 1: ENTRADA DE DATOS ---
st.header("1. Entrada de Puntos $(x_i, y_i)$")

# Por defecto ponemos 3 puntos (se pueden añadir más)
num_puntos = st.number_input("Número de puntos a ingresar:", min_value=2, max_value=10, value=3, step=1)

col1, col2 = st.columns(2)
x_puntos = []
y_puntos = []

with col1:
    st.subheader("Valores de X")
    for i in range(num_puntos):
        # Valores iniciales de ejemplo (0, 1, 2)
        val_x = st.number_input(f"x_{i}", value=float(i), key=f"x_{i}")
        x_puntos.append(val_x)

with col2:
    st.subheader("Valores de Y")
    # Valores iniciales de ejemplo (f(x) = x^2 por decir algo: 0, 1, 4)
    valores_y_defecto = [0.0, 1.0, 4.0] if num_puntos == 3 else [float(i**2) for i in range(num_puntos)]
    for i in range(num_puntos):
        val_y = st.number_input(f"y_{i}", value=valores_y_defecto[i] if i < len(valores_y_defecto) else float(i), key=f"y_{i}")
        y_puntos.append(val_y)

# Comprobación de que no haya X repetidas (requisito matemático de Lagrange)
if len(x_puntos) != len(set(x_puntos)):
    st.error("⚠️ Error: Los valores de X deben ser todos diferentes entre sí.")
    st.stop()

# Valor a evaluar
st.markdown("---")
x_interpolar = st.number_input("🎯 Valor de **x** que deseas interpolar/evaluar:", value=0.5)

# --- SECCIÓN 2: PROCESAMIENTO Y PASO A PASO ---
st.header("📝 Procedimiento Paso a Paso")

polinomios_base_valores = []
polinomios_base_formulas = []

# Calcular cada L_i(x)
for i in range(num_puntos):
    numerador_str = ""
    denominador_str = ""
    numerador_val = 1.0
    denominador_val = 1.0
    
    for j in range(num_puntos):
        if j != i:
            # Construcción de la cadena de texto (LaTeX) para la fórmula paso a paso
            numerador_str += f"({x_interpolar} - {x_puntos[j]})"
            denominador_str += f"({x_puntos[i]} - {x_puntos[j]})"
            
            # Cálculo matemático real
            numerador_val *= (x_interpolar - x_puntos[j])
            denominador_val *= (x_puntos[i] - x_puntos[j])
            
    val_l = numerador_val / denominador_val
    polinomios_base_valores.append(val_l)
    
    # Guardamos la representación visual en LaTeX
    formula_latex = f"L_{i}({x_interpolar}) = \\frac{{{numerador_str}}}{{{denominador_str}}} = \\frac{{{numerador_val:.4f}}}{{{denominador_val:.4f}}} = {val_l:.4f}"
    polinomios_base_formulas.append(formula_latex)

# Mostrar Polinomios Base
st.subheader("Paso 1: Calcular los Polinomios Base $L_i(x)$")
for formula in polinomios_base_formulas:
    st.latex(formula)

# Calcular el resultado final P(x)
st.subheader("Paso 2: Suma Ponderada $P(x) = \\sum y_i \\cdot L_i(x)$")

terminos_suma_str = ""
resultado_final = 0.0

for i in range(num_puntos):
    producto = y_puntos[i] * polinomios_base_valores[i]
    resultado_final += producto
    terminos_suma_str += f"({y_puntos[i]} \\cdot {polinomios_base_valores[i]:.4f})"
    if i < num_puntos - 1:
        terminos_suma_str += " + "

st.latex(f"P({x_interpolar}) = {terminos_suma_str}")
st.success(f"✨ **Resultado final:** $P({x_interpolar}) = {resultado_final:.6f}$")

# --- SECCIÓN 3: GRÁFICO INTERACTIVO ---
st.markdown("---")
st.header("📊 Visualización Gráfica")

# Función interna para evaluar cualquier punto X en el polinomio obtenido
def evaluar_lagrange(x_val):
    suma = 0.0
    for i in range(num_puntos):
        li = 1.0
        for j in range(num_puntos):
            if j != i:
                li *= (x_val - x_puntos[j]) / (x_puntos[i] - x_puntos[j])
        suma += y_puntos[i] * li
    return suma

# Generar una curva suave para el gráfico
margin = max(x_puntos) - min(x_puntos) if max(x_puntos) - min(x_puntos) != 0 else 1.0
x_curva = np.linspace(min(x_puntos) - margin*0.2, max(x_puntos) + margin*0.2, 200)
y_curva = [evaluar_lagrange(x) for x in x_curva]

# Construcción de la figura interactiva de Plotly
fig = go.Figure()

# Línea del polinomio
fig.add_trace(go.Scatter(x=x_curva, y=y_curva, mode='lines', name='Polinomio de Lagrange', line=dict(color='royalblue', width=3)))

# Puntos originales dados por el usuario
fig.add_trace(go.Scatter(x=x_puntos, y=y_puntos, mode='markers', name='Puntos Originales', marker=dict(color='red', size=12, symbol='circle')))

# Punto interpolado actual
fig.add_trace(go.Scatter(x=[x_interpolar], y=[resultado_final], mode='markers', name=f'Resultado P({x_interpolar})', marker=dict(color='gold', size=15, symbol='star')))

fig.update_layout(
    title=f"Curva de Interpolación que pasa por los {num_puntos} puntos",
    xaxis_title="Eje X",
    yaxis_title="Eje Y",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
