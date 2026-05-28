import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Calculadora Lagrange", layout="wide")

st.title("🧮 Calculadora del Método Numérico de Lagrange")
st.write("Inserta tus puntos, define el valor a interpolar y observa el procedimiento paso a paso.")

# --- SECCIÓN 1: ENTRADA DE DATOS ---
st.header("1. Entrada de Puntos $(x_i, y_i)$")

num_puntos = st.number_input("Número de puntos a ingresar:", min_value=2, max_value=10, value=3, step=1)

col1, col2 = st.columns(2)
x_puntos = []
y_puntos = []

with col1:
    st.subheader("Valores de X")
    for i in range(num_puntos):
        val_x = st.number_input(f"x_{i}", value=float(i), key=f"x_{i}")
        x_puntos.append(val_x)

with col2:
    st.subheader("Valores de Y")
    valores_y_defecto = [0.0, 1.0, 4.0] if num_puntos == 3 else [float(i**2) for i in range(num_puntos)]
    for i in range(num_puntos):
        val_y = st.number_input(f"y_{i}", value=valores_y_defecto[i] if i < len(valores_y_defecto) else float(i), key=f"y_{i}")
        y_puntos.append(val_y)

if len(x_puntos) != len(set(x_puntos)):
    st.error("⚠️ Error: Los valores de X deben ser todos diferentes entre sí.")
    st.stop()

st.markdown("---")
x_interpolar = st.number_input("🎯 Valor de **x** que deseas interpolar/evaluar:", value=0.5)

# --- SECCIÓN 2: OBTENCIÓN DEL POLINOMIO SIMBÓLICO (SYM PY) ---
st.header("✨ Expresión Analítica del Polinomio")

# Definimos la variable x como un símbolo algebraico
x = sp.Symbol('x')
polinomio_simbolico = 0

for i in range(num_puntos):
    li_simbolico = 1
    for j in range(num_puntos):
        if j != i:
            li_simbolico *= (x - x_puntos[j]) / (x_puntos[i] - x_puntos[j])
    polinomio_simbolico += y_puntos[i] * li_simbolico

# Simplificamos algebraicamente la expresión expandiéndola
polinomio_simplificado = sp.expand(polinomio_simbolico)

# Mostramos el polinomio usando formato LaTeX limpio
st.write("A partir de los puntos ingresados, el polinomio único de interpolación resultante es:")
st.latex(f"P(x) = {sp.latex(polinomio_simplificado)}")


# --- SECCIÓN 3: PROCESAMIENTO EVALUACIÓN PASO A PASO ---
st.markdown("---")
st.header("📝 Evaluación Paso a Paso en $x = " + str(x_interpolar) + "$")

polinomios_base_valores = []
polinomios_base_formulas = []

for i in range(num_puntos):
    numerador_str = ""
    denominador_str = ""
    numerador_val = 1.0
    denominador_val = 1.0
    
    for j in range(num_puntos):
        if j != i:
            numerador_str += f"({x_interpolar} - {x_puntos[j]})"
            denominador_str += f"({x_puntos[i]} - {x_puntos[j]})"
            numerador_val *= (x_interpolar - x_puntos[j])
            denominador_val *= (x_puntos[i] - x_puntos[j])
            
    val_l = numerador_val / denominador_val
    polinomios_base_valores.append(val_l)
    
    formula_latex = f"L_{i}({x_interpolar}) = \\frac{{{numerador_str}}}{{{denominador_str}}} = \\frac{{{numerador_val:.4f}}}{{{denominador_val:.4f}}} = {val_l:.4f}"
    polinomios_base_formulas.append(formula_latex)

st.subheader("Paso 1: Calcular los Polinomios Base $L_i(x)$")
for formula in polinomios_base_formulas:
    st.latex(formula)

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
st.success(f"✨ **Resultado de la evaluación:** $P({x_interpolar}) = {resultado_final:.6f}$")


# --- SECCIÓN 4: GRÁFICO INTERACTIVO ---
st.markdown("---")
st.header("📊 Visualización Gráfica")

def evaluar_lagrange(x_val):
    suma = 0.0
    for i in range(num_puntos):
        li = 1.0
        for j in range(num_puntos):
            if j != i:
                li *= (x_val - x_puntos[j]) / (x_puntos[i] - x_puntos[j])
        suma += y_puntos[i] * li
    return suma

margin = max(x_puntos) - min(x_puntos) if max(x_puntos) - min(x_puntos) != 0 else 1.0
x_curva = np.linspace(min(x_puntos) - margin*0.2, max(x_puntos) + margin*0.2, 200)
y_curva = [evaluar_lagrange(x) for x in x_curva]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_curva, y=y_curva, mode='lines', name='Polinomio de Lagrange', line=dict(color='royalblue', width=3)))
fig.add_trace(go.Scatter(x=x_puntos, y=y_puntos, mode='markers', name='Puntos Originales', marker=dict(color='red', size=12, symbol='circle')))
fig.add_trace(go.Scatter(x=[x_interpolar], y=[resultado_final], mode='markers', name=f'Resultado P({x_interpolar})', marker=dict(color='gold', size=15, symbol='star')))

fig.update_layout(
    title=f"Curva del polinomio obtenido",
    xaxis_title="Eje X",
    yaxis_title="Eje Y",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
