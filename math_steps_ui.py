# -*- coding: utf-8 -*-
"""Panel matemático paso a paso (Streamlit)."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from expo_cases import ExpoCase, slide_steps
from math_step_texts import (
    aux_coeffs,
    block_a_newton_latex,
    block_b_coeff_breakdown,
    block_b_ode_numeric_latex,
    block_c_derivatives_latex,
    block_d_substitution_lines,
    block_e_factorization,
    block_e_quadratic_formula,
    block_f_discriminant_steps,
    block_g_solution_latex,
    block_h_verification,
)
from physics_core import PlantParams, leibniz_ode_general_text, leibniz_ode_text

PASO_ZOOM_MIN = 100
PASO_ZOOM_MAX = 165
PASO_ZOOM_STEP = 5
_PASO_ZOOM_BAR_H = 40


def render_paso_zoom_bar() -> None:
    """Barra HTML minimalista; el zoom se aplica en el cliente (sin slider Streamlit)."""
    st.markdown(
        """
        <style>
        iframe.paso-zoom-iframe {
            border: none !important;
            display: block;
            width: 100%;
            min-height: 40px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(
        f"""
<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<style>
* {{ box-sizing: border-box; margin: 0; }}
html, body {{
  background: transparent;
  font-family: system-ui, -apple-system, sans-serif;
}}
.bar {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 2px 4px;
  width: 100%;
}}
.lbl {{
  font-size: 12px;
  font-weight: 600;
  color: #1a365d;
  flex: 0 0 auto;
}}
.track {{
  flex: 1 1 auto;
  min-width: 80px;
}}
input[type="range"] {{
  width: 100%;
  height: 6px;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
  background: #d4dce8;
}}
input[type="range"]::-webkit-slider-thumb {{
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #1a365d;
  border: 2px solid #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,.2);
  margin-top: -4px;
}}
input[type="range"]::-moz-range-thumb {{
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #1a365d;
  border: 2px solid #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,.2);
}}
input[type="range"]::-moz-range-track {{
  height: 6px;
  border-radius: 3px;
  background: #d4dce8;
}}
.pct {{
  font-size: 12px;
  font-weight: 600;
  color: #1a365d;
  min-width: 36px;
  text-align: right;
  flex: 0 0 auto;
  font-variant-numeric: tabular-nums;
}}
</style></head>
<body>
<div class="bar">
  <span class="lbl">Escala</span>
  <div class="track"><input type="range" id="z" min="{PASO_ZOOM_MIN}" max="{PASO_ZOOM_MAX}" step="{PASO_ZOOM_STEP}" value="100"></div>
  <span class="pct" id="v">100%</span>
</div>
<script>
(function () {{
  const MIN = {PASO_ZOOM_MIN}, MAX = {PASO_ZOOM_MAX}, STEP = {PASO_ZOOM_STEP};
  const KEY = "paso_paso_zoom_pct";
  const doc = window.parent.document;
  const z = document.getElementById("z");
  const v = document.getElementById("v");

  function trackFill(pct) {{
    const t = ((pct - MIN) / (MAX - MIN)) * 100;
    z.style.background = "linear-gradient(90deg,#1a365d 0%,#1a365d " + t + "%,#d4dce8 " + t + "%,#d4dce8 100%)";
  }}

  function zoomRoot() {{
    const start = doc.getElementById("paso-paso-scale-anchor");
    const end = doc.getElementById("paso-paso-scale-end");
    if (!start || !end) return null;

    let outer = start.parentElement;
    while (outer && !outer.contains(end)) outer = outer.parentElement;
    if (!outer) return null;

    let best = outer;
    let cur = start.parentElement;
    while (cur && cur !== outer) {{
      if (cur.contains(end)) best = cur;
      cur = cur.parentElement;
    }}
    return best;
  }}

  function clearZoom() {{
    doc.querySelectorAll("[data-paso-zoom-active]").forEach(function (el) {{
      el.style.zoom = "";
      el.style.transform = "";
      el.style.width = "";
      el.removeAttribute("data-paso-zoom-active");
    }});
  }}

  function setScale(el, scale) {{
    if (!el) return;
    if (scale <= 1.001) {{
      el.style.zoom = "";
      el.style.transform = "";
      el.style.width = "";
      el.removeAttribute("data-paso-zoom-active");
      return;
    }}
    el.setAttribute("data-paso-zoom-active", "1");
    el.style.zoom = String(scale);
    el.style.transform = "";
    el.style.width = "";
  }}

  function apply(pct) {{
    pct = Math.round(Math.max(MIN, Math.min(MAX, pct)) / STEP) * STEP;
    const scale = pct / 100;
    z.value = pct;
    v.textContent = pct + "%";
    trackFill(pct);
    try {{ localStorage.setItem(KEY, String(pct)); }} catch (e) {{}}

    const root = zoomRoot();
    if (!root) return false;
    clearZoom();
    setScale(root, scale);
    const exp = root.closest('[data-testid="stExpanderDetails"]');
    if (exp) exp.style.overflowX = "auto";
    return true;
  }}

  let start = MIN;
  try {{
    const saved = parseInt(localStorage.getItem(KEY), 10);
    if (!isNaN(saved)) start = saved;
  }} catch (e) {{}}

  z.addEventListener("input", function () {{
    apply(parseInt(z.value, 10));
  }});

  function boot() {{
    if (apply(start)) return;
    let n = 0;
    const id = setInterval(function () {{
      if (apply(start) || ++n > 50) clearInterval(id);
    }}, 80);
  }}
  boot();

  const exp = doc.querySelector('[data-testid="stExpanderDetails"]');
  if (exp) {{
    new MutationObserver(function () {{
      const root = zoomRoot();
      if (root) apply(parseInt(z.value, 10));
    }}).observe(exp, {{ childList: true, subtree: true }});
  }}
}})();
</script>
</body></html>
        """,
        height=_PASO_ZOOM_BAR_H,
    )


def _paso_zoom_anchor() -> None:
    st.markdown(
        '<div id="paso-paso-scale-anchor" aria-hidden="true" '
        'style="display:none;height:0;margin:0;padding:0;overflow:hidden"></div>',
        unsafe_allow_html=True,
    )


def _paso_zoom_end() -> None:
    st.markdown(
        '<div id="paso-paso-scale-end" aria-hidden="true" '
        'style="display:none;height:0;margin:0;padding:0;overflow:hidden"></div>',
        unsafe_allow_html=True,
    )


def _latex(text: str) -> None:
    s = text.strip()
    if s.startswith("$") and s.endswith("$"):
        s = s[1:-1].strip()
    st.latex(s)


def _var_table(rows: list[tuple[str, str]]) -> None:
    st.markdown("| Símbolo | Definición |")
    st.markdown("|---------|------------|")
    for sym, meaning in rows:
        st.markdown(f"| {sym} | {meaning} |")


def _render_block_a() -> None:
    st.markdown("#### A. Segunda ley (linealizada)")
    _latex(block_a_newton_latex())
    _var_table(
        [
            (r"$x(t)$", "Desplazamiento transversal (m)"),
            (r"$m$", "Masa modal (kg)"),
            (r"$c$", "Amortiguamiento mecánico (N·s/m)"),
            (r"$k_i$", "Ganancia del sensor"),
            (r"$K_p$, $K_d$", "Ganancias del controlador"),
            (r"$k_s$", "Rigidez magnética pasiva (N/m)"),
        ]
    )


def _render_block_b(pp: PlantParams) -> None:
    st.markdown("#### B. E.D.O. homogénea")
    st.caption("Forma general")
    _latex(leibniz_ode_general_text())
    st.caption("Caso activo")
    _latex(leibniz_ode_text(pp))
    _latex(block_b_ode_numeric_latex(pp))
    st.caption("Coeficientes")
    for sym, meaning in block_b_coeff_breakdown(pp):
        st.markdown(f"- {sym}: {meaning}")


def _render_block_c() -> None:
    st.markdown("#### C. Ansatz $x = e^{st}$")
    for line in block_c_derivatives_latex():
        _latex(line)
    _var_table(
        [
            (r"$s$", "Parámetro complejo del polinomio característico"),
            (r"$t$", "Tiempo (s)"),
            (r"$e^{st}$", "$\neq 0$ para $t \in \mathbb{R}$"),
        ]
    )


def _render_block_d(pp: PlantParams) -> None:
    st.markdown("#### D. Sustitución → ecuación auxiliar")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("E.D.O.")
        _latex(leibniz_ode_text(pp))
    with c2:
        st.caption("$x,\,x',\,x''$")
        _latex(r"x=e^{st},\; x'=s e^{st},\; x''=s^2 e^{st}")
    for line in block_d_substitution_lines(pp):
        _latex(line)


def _render_block_e(pp: PlantParams, aux: dict) -> None:
    st.markdown("#### E. Polinomio característico")
    ac = aux_coeffs(pp)
    _latex(
        r"m s^2 + (c + k_i K_d)\,s + (k_i K_p - k_s) = 0"
        rf"\quad\Leftrightarrow\quad {_fmt(ac.a)} s^2 + {_fmt(ac.b)} s + {_fmt(ac.c)} = 0"
    )
    fact = block_e_factorization(pp)
    if fact is not None:
        st.caption("Factorización")
        _latex(fact["vieta"])
        _latex(fact["latex"])
        r1, r2 = fact["roots"]
        _latex(rf"s_1 = {r1:g},\quad s_2 = {r2:g}")

    st.caption("Fórmula general")
    for line in block_e_quadratic_formula(pp):
        _latex(line)

    if fact is not None:
        s1 = aux["s1"]
        fr1, fr2 = fact["roots"]
        if min(abs(s1 - fr1), abs(s1 - fr2)) < 1e-4:
            st.caption("Factorización y fórmula general: mismas raíces.")


def _fmt(x: float) -> str:
    return f"{x:g}"


def _render_block_f(pp: PlantParams, aux: dict) -> None:
    st.markdown("#### F. Discriminante")
    for line in block_f_discriminant_steps(pp, aux["delta"]):
        _latex(line)
    st.markdown(
        "| $\\Delta$ | Caso |\n"
        "|----------|------|\n"
        "| $> 0$ | I — raíces reales distintas |\n"
        "| $= 0$ | II — raíz real doble |\n"
        "| $< 0$ | III — raíces complejas conjugadas |"
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Δ", f"{aux['delta']:.6g}")
    c2.metric("Caso", aux["case_id"])
    c3.metric("Re(s₁)", f"{aux['s1'].real:.4g}")


def _render_block_g(aux: dict) -> None:
    st.markdown("#### G. Solución general $x(t)$")
    for line in block_g_solution_latex(aux):
        _latex(line)
    s1, s2 = aux["s1"], aux["s2"]
    _latex(
        rf"s_1 = {s1.real:.6g}{s1.imag:+.6g}\,j,\qquad "
        rf"s_2 = {s2.real:.6g}{s2.imag:+.6g}\,j"
    )


def _render_block_h(pp: PlantParams, aux: dict) -> None:
    st.markdown("#### H. Residuo en la auxiliar ($s_1$)")
    for line in block_h_verification(pp, aux):
        _latex(line)


def _render_block_i(case: ExpoCase, aux: dict) -> None:
    st.markdown("#### I. Salidas del simulador")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Plano $s$", f"{aux['s1'].real:.3g}{aux['s1'].imag:+.3g}j")
    c2.metric("Caso", aux["case_id"])
    c3.metric("Δ", f"{aux['delta']:.4g}")
    c4.metric("Estable", "sí" if aux["stable"] else "no")
    st.caption(
        f"Gráfica $x(t)$, visor 3D (holgura {case.clearance_m * 1e6:.0f} µm), "
        f"intervalo $t \\in [0,\\,{case.t_end:.2f}]$ s."
    )
    _render_turbine_extra(case)


def _render_turbine_extra(case: ExpoCase) -> None:
    steps = slide_steps(case)
    if not steps or case.slide_id not in ("caso_a", "caso_b"):
        return
    st.markdown("#### Turbina X-100")
    for item in steps:
        if isinstance(item, tuple):
            label, latex = item
            st.caption(label)
            _latex(latex)
        else:
            _latex(item)


def render_step_by_step(case: ExpoCase, pp: PlantParams, aux: dict) -> None:
    _paso_zoom_anchor()
    tabs = st.tabs(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
    with tabs[0]:
        _render_block_a()
    with tabs[1]:
        _render_block_b(pp)
    with tabs[2]:
        _render_block_c()
    with tabs[3]:
        _render_block_d(pp)
    with tabs[4]:
        _render_block_e(pp, aux)
    with tabs[5]:
        _render_block_f(pp, aux)
    with tabs[6]:
        _render_block_g(aux)
    with tabs[7]:
        _render_block_h(pp, aux)
    with tabs[8]:
        _render_block_i(case, aux)
    _paso_zoom_end()
