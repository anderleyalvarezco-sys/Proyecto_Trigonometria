import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(
    page_title="MathCore | Motor Analítico",
    page_icon="",
    layout="centered"
)

plt.style.use('dark_background')

# =========================================================================
# SPLASH SCREEN
# =========================================================================
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    # CSS para ocultar todo Streamlit y el botón trigger
    st.markdown("""
    <style>
        header {visibility:hidden;}
        footer {visibility:hidden;}
        body, [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > .block-container {
            background:#07111F !important;
            padding:0 !important;
            max-width:100% !important;
        }
        [data-testid="stVerticalBlock"] { gap:0 !important; }
        /* Ocultar completamente el botón trigger */
        div[data-testid="stButton"] {
            position:absolute !important;
            opacity:0 !important;
            pointer-events:none !important;
            height:0 !important;
            overflow:hidden !important;
        }
        /* Expandir iframe a pantalla completa */
        iframe {
            display:block !important;
            width:100vw !important;
            min-width:100vw !important;
            border:none !important;
            margin-left:calc(-50vw + 50%) !important;
            background:#07111F !important;
        }
    </style>
    """, unsafe_allow_html=True)

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    width:100%; height:100vh;
    background:#07111F;
    display:flex; align-items:center; justify-content:center;
    overflow:hidden;
  }
  canvas { position:absolute; inset:0; width:100%; height:100%; }
  .wrap { position:relative; z-index:2; text-align:center; }

  #si {
    opacity:0; transform:scale(0.3);
    transition: opacity .7s cubic-bezier(.34,1.56,.64,1),
                transform .7s cubic-bezier(.34,1.56,.64,1);
    margin-bottom:22px;
  }
  #si.on { opacity:1; transform:scale(1); }
  .ibox {
    width:130px; height:130px; margin:0 auto; border-radius:28px;
    background:#0b1a2e;
    border: 2px solid #1e3a5f;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 0 60px rgba(37,99,255,.55), 0 0 120px rgba(124,58,237,.2);
  }
  #st2 {
    opacity:0; transform:translateY(26px);
    transition: opacity .7s ease .35s, transform .7s ease .35s;
  }
  #st2.on { opacity:1; transform:translateY(0); }
  .tn {
    font-size:46px; font-weight:700; font-family:'Space Grotesk',sans-serif;
    background:linear-gradient(135deg,#06B6D4 0%,#2563FF 50%,#7C3AED 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    letter-spacing:-.03em; margin-bottom:7px;
  }
  .ts { color:#475569; font-size:11.5px; letter-spacing:.13em; text-transform:uppercase; font-family:'Inter',sans-serif; }

  #sb { margin-top:46px; opacity:0; transition: opacity .5s ease .9s; }
  #sb.on { opacity:1; }
  .trk { width:210px; height:2px; background:rgba(148,163,184,.1); border-radius:2px; overflow:hidden; margin:0 auto; }
  #sf {
    height:100%; width:0%;
    background:linear-gradient(90deg,#06B6D4,#2563FF,#7C3AED);
    border-radius:2px; transition:width 2.2s cubic-bezier(.4,0,.2,1) .1s;
  }
  #sm { color:#334155; font-size:11px; margin-top:13px; font-family:monospace; letter-spacing:.07em; transition:opacity .25s; }

  /* Salida: fade + scale hacia arriba, como abrir una app */
  body.exit {
    animation: openApp .85s cubic-bezier(.4,0,.2,1) forwards;
  }
  @keyframes openApp {
    0%   { opacity:1; transform:scale(1)    translateY(0);   }
    100% { opacity:0; transform:scale(1.12) translateY(-24px); }
  }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div class="wrap">
  <div id="si">
    <div class="ibox">
<svg width="80" height="80" viewBox="-36 -36 72 72" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ic1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22D3EE"/><stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="ic2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2563FF"/>
    </linearGradient>
    <linearGradient id="ic3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>
  <rect x="-28" y="-28" width="17" height="17" fill="url(#ic1)" rx="4"/>
  <rect x="-9"  y="-28" width="17" height="17" fill="url(#ic1)" rx="4"/>
  <rect x="10"  y="-28" width="17" height="17" fill="url(#ic1)" rx="4"/>
  <rect x="-28" y="-9"  width="17" height="17" fill="url(#ic2)" rx="4"/>
  <rect x="-9"  y="-9"  width="17" height="17" fill="rgba(14,32,56,0.8)" rx="4"/>
  <rect x="10"  y="-9"  width="17" height="17" fill="rgba(14,32,56,0.8)" rx="4"/>
  <rect x="-28" y="10"  width="17" height="17" fill="url(#ic3)" rx="4"/>
  <rect x="-9"  y="10"  width="17" height="17" fill="url(#ic3)" rx="4"/>
  <rect x="10"  y="10"  width="17" height="17" fill="url(#ic3)" rx="4"/>
  <circle cx="19"  cy="-20" r="3.5" fill="#06B6D4"/>
  <circle cx="19"  cy="19"  r="3.5" fill="#7C3AED"/>
  <circle cx="-5"  cy="0"   r="3"   fill="#2563FF"/>
</svg>
    </div>
  </div>
  <div id="st2">
    <div class="tn">MathCore</div>
    <div class="ts">Motor Analítico Avanzado</div>
  </div>
  <div id="sb">
    <div class="trk"><div id="sf"></div></div>
    <div id="sm">Iniciando módulos...</div>
  </div>
</div>

<script>
// Partículas
var cv=document.getElementById('c'), ctx=cv.getContext('2d');
cv.width=window.innerWidth; cv.height=window.innerHeight;
var pts=[];
for(var i=0;i<60;i++) pts.push({
  x:Math.random()*cv.width, y:Math.random()*cv.height,
  vx:(Math.random()-.5)*.5, vy:(Math.random()-.5)*.5,
  r:Math.random()*1.7+.4, a:Math.random()*.5+.2
});
function dp(){
  ctx.clearRect(0,0,cv.width,cv.height);
  pts.forEach(function(p,i){
    p.x+=p.vx; p.y+=p.vy;
    if(p.x<0)p.x=cv.width; if(p.x>cv.width)p.x=0;
    if(p.y<0)p.y=cv.height; if(p.y>cv.height)p.y=0;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle='rgba(37,99,255,'+p.a*.45+')'; ctx.fill();
    pts.slice(i+1).forEach(function(q){
      var d=Math.hypot(p.x-q.x,p.y-q.y);
      if(d<90){ ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y);
        ctx.strokeStyle='rgba(124,58,237,'+(1-d/90)*.13+')';
        ctx.lineWidth=.5; ctx.stroke(); }
    });
  });
  requestAnimationFrame(dp);
}
dp();

// Entrada
var msgs=["Iniciando módulos...","Cargando motor simbólico...","Preparando interfaz...","Listo."], ph=0;
function nm(){
  var el=document.getElementById('sm'); if(!el||ph>=msgs.length)return;
  el.style.opacity='0';
  setTimeout(function(){ el.textContent=msgs[ph]; el.style.opacity='1'; ph++; },260);
}
setTimeout(function(){ document.getElementById('si').classList.add('on'); },200);
setTimeout(function(){ document.getElementById('st2').classList.add('on'); },540);
setTimeout(function(){
  document.getElementById('sb').classList.add('on');
  setTimeout(function(){ document.getElementById('sf').style.width='100%'; },80);
},980);
var iv=setInterval(function(){ nm(); if(ph>=msgs.length)clearInterval(iv); },650);

// Animación de salida — Python hace el rerun con time.sleep
setTimeout(function(){
  document.body.classList.add('exit');
}, 3200);
</script>
</body>
</html>
""", height=760, scrolling=False)

    import time
    time.sleep(4.2)
    st.session_state.splash_done = True
    st.rerun()

# =========================================================================
# CSS PRINCIPAL
# =========================================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #07111F !important;
            background-image:
                radial-gradient(at 0% 0%, rgba(124,58,237,0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(37,99,255,0.12) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(6,182,212,0.05) 0px, transparent 70%) !important;
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif;
            animation: bgPulse 8s ease-in-out infinite alternate !important;
        }
        @keyframes bgPulse {
            0% {
                background-image:
                    radial-gradient(at 0% 0%,   rgba(124,58,237,0.18) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(37,99,255,0.14) 0px, transparent 50%),
                    radial-gradient(at 50% 50%,  rgba(6,182,212,0.06) 0px, transparent 70%) !important;
            }
            33% {
                background-image:
                    radial-gradient(at 20% 80%,  rgba(37,99,255,0.16) 0px, transparent 55%),
                    radial-gradient(at 80% 20%,  rgba(124,58,237,0.13) 0px, transparent 50%),
                    radial-gradient(at 50% 50%,  rgba(6,182,212,0.07) 0px, transparent 65%) !important;
            }
            66% {
                background-image:
                    radial-gradient(at 80% 10%,  rgba(6,182,212,0.12) 0px, transparent 50%),
                    radial-gradient(at 10% 90%,  rgba(124,58,237,0.16) 0px, transparent 55%),
                    radial-gradient(at 50% 50%,  rgba(37,99,255,0.06) 0px, transparent 70%) !important;
            }
            100% {
                background-image:
                    radial-gradient(at 100% 0%,  rgba(37,99,255,0.15) 0px, transparent 50%),
                    radial-gradient(at 0% 100%,  rgba(6,182,212,0.11) 0px, transparent 50%),
                    radial-gradient(at 50% 50%,  rgba(124,58,237,0.07) 0px, transparent 70%) !important;
            }
        }
        h1,h2,h3,h4,.main-title { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-0.03em; }
        header {visibility:hidden;} footer {visibility:hidden;}
        .header-logo {
            animation: logoAppear 0.6s cubic-bezier(0.34,1.56,0.64,1) forwards;
            opacity:0;
        }
        @keyframes logoAppear {
            0%   { opacity:0; transform:scale(0.5); }
            100% { opacity:1; transform:scale(1); }
        }
        .main-title {
            font-size:40px; font-weight:700;
            background:linear-gradient(135deg,#06B6D4 0%,#2563FF 50%,#7C3AED 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            margin-bottom:2px; display:inline-block;
            opacity:0; clip-path:inset(0 100% 0 0);
            animation: slideFromLogo 0.7s cubic-bezier(0.4,0,0.2,1) 0.5s forwards;
        }
        @keyframes slideFromLogo {
            0%   { opacity:0; clip-path:inset(0 100% 0 0); transform:translateX(-12px); }
            30%  { opacity:1; }
            100% { opacity:1; clip-path:inset(0 0% 0 0);   transform:translateX(0); }
        }
        .sub-title { color:#94A3B8; font-size:15px; margin-bottom:30px; font-weight:400; }
        .glass-panel {
            background:rgba(15,23,42,0.65) !important;
            backdrop-filter:blur(16px) saturate(180%);
            border:1px solid rgba(148,163,184,0.12);
            border-radius:16px; padding:24px; margin-bottom:25px;
            box-shadow:0 8px 32px 0 rgba(0,0,0,0.37);
        }
        div[data-testid="stTextInput"] > div > div > input {
            background-color:#0F172A !important; color:#E2E8F0 !important;
            border:1px solid rgba(148,163,184,0.2) !important;
            border-radius:10px !important; padding:12px 16px !important;
            font-family:'Space Grotesk',monospace !important; font-size:15px !important;
        }
        div[data-testid="stTextInput"] > div > div > input:focus {
            border-color:#2563FF !important;
            box-shadow:0 0 15px rgba(37,99,255,0.35) !important;
            background-color:#07111F !important;
        }
        label,p,div[data-testid="stWidgetLabel"] p {
            color:#94A3B8 !important; font-weight:500 !important; font-size:14px !important;
        }
        div[data-testid="stSelectbox"] > div > div {
            background-color:#0F172A !important;
            border:1px solid rgba(148,163,184,0.2) !important;
            color:#E2E8F0 !important; border-radius:10px !important;
        }
        div.stButton > button:first-child {
            background:linear-gradient(135deg,#2563FF 0%,#7C3AED 100%) !important;
            color:#FFFFFF !important; border-radius:12px !important;
            border:none !important; padding:14px 28px !important;
            font-family:'Space Grotesk',sans-serif !important; font-size:15px !important;
            font-weight:600 !important; letter-spacing:0.02em;
            box-shadow:0 4px 15px rgba(124,58,237,0.3) !important;
            width:100%; margin-top:10px;
        }
        div.stButton > button:first-child:hover {
            transform:translateY(-2px) !important;
            box-shadow:0 0 25px rgba(37,99,255,0.5) !important;
            filter:brightness(1.1);
        }
        div[data-testid="stTabs"] [data-baseweb="tab-list"] {
            background-color:#0F172A !important;
            border:1px solid rgba(148,163,184,0.1) !important;
            padding:6px !important; border-radius:14px !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab"] {
            background-color:transparent !important; color:#94A3B8 !important;
            padding:10px 20px !important; border-radius:10px !important;
            font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important;
        }
        div[data-testid="stTabs"] [aria-selected="true"] {
            background:linear-gradient(135deg,rgba(37,99,255,0.15),rgba(124,58,237,0.15)) !important;
            color:#06B6D4 !important; border:1px solid rgba(6,182,212,0.3) !important;
        }
        .solucion-glow-card {
            background:linear-gradient(135deg,rgba(7,17,31,0.95) 0%,rgba(15,23,42,0.9) 100%) !important;
            border:1px solid rgba(37,99,255,0.3); border-radius:14px;
            padding:22px; margin:25px 0;
            box-shadow:0 0 30px rgba(37,99,255,0.15); text-align:center;
        }
        .solucion-value {
            font-family:'Space Grotesk',sans-serif !important; font-size:28px; font-weight:700;
            background:linear-gradient(90deg,#06B6D4,#2563FF);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-top:5px;
        }
        .step-anim {
            animation: stepIn 0.55s ease both;
        }
        .step-anim:nth-child(1)  { animation-delay: 0.05s; }
        .step-anim:nth-child(2)  { animation-delay: 0.42s; }
        .step-anim:nth-child(3)  { animation-delay: 0.80s; }
        .step-anim:nth-child(4)  { animation-delay: 1.18s; }
        .step-anim:nth-child(5)  { animation-delay: 1.56s; }
        .step-anim:nth-child(6)  { animation-delay: 1.94s; }
        .step-anim:nth-child(7)  { animation-delay: 2.32s; }
        .step-anim:nth-child(8)  { animation-delay: 2.70s; }
        @keyframes stepIn {
            from { opacity:0; transform:translateY(18px); }
            to   { opacity:1; transform:translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)



# =========================================================================
# ENCABEZADO
# =========================================================================
st.markdown("""
<div style='display:flex;align-items:center;gap:16px;margin-bottom:2px;'>
  <div class='header-logo' style='width:52px;height:52px;border-radius:14px;background:#0b1a2e;border:1.5px solid #1e3a5f;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 20px rgba(37,99,255,0.3);'>
    <svg width="36" height="36" viewBox="-36 -36 72 72" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="h1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#22D3EE"/><stop offset="100%" stop-color="#06B6D4"/></linearGradient>
        <linearGradient id="h2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2563FF"/></linearGradient>
        <linearGradient id="h3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient>
      </defs>
      <rect x="-28" y="-28" width="17" height="17" fill="url(#h1)" rx="4"/>
      <rect x="-9"  y="-28" width="17" height="17" fill="url(#h1)" rx="4"/>
      <rect x="10"  y="-28" width="17" height="17" fill="url(#h1)" rx="4"/>
      <rect x="-28" y="-9"  width="17" height="17" fill="url(#h2)" rx="4"/>
      <rect x="-9"  y="-9"  width="17" height="17" fill="rgba(14,32,56,0.9)" rx="4"/>
      <rect x="10"  y="-9"  width="17" height="17" fill="rgba(14,32,56,0.9)" rx="4"/>
      <rect x="-28" y="10"  width="17" height="17" fill="url(#h3)" rx="4"/>
      <rect x="-9"  y="10"  width="17" height="17" fill="url(#h3)" rx="4"/>
      <rect x="10"  y="10"  width="17" height="17" fill="url(#h3)" rx="4"/>
      <circle cx="19" cy="-20" r="3" fill="#06B6D4"/>
      <circle cx="19" cy="19"  r="3" fill="#7C3AED"/>
      <circle cx="-5" cy="0"   r="2.5" fill="#2563FF"/>
    </svg>
  </div>
  <div class='main-title'>MathCore</div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Motor Analítico Avanzado &nbsp;·&nbsp; Resolución Paso a Paso</div>", unsafe_allow_html=True)

modulo = st.tabs(["Polinomios y Logaritmos", "Sistemas Lineales 2x2"])
transformaciones_inteligentes = standard_transformations + (implicit_multiplication_application, convert_xor)

def explicacion(texto):
    st.markdown(f"> *{texto}*")

# =========================================================================
# MODULO 1
# =========================================================================
with modulo[0]:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### Parametros de entrada")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        metodo = st.selectbox("Metodo de resolucion:", ["Formula General (Bachiller)", "Factorizacion de Trinomio"])
    with col_c2:
        tipo_entrada = st.radio("Tipo de ecuacion:", ["Polinomio Directo", "Ecuacion Logaritmica"], horizontal=True)

    x = sp.symbols('x')
    local_dict = {'x': x, 'log': sp.log}
    proceder = False

    if tipo_entrada == "Polinomio Directo":
        st.markdown("<br><p style='margin-bottom:-10px;'>Ingresa los coeficientes de ax² + bx + c = 0</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: ent_a = st.text_input("Coeficiente a", value="1", key="quad_a")
        with c2: ent_b = st.text_input("Coeficiente b", value="-5", key="quad_b")
        with c3: ent_c = st.text_input("Coeficiente c", value="6", key="quad_c")

        if st.button("Resolver ecuacion cuadratica"):
            try:
                a_val = sp.Rational(ent_a)
                b_val = sp.Rational(ent_b)
                c_val = sp.Rational(ent_c)
                LIMITE = 10**6
                if a_val == 0:
                    st.error("El coeficiente 'a' no puede ser 0.")
                elif abs(a_val) > LIMITE or abs(b_val) > LIMITE or abs(c_val) > LIMITE:
                    st.error("Los coeficientes son demasiado grandes. Usa valores menores a 1,000,000.")
                else:
                    ecuacion_final = a_val*x**2 + b_val*x + c_val
                    soluciones_quad = sp.solve(sp.Eq(ecuacion_final, 0), x)
                    proceder = True
                    is_log = False
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        ent_base = st.text_input("Base del logaritmo (b):", value="2", key="log_base")
        c_izq, c_der = st.columns(2)
        with c_izq: ent_izq = st.text_input("Miembro izquierdo", value="log(x+2) + log(x+4)", key="log_izq")
        with c_der: ent_der = st.text_input("Miembro derecho", value="3", key="log_der")

        if st.button("Resolver ecuacion logaritmica"):
            try:
                b = int(ent_base)
                if b <= 0 or b == 1:
                    st.error("La base debe cumplir b > 0 y b distinto de 1.")
                elif b > 10**6:
                    st.error("La base es demasiado grande. Usa un valor menor a 1,000,000.")
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
                st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    if proceder:
        st.markdown("### Desarrollo paso a paso")
        st.markdown("""
<script>
(function(){
  function animateSteps(){
    var steps = document.querySelectorAll('.step-anim');
    steps.forEach(function(s){ s.classList.remove('visible'); });
    steps.forEach(function(s, i){
      setTimeout(function(){ s.classList.add('visible'); }, 120 + i * 380);
    });
  }
  // Esperar a que Streamlit renderice los elementos
  setTimeout(animateSteps, 300);
})();
</script>
""", unsafe_allow_html=True)
        if is_log:
            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso 1 — Transformacion exponencial**")
            explicacion(r"Aplicamos la propiedad del producto: $\log(a) + \log(b) = \log(a \cdot b)$. Luego, si $\log_b(\text{expr}) = n$, la expresión equivale a $b^n$.")
            st.latex(rf"\log_{{{b}}}({sp.latex(arg1)}) + \log_{{{b}}}({sp.latex(arg2)}) = {num_der}")
            st.latex(rf"({sp.latex(arg1)}) \cdot ({sp.latex(arg2)}) = {b}^{{{num_der}}}")
            st.latex(rf"{sp.latex(polinomio_izq)} = {num_exponenciado}")

        st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
        st.markdown("**Paso 2 — Forma canonica**")
        explicacion(r"Pasamos todo al lado izquierdo para obtener $ax^2 + bx + c = 0$, la forma estándar necesaria para cualquier método.")
        st.latex(rf"{sp.latex(a_val)}x^2 + ({sp.latex(b_val)})x + ({sp.latex(c_val)}) = 0")
        disc = b_val**2 - 4*a_val*c_val

        if metodo == "Formula General (Bachiller)":
            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso 3 — Identificacion de coeficientes**")
            explicacion(r"Identificamos $a$, $b$ y $c$: el coeficiente $a$ acompaña a $x^2$, $b$ acompaña a $x$, y $c$ es el término independiente.")
            st.latex(rf"a = {a_val}, \quad b = {b_val}, \quad c = {c_val}")

            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso 4 — Discriminante**")
            explicacion(r"El discriminante $\Delta = b^2 - 4ac$ determina el tipo de soluciones: $\Delta > 0$ dos raíces reales, $\Delta = 0$ una raíz doble, $\Delta < 0$ raíces complejas.")
            st.latex(rf"\Delta = ({b_val})^2 - 4({a_val})({c_val}) = {disc}")

            if disc < 0:
                st.warning("El discriminante es negativo. La ecuacion no tiene soluciones reales.")
            else:
                st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                st.markdown("**Paso 5 — Formula general**")
                explicacion(r"Aplicamos $x = \frac{-b \pm \sqrt{\Delta}}{2a}$. El signo $\pm$ produce dos raíces: $x_1$ con suma y $x_2$ con resta.")
                st.latex(rf"x = \frac{{-({b_val}) \pm \sqrt{{{disc}}}}}{{2({a_val})}}")
                sqrt_disc = sp.sqrt(disc)
                st.latex(rf"x_1 = {soluciones_quad[0]}")
                if len(soluciones_quad) > 1:
                    st.latex(rf"x_2 = {soluciones_quad[1]}")
        else:
            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso 3 — Factorizacion**")
            explicacion(r"Reescribimos como $a(x - r_1)(x - r_2) = 0$. Las raíces $r_1$ y $r_2$ anulan cada factor respectivamente.")
            factores = sp.factor(ecuacion_final)
            st.latex(rf"{sp.latex(factores)} = 0")
            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso 4 — Despeje de raices**")
            explicacion(r"Por la Propiedad de la Multiplicación Nula: si $A \cdot B = 0$, entonces $A = 0$ o $B = 0$.")
            for i, sol in enumerate(soluciones_quad):
                st.latex(rf"x_{i+1} = {sol}")

        if is_log and disc >= 0:
            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
            st.markdown("**Paso final — Validacion de dominio**")
            explicacion(r"Los argumentos del logaritmo deben ser $> 0$. Descartamos toda raíz que produzca $\log(\text{número} \leq 0)$.")
            sol_finales = []
            for sol in soluciones_quad:
                try:
                    if arg1.subs(x, sol) > 0 and arg2.subs(x, sol) > 0:
                        sol_finales.append(sol)
                        st.success(rf"x = {sol} es valida.")
                    else:
                        st.error(rf"x = {sol} se descarta.")
                except: pass
            if len(sol_finales) == 0:
                sol_str = "∅"
            elif len(sol_finales) == 1:
                sol_str = f"{{ {sol_finales[0]} }}"
            else:
                sol_str = f"{{ {sol_finales[0]} , {sol_finales[1]} }}"
            st.markdown(f"""
            <div class='solucion-glow-card'>
                <div style='color:#94A3B8;font-size:13px;font-weight:600;letter-spacing:0.06em;margin-bottom:10px;'>CONJUNTO SOLUCIÓN</div>
                <div class='solucion-value'>S = {sol_str}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if len(soluciones_quad) == 0:
                sol_str = "∅"
            elif len(soluciones_quad) == 1:
                sol_str = f"{{ {soluciones_quad[0]} }}"
            else:
                sol_str = f"{{ {soluciones_quad[0]} , {soluciones_quad[1]} }}"
            st.markdown(f"""
            <div class='solucion-glow-card'>
                <div style='color:#94A3B8;font-size:13px;font-weight:600;letter-spacing:0.06em;margin-bottom:10px;'>CONJUNTO SOLUCIÓN</div>
                <div class='solucion-value'>S = {sol_str}</div>
            </div>
            """, unsafe_allow_html=True)

        try:
            st.markdown("### Representacion grafica")
            a_f = float(a_val if a_val != 0 else 1)
            b_f = float(b_val)
            v_x = -b_f / (2 * a_f)
            x_v = np.linspace(v_x - 6, v_x + 6, 200)
            y_v = float(a_val)*x_v**2 + float(b_val)*x_v + float(c_val)
            fig, ax = plt.subplots(figsize=(6, 3.8))
            fig.patch.set_facecolor('#0F172A')
            ax.set_facecolor('#07111F')
            ax.plot(x_v, y_v, color="#06B6D4", linewidth=2.5, label="f(x)")
            ax.axhline(0, color='#94a3b833', linewidth=1, linestyle='--')
            ax.axvline(0, color='#94a3b833', linewidth=1, linestyle='--')
            ax.spines['bottom'].set_color('#94a3b866')
            ax.spines['left'].set_color('#94a3b866')
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            ax.tick_params(colors='#94A3B8', labelsize=9)
            ax.grid(True, linestyle=':', color='#94a3b81a')
            ax.legend(facecolor='#07111F', edgecolor='#94a3b833', labelcolor='#E2E8F0')
            st.pyplot(fig)
        except Exception as e:
            st.caption(f"No se pudo generar la grafica: {e}")

# =========================================================================
# MODULO 2
# =========================================================================
with modulo[1]:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### Configuracion del sistema")
    metodo_sist = st.selectbox("Metodo de resolucion:", ["Sustitucion", "Igualacion", "Reduccion"])
    st.markdown("<p style='margin-top:10px;color:#06B6D4 !important;'>Ingresa cada ecuacion en forma libre — ejemplo: 2x + 3y = 20</p>", unsafe_allow_html=True)
    c_sys1, c_sys2 = st.columns(2)
    with c_sys1: ent_eq1 = st.text_input("Ecuacion 1:", value="2x + 3y = 20", key="sys_eq1")
    with c_sys2: ent_eq2 = st.text_input("Ecuacion 2:", value="x - 2y = 3", key="sys_eq2")

    if st.button("Resolver sistema lineal"):
        if "=" not in ent_eq1 or "=" not in ent_eq2:
            st.error("Ambas ecuaciones deben contener el signo '='.")
        else:
            try:
                t1 = ent_eq1.split("="); t2 = ent_eq2.split("=")
                x, y = sp.symbols('x y')
                local_dict_sys = {'x': x, 'y': y}
                izq1 = parse_expr(t1[0], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                der1 = parse_expr(t1[1], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                izq2 = parse_expr(t2[0], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                der2 = parse_expr(t2[1], local_dict=local_dict_sys, transformations=transformaciones_inteligentes)
                exp1, exp2 = izq1 - der1, izq2 - der2
                a1, b1, c1 = exp1.coeff(x), exp1.coeff(y), -exp1.subs({x:0, y:0})
                a2, b2, c2 = exp2.coeff(x), exp2.coeff(y), -exp2.subs({x:0, y:0})
                LIMITE = 10**6
                coeffs_check = [abs(float(v)) for v in [a1,b1,c1,a2,b2,c2] if v != 0]
                if coeffs_check and max(coeffs_check) > LIMITE:
                    st.error("Los coeficientes son demasiado grandes. Usa valores menores a 1,000,000.")
                else:
                    solucion = sp.solve((sp.Eq(izq1, der1), sp.Eq(izq2, der2)), (x, y))
                    if not solucion:
                        st.warning("Las rectas son paralelas o coincidentes.")
                    else:
                        val_x, val_y = solucion[x], solucion[y]
                        st.markdown("### Desarrollo paso a paso")

                        st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                        st.markdown("**Paso 1 — Forma canonica**")
                        explicacion(r"Reorganizamos en la forma $ax + by = c$ con variables a la izquierda y constantes a la derecha.")
                        st.latex(rf"\begin{{cases}} {a1}x + ({b1})y = {c1} \\ {a2}x + ({b2})y = {c2} \end{{cases}}")

                        if metodo_sist == "Sustitucion":
                            des_x = sp.solve(sp.Eq(izq1, der1), x)[0]
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 2 — Despeje**")
                            explicacion(r"Despejamos $x$ en la primera ecuación para expresarla en términos de $y$.")
                            st.latex(rf"x = {sp.latex(des_x)}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 3 — Sustitucion**")
                            explicacion(r"Reemplazamos $x$ en la segunda ecuación y resolvemos para $y$.")
                            expr_sust = izq2.subs(x, des_x)
                            st.latex(rf"{sp.latex(sp.simplify(expr_sust))} = {c2}")
                            st.latex(rf"y = {val_y}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 4 — Sustitucion inversa**")
                            explicacion(r"Sustituimos $y$ en la expresión de $x$ del paso 2.")
                            st.latex(rf"x = {sp.latex(des_x.subs(y, val_y))} \implies x = {val_x}")

                        elif metodo_sist == "Igualacion":
                            des_x1 = sp.solve(sp.Eq(izq1, der1), x)[0]
                            des_x2 = sp.solve(sp.Eq(izq2, der2), x)[0]
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 2 — Doble despeje**")
                            explicacion(r"Despejamos $x$ en cada ecuación, obteniendo dos expresiones de $x$ en términos de $y$.")
                            st.latex(rf"x = {sp.latex(des_x1)}")
                            st.latex(rf"x = {sp.latex(des_x2)}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 3 — Igualacion**")
                            explicacion(r"Igualamos las dos expresiones y resolvemos para $y$.")
                            st.latex(rf"{sp.latex(des_x1)} = {sp.latex(des_x2)}")
                            st.latex(rf"y = {val_y}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 4 — Calculo de x**")
                            explicacion(r"Sustituimos $y$ en cualquiera de las expresiones de $x$.")
                            st.latex(rf"x = {sp.latex(des_x1.subs(y, val_y))} \implies x = {val_x}")

                        else:
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 2 — Preparacion**")
                            explicacion(r"Multiplicamos para igualar los coeficientes de $x$ y poder cancelarlos al restar.")
                            st.latex(rf"\begin{{cases}} {a1*a2}x + ({b1*a2})y = {c1*a2} \\ {a2*a1}x + ({b2*a1})y = {c2*a1} \end{{cases}}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 3 — Eliminacion**")
                            explicacion(r"Restamos las ecuaciones. Los términos con $x$ se anulan y obtenemos $y$.")
                            st.latex(rf"({b1*a2 - b2*a1})y = {c1*a2 - c2*a1} \implies y = {val_y}")
                            st.markdown("<div class='step-anim'>", unsafe_allow_html=True)
                            st.markdown("**Paso 4 — Sustitucion**")
                            explicacion(r"Sustituimos $y$ en una ecuación original para encontrar $x$.")
                            st.latex(rf"{a1}x + ({b1})({val_y}) = {c1} \implies x = {val_x}")

                        st.markdown(f"""
                        <div class='solucion-glow-card'>
                            <div style='color:#94A3B8;font-size:13px;font-weight:600;letter-spacing:0.06em;margin-bottom:10px;'>PUNTO DE INTERSECCIÓN</div>
                            <div class='solucion-value'>P = ( {val_x} , {val_y} )</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("### Representacion grafica")
                        try:
                            x_num = float(val_x)
                            x_vals = np.linspace(x_num - 5, x_num + 5, 100)
                            fig, ax = plt.subplots(figsize=(6, 4))
                            fig.patch.set_facecolor('#0F172A'); ax.set_facecolor('#07111F')
                            if b1 != 0:
                                y_vals1 = [float((c1 - a1*kv) / b1) for kv in x_vals]
                                ax.plot(x_vals, y_vals1, color="#2563FF", linewidth=2.5, label="Ecuacion 1")
                            else:
                                ax.axvline(float(c1/a1), color="#2563FF", linewidth=2.5, label="Ecuacion 1")
                            if b2 != 0:
                                y_vals2 = [float((c2 - a2*kv) / b2) for kv in x_vals]
                                ax.plot(x_vals, y_vals2, color="#7C3AED", linewidth=2.5, label="Ecuacion 2")
                            else:
                                ax.axvline(float(c2/a2), color="#7C3AED", linewidth=2.5, label="Ecuacion 2")
                            ax.scatter(float(val_x), float(val_y), color="#06B6D4", s=140, zorder=5,
                                       label=f"P({val_x}, {val_y})", edgecolors='white')
                            ax.axhline(0, color='#94a3b833', linewidth=0.8, linestyle='--')
                            ax.axvline(0, color='#94a3b833', linewidth=0.8, linestyle='--')
                            ax.spines['bottom'].set_color('#94a3b866'); ax.spines['left'].set_color('#94a3b866')
                            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
                            ax.tick_params(colors='#94A3B8', labelsize=9)
                            ax.grid(True, linestyle=':', color='#94a3b81a')
                            ax.legend(facecolor='#07111F', edgecolor='#94a3b833', labelcolor='#E2E8F0')
                            st.pyplot(fig)
                        except Exception as e:
                            st.caption(f"No se pudo generar la grafica: {e}")

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
