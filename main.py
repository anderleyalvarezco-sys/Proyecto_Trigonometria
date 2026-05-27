import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# =========================================================================
# 1. CONFIGURACIÓN DEL ENGINE Y PARADIGMA ESTÉTICO EXCLUSIVO BLANCO Y AZUL
# =========================================================================
st.set_page_config(
    page_title="Resolutor Matemático | Sistema Corporativo",
    page_icon="📊",
    layout="centered"
)

# Configuración global de Matplotlib para entornos claros e institucionales
plt.style.use('default')
plt.rcParams['text.color'] = '#1E3A8A'
plt.rcParams['axes.labelcolor'] = '#1E3A8A'
plt.rcParams['xtick.color'] = '#1E3A8A'
plt.rcParams['ytick.color'] = '#1E3A8A'

# Inyección de CSS Profesional: Exclusivo Blanco Puro y Tonos de Azul
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Fondo 100% Blanco Puro */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            background-image: none !important;
            color: #1E3A8A !important;
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, h4, .main-title {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* TÍTULO PRINCIPAL EN AZUL MARINO */
        .main-title {
            font-size: 38px;
            color: #1E3A8A;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* SUBTÍTULO EN AZUL COBALTO */
        .sub-title {
            color: #3B82F6;
            font-size: 15px;
            margin-bottom: 30px;
            font-weight: 400;
        }

        /* CONTENEDORES CON BORDE AZUL LIGERO */
        .glass-panel {
            background: #FFFFFF !important;
            border: 2px solid #EFF6FF;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.05);
        }

        /* ENTRADAS DE TEXTO CON ENFOQUE AZUL */
        div[data-testid="stTextInput"] > div > div > input {
            background-color: #FFFFFF !important;
            color: #1E3A8A !important;
            border: 1px solid #BFDBFE !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stTextInput"] > div > div > input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
        }
        
        label, p, div[data-testid="stWidgetLabel"] p {
            color: #1E40AF !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }

        div[data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #BFDBFE !important;
            color: #1E3A8A !important;
            border-radius: 8px !important;
        }

        /* BOTONES INTERACTIVOS EN AZUL REY */
        div.stButton > button:first-child {
            background: #2563EB !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
            width: 100%;
            margin-top: 10px;
        }
        div.stButton > button:first-child:hover {
            background: #1D4ED8 !important;
            transform: translateY(-1px) !important;
        }

        /* PESTAÑAS / TABS EN TONOS AZULES */
        div[data-testid="stTabs"] {
            background: transparent !important;
            gap: 4px !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab-list"] {
            background-color: #DBEAFE !important;
            padding: 4px !important;
            border-radius: 10px !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #1E40AF !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }
        div[data-testid="stTabs"] [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #2563EB !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
        }

        /* TARJETA DE SOLUCIÓN EN AZUL CIELO */
        .solucion-glow-card {
            background: #EFF6FF !important;
            border: 2px solid #BFDBFE;
            border-radius: 12px;
            padding: 20px;
            margin: 25px 0;
            text-align: center;
        }
        .solucion-value {
            font-size: 26px;
            font-weight: 700;
            color: #1E40AF;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>CALCULADORA DE SISTEMAS</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Motor de Computación Algebraica y Representation Geométrica</div>", unsafe_allow_html=True)

modulo = st.tabs(["Polinomios y Logaritmos", "Sistemas Lineales 2x2"])
transformaciones_inteligentes = standard_transformations + (implicit_multiplication_application, convert_xor)

# =========================================================================
# MÓDULO 1: CUADRÁTICAS Y LOGARÍTMICAS
# =========================================================================
with modulo[0]:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### Parámetros del Motor Numérico")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        metodo = st.selectbox("Algoritmo Operacional:", ["Fórmula General", "Factorización de Trinomio"])
    with col_c2:
        tipo_entrada = st.radio("Estructura Algebraica:", ["Polinomio Directo", "Ecuación Logarítmica"], horizontal=True)
        
    x = sp.symbols('x')
    local_dict = {'x': x, 'log': sp.log}
    proceder = False

    if tipo_entrada == "Polinomio Directo":
        st.markdown("<br><p style='margin-bottom:-10px;'>Configura la matriz polinomial para ax² + bx + c = 0</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: ent_a = st.text_input("Componente cuadrático [a]", value="1", key="quad_a")
        with c2: ent_b = st.text_input("Componente lineal [b]", value="-5", key="quad_b")
        with c3: ent_c = st.text_input("Término independiente [c]", value="6", key="quad_c")
        
        if st.button("EJECUTAR CÓMPUTO CUADRÁTICO"):
            try:
                a_val = sp.Rational(ent_a)
                b_val = sp.Rational(ent_b)
                c_val = sp.Rational(ent_c)
                if a_val == 0:
                    st.error("Inconsistencia: El coeficiente 'a' no puede ser 0.")
                else:
                    ecuacion_final = a_val*x**2 + b_val*x + c_val
                    soluciones_quad = sp.solve(sp.Eq(ecuacion_final, 0), x)
                    proceder = True
                    is_log = False
            except Exception as e: 
                st.error(f"Sintaxis analítica inválida: {e}")
                
    else: 
        st.markdown("<br>", unsafe_allow_html=True)
        ent_base = st.text_input("Base del Campo Logarítmico (b):", value="2", key="log_base")
        c_izq, c_der = st.columns(2)
        with c_izq: ent_izq = st.text_input("Miembro Izquierdo", value="log(x+2) + log(x+4)", key="log_izq")
        with c_der: ent_der = st.text_input("Miembro Derecho", value="3", key="log_der")
        
        if st.button("ANALIZAR ESTRUCTURA LOGARÍTMICA"):
            try:
                b = int(ent_base)
                if b <= 0 or b == 1: 
                    st.error("La base matemática debe cumplir b > 0 y b ≠ 1.")
                else:
                    txt_izq = ent_izq.replace(" ", "")
                    txt_der = ent_der.replace(" ", "")
                    
                    if "+" in txt_izq and txt_der.isdigit():
                        terminos = txt_izq.split("+")
                        arg1_txt = terminos[0].replace("log(", "").rstrip(")")
                        arg2_txt = terminos[1].replace("log(", "").rstrip(")")
                        
                        arg1 = parse_expr(arg1_txt, local_dict=local_dict, transformations=transformaciones_inteligentes)
                        arg2 = parse_expr(arg2_txt, local_dict=local_dict, transformations=transformaciones_inteligentes)
                        num_der = int(txt_der)
                        
                        polinomio_izq = sp.expand(arg1 * arg2)
                        num_exponenciado = b ** num_der
                        ecuacion_final = polinomio_izq - num_exponenciado
                    else:
                        izq_p = parse_expr(txt_izq, local_dict=local_dict, transformations=transformaciones_inteligentes)
                        der_p = parse_expr(txt_der, local_dict=local_dict, transformations=transformaciones_inteligentes)
                        ecuacion_final = izq_p - der_p
                        
                    ecuacion_poly = sp.Poly(ecuacion_final, x)
                    coeffs = ecuacion_poly.all_coeffs()
                    a_val, b_val, c_val = (coeffs[0], coeffs[1], coeffs[2]) if len(coeffs)==3 else (0, coeffs[0], coeffs[1]) if len(coeffs)==2 else (0,0,coeffs[0])
                    ecuacion_final = ecuacion_poly.as_expr()
                    soluciones_quad = sp.solve(sp.Eq(ecuacion_final, 0), x)
                    proceder = True
                    is_log = True
            except Exception as e: 
                st.error(f"Error de consistencia algebraica: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    if proceder:
        st.markdown("### Desarrollo Analítico Paso a Paso")
        
        if is_log:
            st.markdown("**Fase I: Transformación Exponencial**")
            st.latex(rf"\log_{{{b}}}({sp.latex(arg1)}) + \log_{{{b}}}({sp.latex(arg2)}) = {num_der}")
            st.markdown("Aplicando la propiedad del producto e igualando la base:")
            st.latex(rf"({sp.latex(arg1)}) \cdot ({sp.latex(arg2)}) = {b}^{{{num_der}}}")
            st.latex(rf"{sp.latex(polinomio_izq)} = {num_exponenciado}")
        
        st.markdown("**Fase II: Forma Canónica del Polinomio Resultante**")
        st.latex(rf"{sp.latex(a_val)}x^2 + ({sp.latex(b_val)})x + ({sp.latex(c_val)}) = 0")
        
        disc = b_val**2 - 4*a_val*c_val
        
        if metodo == "Fórmula General":
            st.markdown("1. **Identificación de Coeficientes:**")
            st.latex(rf"a = {a_val}, \quad b = {b_val}, \quad c = {c_val}")
            
            st.markdown("2. **Cálculo del Discriminante ($\Delta$):**")
            st.latex(rf"\Delta = b^2 - 4ac")
            st.latex(rf"\Delta = ({b_val})^2 - 4({a_val})({c_val}) = {disc}")
            
            if disc < 0:
                st.info("El discriminante es menor a cero. Las soluciones pertenecen al campo de los números complejos.")
            else:
                st.markdown("3. **Aplicación de la Fórmula General:**")
                st.latex(rf"x = \frac{{-b \pm \sqrt{{\Delta}}}}{{2a}}")
                st.latex(rf"x = \frac{{-({b_val}) \pm \sqrt{{{disc}}}}}{{2({a_val})}}")
                
                sqrt_disc = sp.sqrt(disc)
                st.markdown("Separando las raíces:")
                st.latex(rf"x_1 = \frac{{{-b_val} + {sqrt_disc}}}{{{2*a_val}}} = {soluciones_quad[0]}")
                if len(soluciones_quad) > 1:
                    st.latex(rf"x_2 = \frac{{{-b_val} - {sqrt_disc}}}{{{2*a_val}}} = {soluciones_quad[1]}")
        else:
            st.markdown("1. **Factorización del Trinomio:**")
            factores = sp.factor(ecuacion_final)
            st.latex(rf"{sp.latex(factores)} = 0")
            st.markdown("2. **Despeje de raíces independientes:**")
            for i, sol in enumerate(soluciones_quad):
                st.latex(rf"x_{i+1} = {sol}")
                    
        if is_log and disc >= 0:
            st.markdown("**Fase III: Validación de Dominio (Argumentos > 0)**")
            sol_finales = []
            for sol in soluciones_quad:
                try:
                    if arg1.subs(x, sol) > 0 and arg2.subs(x, sol) > 0:
                        sol_finales.append(sol)
                        st.info(rf"Raíz x = {sol} es válida. Mantiene los argumentos positivos.")
                    else:
                        st.info(rf"Raíz x = {sol} descartada. Produce un argumento negativo o indefinido.")
                except: pass
            
            st.markdown(f"<div class='solucion-glow-card'><div style='color:#1E40AF; font-size:14px; font-weight:600;'>CONJUNTO SOLUCIÓN GLOBAL DEPURADO</div><div class='solucion-value'>S = {sol_finales}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='solucion-glow-card'><div style='color:#1E40AF; font-size:14px; font-weight:600;'>CONJUNTO SOLUCIÓN GLOBAL</div><div class='solucion-value'>S = {list(soluciones_quad)}</div></div>", unsafe_allow_html=True)
            
        try:
            st.markdown("### Representación Geométrica")
            a_f = float(a_val if a_val != 0 else 1)
            b_f = float(b_val)
            v_x = -b_f / (2 * a_f)
            x_v = np.linspace(v_x - 6, v_x + 6, 200)
            y_v = float(a_val)*x_v**2 + float(b_val)*x_v + float(c_val)
            
            fig, ax = plt.subplots(figsize=(6, 3.8))
            fig.patch.set_facecolor('#FFFFFF')  
            ax.set_facecolor('#FFFFFF')         
            
            ax.plot(x_v, y_v, color="#2563EB", linewidth=2.5, label="Función F(x)")
            ax.axhline(0, color='#BFDBFE', linewidth=1, linestyle='--')
            ax.axvline(0, color='#BFDBFE', linewidth=1, linestyle='--')
            
            ax.spines['bottom'].set_color('#1E40AF')
            ax.spines['left'].set_color('#1E40AF')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(colors='#1E3A8A', labelsize=9)
            ax.grid(True, linestyle=':', color='#BFDBFE')
            ax.legend(facecolor='#FFFFFF', edgecolor='#BFDBFE', labelcolor='#1E3A8A')
            st.pyplot(fig)
        except Exception as e: 
            st.caption(f"Error gráfico: {e}")

# =========================================================================
# MÓDULO 2: SISTEMAS DE ECUACIONES (2x2)
# =========================================================================
with modulo[1]:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### Configuración de Sistemas Multivariable")
    metodo_sist = st.selectbox("Estrategia de Resolución Sistémica:", ["Sustitución", "Igualación", "Reducción"])
    
    st.markdown("<p style='margin-top:10px; color:#2563EB !important;'>Ingrese el sistema de ecuaciones de forma libre tradicional (ej: '2x + 3y = 20').</p>", unsafe_allow_html=True)
    c_sys1, c_sys2 = st.columns(2)
    with c_sys1: ent_eq1 = st.text_input("Ecuación de la Recta [1]:", value="2x + 3y = 20", key="sys_eq1")
    with c_sys2: ent_eq2 = st.text_input("Ecuación de la Recta [2]:", value="x - 2y = 3", key="sys_eq2")
    
    if st.button("PROCESAR SISTEMA LINEAL"):
        if "=" not in ent_eq1 or "=" not in ent_eq2:
            st.error("Ambos campos deben contener el signo igual '='.")
        else:
            try:
                t1 = ent_eq1.split("=")
                t2 = ent_eq2.split("=")
                x, y = sp.symbols('x y')
                local_dict_sys = {'x': x, 'y': y}
                
                izq1 = parse_expr(t1[0], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                der1 = parse_expr(t1[1], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                izq2 = parse_expr(t2[0], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                der2 = parse_expr(t2[1], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                
                exp1, exp2 = izq1 - der1, izq2 - der2
                a1, b1, c1 = exp1.coeff(x), exp1.coeff(y), -exp1.subs({x: 0, y: 0})
                a2, b2, c2 = exp2.coeff(x), exp2.coeff(y), -exp2.subs({x: 0, y: 0})
                
                solucion = sp.solve((sp.Eq(izq1, der1), sp.Eq(izq2, der2)), (x, y))
                
                if not solucion:
                    st.info("Las rectas son paralelas o incompatibles. No existe punto de intersección.")
                else:
                    val_x, val_y = solucion[x], solucion[y]
                    st.markdown("### Desarrollo Analítico Completo")
                    
                    st.markdown("**Sistema Reducido Canónico:**")
                    st.latex(rf"\begin{{cases}} {a1}x + ({b1})y = {c1} \\ {a2}x + ({b2})y = {c2} \end{{cases}}")
                    
                    if metodo_sist == "Sustitución":
                        des_x = sp.solve(sp.Eq(izq1, der1), x)[0]
                        st.markdown("1. **Despeje de $x$ en la primera ecuación:**")
                        st.latex(rf"x = {sp.latex(des_x)}")
                        
                        st.markdown("2. **Sustitución en la segunda ecuación:**")
                        expr_sustituda_izq = izq2.subs(x, des_x)
                        st.latex(rf"{sp.latex(a2)}\left({sp.latex(des_x)}\right) + ({b2})y = {c2}")
                        st.markdown("Simplificando los términos:")
                        st.latex(rf"{sp.latex(sp.simplify(expr_sustituda_izq))} = {c2}")
                        st.latex(rf"y = {val_y}")
                        
                        st.markdown("3. **Sustitución inversa para hallar $x$:**")
                        st.latex(rf"x = {sp.latex(des_x.subs(y, val_y))} \implies x = {val_x}")

                    elif metodo_sist == "Igualación":
                        des_x1 = sp.solve(sp.Eq(izq1, der1), x)[0]
                        des_x2 = sp.solve(sp.Eq(izq2, der2), x)[0]
                        st.markdown("1. **Despeje de la misma incógnita ($x$) en ambas ecuaciones:**")
                        st.latex(rf"x = {sp.latex(des_x1)}")
                        st.latex(rf"x = {sp.latex(des_x2)}")
                        
                        st.markdown("2. **Igualación de términos:**")
                        st.latex(rf"{sp.latex(des_x1)} = {sp.latex(des_x2)}")
                        st.markdown("Agrupando y resolviendo $y$:")
                        st.latex(rf"y = {val_y}")
                        
                        st.markdown("3. **Evaluación final:**")
                        st.latex(rf"x = {sp.latex(des_x1.subs(y, val_y))} \implies x = {val_x}")

                    else: 
                        st.markdown("1. **Estandarización de coeficientes cruzados para eliminar $x$:**")
                        st.markdown(f"Multiplicamos la ecuación 1 por ${a2}$ y la ecuación 2 por ${a1}$:")
                        st.latex(rf"\begin{{cases}} {a1*a2}x + ({b1*a2})y = {c1*a2} \\ {a2*a1}x + ({b2*a1})y = {c2*a1} \end{{cases}}")
                        
                        st.markdown("2. **Resta de ecuaciones para anular el vector lineal:**")
                        st.latex(rf"({b1*a2 - b2*a1})y = {c1*a2 - c2*a1}")
                        st.latex(rf"y = {val_y}")
                        
                        st.markdown("3. **Sustitución en ecuación primitiva:**")
                        st.latex(rf"{a1}x + ({b1})({val_y}) = {c1} \implies x = {val_x}")
                    
                    st.markdown(f"""
                        <div class='solucion-glow-card'>
                            <div style='color:#1E40AF; font-size:14px; font-weight:600;'>COORDENADA VECTORIAL DE INTERSECCIÓN</div>
                            <div class='solucion-value'>Punto Solución P = ({val_x} , {val_y})</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.markdown("### Geometría del Vector Intersección")
                        x_num = float(val_x)
                        x_vals = np.linspace(x_num - 5, x_num + 5, 100)
                        
                        fig, ax = plt.subplots(figsize=(6, 4))
                        fig.patch.set_facecolor('#FFFFFF') 
                        ax.set_facecolor('#FFFFFF')        
                        
                        if b1 != 0:
                            y_vals1 = [float((c1 - a1*kv) / b1) for kv in x_vals]
                            ax.plot(x_vals, y_vals1, color="#2563EB", linewidth=2.5, label="Recta [1]")
                        else: 
                            ax.axvline(float(c1/a1), color="#2563EB", linewidth=2.5, label="Recta [1]")
                            
                        if b2 != 0:
                            y_vals2 = [float((c2 - a2*kv) / b2) for kv in x_vals]
                            ax.plot(x_vals, y_vals2, color="#3B82F6", linewidth=2.5, label="Recta [2]")
                        else: 
                            ax.axvline(float(c2/a2), color="#3B82F6", linewidth=2.5, label="Recta [2]")
                        
                        ax.scatter(float(val_x), float(val_y), color="#1D4ED8", s=140, zorder=5, label=f"Intersección P({val_x}, {val_y})", edgecolors='#1E3A8A')
                        
                        ax.axhline(0, color='#BFDBFE', linewidth=0.8, linestyle='--')
                        ax.axvline(0, color='#BFDBFE', linewidth=0.8, linestyle='--')
                        
                        ax.spines['bottom'].set_color('#1E40AF')
                        ax.spines['left'].set_color('#1E40AF')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.tick_params(colors='#1E3A8A', labelsize=9)
                        ax.grid(True, linestyle=':', color='#BFDBFE')
                        ax.legend(facecolor='#FFFFFF', edgecolor='#BFDBFE', labelcolor='#1E3A8A')
                        st.pyplot(fig)
                    except Exception as e:
                        st.caption(f"Aviso gráfico: Render acotado ({e})")
                        
            except Exception as e: 
                st.error(f"Error crítico lineal: {e}")
    st.markdown("</div>", unsafe_allow_html=True)
