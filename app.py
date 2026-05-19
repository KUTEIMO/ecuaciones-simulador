# -*- coding: utf-8 -*-
"""
APLICACIÓN DE ESTABILIDAD DINÁMICA PARA COJINETES MAGNÉTICOS ACTIVOS (AMB)
EN TURBINAS DE ALTA VELOCIDAD

Grupo 6 — Soluciones según las raíces de la ecuación auxiliar.

Ejecutar: python -m streamlit run app.py
"""

from __future__ import annotations

import io
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from matplotlib.collections import LineCollection

from bearing_three_html import build_bearing_viewer_html, visual_gain_for_orbit
from expo_cases import (
    EXPO_BY_SLIDE_ID,
    EXPO_MENU,
    FORMA_OPTIONS,
    SLIDE_IDS_ORDER,
    ExpoCase,
    forma_for_slide_id,
    forma_is_doble,
    forma_is_reales,
    menu_label,
    resolve_slide_for_root_forma,
)
from math_steps_ui import render_paso_zoom_bar, render_step_by_step
from physics_core import (
    DigitalParams,
    PlantParams,
    analytic_response,
    auxiliary_polynomial_text,
    classify_auxiliary_case,
    kp_min,
    leibniz_ode_text,
    leibniz_discriminant_text,
    plant_from_characteristic_roots,
    roots_to_gains_summary,
    run_case,
)
from viz_export import fig_to_png_bytes

APP_TITLE_FULL = (
    "APLICACIÓN DE ESTABILIDAD DINÁMICA PARA COJINETES MAGNÉTICOS ACTIVOS (AMB) "
    "EN TURBINAS DE ALTA VELOCIDAD"
)

# Estilo diapositivas: fondo claro, azul marino
plt.rcParams.update(
    {
        "figure.facecolor": "#f8f6f0",
        "axes.facecolor": "#f8f6f0",
        "axes.edgecolor": "#1a365d",
        "axes.labelcolor": "#1a365d",
        "text.color": "#1a365d",
        "font.size": 10,
    }
)

NAVY = "#1a365d"
STEEL = "#4a6fa5"
GREEN = "#c8e6c9"
RED = "#ffcdd2"


def run_expo_case(case: ExpoCase, pp: PlantParams | None = None) -> dict:
    pp = pp or case.pp
    npts = min(18000, max(800, int(case.t_end / 4e-5)))
    return run_case(
        pp,
        case.digital,
        case.t_end,
        npts,
        case.x0,
        case.v0,
        case.clearance_m,
        imax=case.imax,
        y0_scale=case.y0_scale,
        use_digital=case.use_digital,
    )


def orbit_xy(res: dict, case: ExpoCase, pp: PlantParams) -> tuple[np.ndarray, np.ndarray]:
    """Trayectoria coherente con la solución analítica (texto) o digital (AMB)."""
    t = res["t"]
    aux = res["aux"]
    if not case.use_digital:
        xa = res["x_analytic"]
        if aux["case_id"] == "III" and aux["beta"] > 1e-9:
            ya = analytic_response(t, pp, 0.0, float(aux["beta"]) * case.x0)
        else:
            ya = np.zeros_like(xa)
        return xa, ya
    return res["x_dig"], res["y_dig"]


def expo_short_name(case: ExpoCase) -> str:
    return menu_label(case.slide_id)


def init_expo_slide_session() -> None:
    valid = set(SLIDE_IDS_ORDER)
    if st.session_state.get("expo_slide_id") in valid:
        return
    legacy = st.session_state.get("expo_modo")
    if isinstance(legacy, str) and legacy in EXPO_MENU:
        st.session_state.expo_slide_id = EXPO_MENU[legacy].slide_id
    else:
        st.session_state.expo_slide_id = "caso_i"
    st.session_state.pop("expo_modo", None)


def visual_state(res: dict, clearance_um: float) -> str:
    if res["unstable"]:
        return "danger"
    if res["contact"] or res["amp_dig_um"] > 0.85 * clearance_um:
        return "marginal"
    return "stable"


def fig_poles(pp: PlantParams, aux: dict) -> plt.Figure:
    s1, s2 = aux["s1"], aux["s2"]
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    lim = max(8.0, abs(s1.real), abs(s2.real), abs(s1.imag), abs(s2.imag)) * 1.22
    ax.axvspan(-lim, 0, alpha=0.35, color=GREEN, label="Semiplano estable Re$(s)<0$")
    ax.axvspan(0, lim, alpha=0.35, color=RED, label="Semiplano inestable Re$(s)>0$")
    ax.scatter([s1.real, s2.real], [s1.imag, s2.imag], s=200, c=[STEEL, NAVY], zorder=6, edgecolors="white", lw=1.5)
    ax.axhline(0, color=NAVY, lw=0.7)
    ax.axvline(0, color=NAVY, lw=0.7)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Re$(s)$ [1/s]")
    ax.set_ylabel(r"Im$(s)$ [1/s]")
    ax.set_title(f"Plano $s$ — Caso {aux['case_id']}: {aux['case_name']}")
    ax.grid(True, alpha=0.35)
    ax.legend(loc="upper right", fontsize=7)
    ax.text(
        0.03,
        0.97,
        leibniz_discriminant_text(pp, aux["delta"])
        + "\n"
        + auxiliary_polynomial_text(pp),
        transform=ax.transAxes,
        va="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    return fig


def fig_xt(res: dict, clearance_um: float, case_name: str, unstable: bool) -> plt.Figure:
    t = res["t"]
    xa = res["x_analytic"] * 1e6
    xc = res["x_cont"] * 1e6
    xd = res["x_dig"] * 1e6
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    tms = t * 1e3
    ax.plot(tms, xa, lw=2.4, color=NAVY, label="Solución analítica (ec. auxiliar)")
    ax.plot(tms, xc, lw=1.2, ls=":", color=STEEL, alpha=0.7, label="Integración numérica")
    if res["use_digital"]:
        ax.plot(tms, xd, lw=1.6, ls="--", color="#c45c26", label="Digital (AMB)")
    ax.axhline(clearance_um, color="#b71c1c", ls=":", lw=1.2)
    ax.axhline(-clearance_um, color="#b71c1c", ls=":", lw=1.2)
    ax.set_xlabel("$t$ [ms]")
    ax.set_ylabel("$x$ [µm]")
    ax.set_title(f"Trayectoria temporal — {case_name}")
    ax.grid(True, alpha=0.35)
    ax.legend(fontsize=8)
    if unstable:
        ax.set_ylim(bottom=min(-clearance_um * 0.5, float(np.min(xa[: min(500, len(xa))]) * 0.9)))
        ymax = min(clearance_um * 3.5, float(np.percentile(np.abs(xa), 99.5)) * 1.1)
        ax.set_ylim(top=max(ymax, clearance_um * 1.2))
    return fig


def fig_orbit(x_m: np.ndarray, y_m: np.ndarray, t: np.ndarray, clearance_um: float, title: str) -> plt.Figure:
    xd, yd = x_m * 1e6, y_m * 1e6
    pts = np.column_stack([xd, yd])
    seg = np.stack([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(seg, cmap="viridis", array=t[:-1], linewidths=2.2, alpha=0.95)
    fig, ax = plt.subplots(figsize=(4.9, 4.5))
    th = np.linspace(0, 2 * np.pi, 360)
    ax.plot(clearance_um * np.cos(th), clearance_um * np.sin(th), color="#b71c1c", lw=2.0, ls="--", label="Holgura AMB")
    ax.add_collection(lc)
    ax.scatter([0], [0], s=40, c=NAVY, zorder=5, label="Centro cojinete")
    rad = float(max(clearance_um * 1.2, np.max(np.hypot(xd, yd)) * 1.08, 30.0))
    ax.set_xlim(-rad, rad)
    ax.set_ylim(-rad, rad)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ [µm]")
    ax.set_ylabel("$y$ [µm]")
    ax.set_title(title)
    ax.grid(True, alpha=0.35)
    fig.colorbar(lc, ax=ax, fraction=0.046, pad=0.04, label="$t$ [s]")
    ax.legend(loc="upper left", fontsize=7)
    return fig


def fig_envelope(res: dict, aux: dict) -> plt.Figure | None:
    if aux["case_id"] != "III" or aux["beta"] < 1e-9:
        return None
    t = res["t"]
    xa = res["x_analytic"]
    alpha, beta = aux["alpha"], aux["beta"]
    env = np.exp(alpha * t) * np.max(np.abs([res["x_analytic"][0], 1e-12]))
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(t, xa * 1e6, color=NAVY, lw=1.8, label=r"$x(t)$")
    ax.plot(t, env * 1e6, "r--", lw=1.2, label=r"envolvente $e^{\alpha t}$")
    ax.plot(t, -env * 1e6, "r--", lw=1.2)
    ax.set_xlabel("$t$ [s]")
    ax.set_ylabel("$x$ [µm]")
    ax.set_title(r"Caso III: $x(t)=e^{\alpha t}[C_1\cos(\beta t)+C_2\sin(\beta t)]$")
    ax.grid(True, alpha=0.35)
    ax.legend(fontsize=8)
    ax.text(0.02, 0.95, rf"$\alpha={alpha:.3f}$, $\beta={beta:.3f}$ rad/s", transform=ax.transAxes, va="top", fontsize=9)
    return fig


def build_plant_amb(alpha: float) -> PlantParams:
    ks, ki = -1.0e5, 320.0
    kpm = kp_min(ks, ki)
    Kp = float(kpm * (1.0 + alpha))
    return PlantParams(m=20.0, c=8.0, ks=ks, ki=ki, Kp=Kp, Kd=0.48)


def sidebar_roots_sync_before_menu() -> bool:
    """
    Checkbox + tipo de raíz + alineación del menú.
    Debe ejecutarse ANTES del selectbox ``expo_slide_id``.
    Solo cambia el bloque si el usuario modifica el *tipo de raíz*, no el menú.
    """
    with st.sidebar.expander("Raíces / polos en tiempo real", expanded=False):
        manual = st.checkbox(
            "Editar raíces manualmente",
            value=False,
            key="root_manual_active",
            help="Mover polos en el plano s y ver K_p, K_d y la respuesta al instante.",
        )
        if not manual:
            st.session_state.pop("_sync_last_slide", None)
            st.session_state.pop("_last_root_forma_pick", None)
            return False

        st.caption(
            r"E.D.O.: $m\frac{d^2x}{dt^2}+(c+k_i K_d)\frac{dx}{dt}+(k_i K_p-k_s)x=0$"
        )
        slide_id = st.session_state.expo_slide_id
        menu_changed = st.session_state.get("_sync_last_slide") != slide_id

        if st.session_state.get("root_forma_pick") not in FORMA_OPTIONS:
            st.session_state.root_forma_pick = forma_for_slide_id(slide_id)

        if menu_changed:
            st.session_state.root_forma_pick = forma_for_slide_id(slide_id)
            st.session_state._sync_last_slide = slide_id
            st.session_state._last_root_forma_pick = st.session_state.root_forma_pick

        prev_forma = st.session_state.get("_last_root_forma_pick")

        st.radio(
            "Tipo de raíz",
            list(FORMA_OPTIONS),
            key="root_forma_pick",
            help="Al cambiar el tipo, el bloque de exposición se alinea automáticamente.",
        )
        forma = st.session_state.root_forma_pick

        if menu_changed:
            st.session_state._last_root_forma_pick = forma
        elif forma != prev_forma:
            st.session_state._last_root_forma_pick = forma
            desired_slide = resolve_slide_for_root_forma(forma, slide_id)
            if desired_slide != slide_id:
                st.session_state.expo_slide_id = desired_slide
                st.session_state._sync_last_slide = desired_slide
                st.rerun()
        else:
            st.session_state._last_root_forma_pick = forma
    return True


def sidebar_root_sliders(base_pp: PlantParams, slide_id: str) -> PlantParams:
    """Deslizadores de s₁, s₂ (después del menú de exposición)."""
    aux0 = classify_auxiliary_case(base_pp)
    s1_0, s2_0 = aux0["s1"], aux0["s2"]
    span = max(5.0, abs(s1_0.real) * 2.2 + 1.5, abs(s1_0.imag) * 2.2 + 1.5)
    forma = st.session_state.get("root_forma_pick", forma_for_slide_id(slide_id))

    with st.sidebar.expander("Valores de las raíces", expanded=True):
        if forma_is_reales(forma):
            s1r = st.slider(
                r"$s_1$ (real)",
                -span,
                span,
                float(s1_0.real),
                0.05,
                key=f"root_s1_re_{slide_id}",
            )
            s2r = st.slider(
                r"$s_2$ (real)",
                -span,
                span,
                float(s2_0.real),
                0.05,
                key=f"root_s2_re_{slide_id}",
            )
            s1, s2 = complex(s1r, 0.0), complex(s2r, 0.0)
        elif forma_is_doble(forma):
            sd = st.slider(
                r"$s$ (raíz doble)",
                -span,
                span,
                float(s1_0.real),
                0.05,
                key=f"root_s_double_{slide_id}",
            )
            s1 = s2 = complex(sd, 0.0)
        else:
            alpha = st.slider(
                r"$\alpha = \mathrm{Re}(s)$",
                -span,
                span,
                float(s1_0.real),
                0.05,
                key=f"root_alpha_{slide_id}",
            )
            beta = st.slider(
                r"$\beta$ [rad/s]",
                0.0,
                span,
                float(abs(s1_0.imag)),
                0.05,
                key=f"root_beta_{slide_id}",
            )
            s1, s2 = complex(alpha, beta), complex(alpha, -beta)

        pp_new = plant_from_characteristic_roots(base_pp, s1, s2)
        gains = roots_to_gains_summary(base_pp, s1, s2)
        st.markdown("**Ganancias equivalentes**")
        g1, g2 = st.columns(2)
        g1.metric(r"$K_p$", f"{gains['Kp']:.4g}")
        g2.metric(r"$K_d$", f"{gains['Kd']:.4g}")
        chk = classify_auxiliary_case(pp_new)
        st.caption(
            rf"$s_1 = {chk['s1'].real:.3f}{chk['s1'].imag:+.3f}j$, "
            rf"$\Delta = {chk['delta']:.4g}$, Caso {chk['case_id']}"
        )
        if chk["stable"]:
            st.success("Semiplano izquierdo — estable")
        else:
            st.warning("Semiplano derecho — inestable")
    return pp_new


def render_simulator() -> None:
    c0, c1, c2 = st.columns([0.4, 5.2, 0.4])
    with c1:
        st.markdown(
            f'<p style="text-align:center;font-size:1.02rem;font-weight:700;line-height:1.35;color:#1a365d;">{APP_TITLE_FULL}</p>',
            unsafe_allow_html=True,
        )
    st.caption(
        "**Grupo 6** — Casos I, II y III · Turbina X-100 (A y B) · AMB interactivo."
    )

    init_expo_slide_session()

    with st.sidebar:
        st.markdown(f"**{APP_TITLE_FULL}**")
        st.markdown("---")
        root_manual = sidebar_roots_sync_before_menu()
        st.selectbox(
            "Bloque de exposición",
            list(SLIDE_IDS_ORDER),
            format_func=menu_label,
            key="expo_slide_id",
            help="Casos I–III, turbina X-100 (A y B) y simulación AMB.",
        )
        case = EXPO_BY_SLIDE_ID[st.session_state.expo_slide_id]

    pp = sidebar_root_sliders(case.pp, case.slide_id) if root_manual else case.pp
    alpha_amb = 0.36
    esc_digital = "Rápido (casi continuo)"
    if case.slide_id == "amb_alpha":
        if not root_manual:
            alpha_amb = st.sidebar.slider(
                r"$\alpha$ — $K_p = K_{p,\min}(1+\alpha)$",
                0.12,
                0.62,
                0.36,
                0.01,
            )
            pp = build_plant_amb(alpha_amb)
        else:
            st.sidebar.caption("Modo raíces manual: el deslizador α queda desactivado.")
        esc_digital = st.sidebar.radio(
            "Lazo digital",
            ["Rápido (casi continuo)", "Lento + retardo (digital visible)"],
        )
        dp_map = {
            "Rápido (casi continuo)": DigitalParams(Ts=7e-5, tau=1.5e-5),
            "Lento + retardo (digital visible)": DigitalParams(Ts=5e-4, tau=3.8e-4),
        }
        case = ExpoCase(
            slide_id=case.slide_id,
            title=case.title,
            integrante=case.integrante,
            bullets=case.bullets,
            pp=pp,
            t_end=case.t_end,
            x0=case.x0,
            v0=case.v0,
            clearance_m=case.clearance_m,
            y0_scale=case.y0_scale,
            use_digital=True,
            digital=dp_map[esc_digital],
            imax=32.0,
            slide_ref=case.slide_ref,
        )

    res = run_expo_case(case, pp)
    aux = res["aux"]
    clearance_um = case.clearance_m * 1e6
    stt = visual_state(res, clearance_um)

    st.subheader(case.title)
    for b in case.bullets[:3]:
        st.markdown(f"- {b}")

    expo_slides = ("caso_i", "caso_ii", "caso_iii", "caso_a", "caso_b")
    with st.expander("Paso a paso (matemática)", expanded=case.slide_id in expo_slides):
        render_paso_zoom_bar()
        render_step_by_step(case, pp, aux)

    x_orb, y_orb = orbit_xy(res, case, pp)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tipo de raíz", aux["case_name"])
    s1 = aux["s1"]
    if abs(s1.imag) > 1e-6:
        m2.metric(r"$s_1$", f"{s1.real:.3f}{s1.imag:+.3f}j")
    else:
        m2.metric(r"Re$(s_1)$", f"{s1.real:.3f}")
    m3.metric(r"$\Delta$", f"{aux['delta']:.4g}")
    rad_um = float(np.max(np.hypot(x_orb, y_orb)) * 1e6)
    m4.metric("Pico |r| (µm)", f"{rad_um:.1f}")
    if res["unstable"]:
        st.error(r"Inestable: $\mathrm{Re}(s)>0$")
    elif res["alert"]:
        st.warning("|r| ≥ holgura")
    else:
        st.success(r"Estable: $\mathrm{Re}(s)<0$")

    vgain = visual_gain_for_orbit(x_orb, y_orb, case.clearance_m, not res["unstable"])
    t_frac_key = f"viewer_t_frac_{case.slide_id}"
    if t_frac_key not in st.session_state:
        st.session_state[t_frac_key] = 0.28

    col3d, colinfo = st.columns([1.65, 1.0])
    with col3d:
        st.markdown("#### Cojinete magnético — vista 3D")
        cap3d = rf"Holgura: anillo rojo. $t \in [0,\,{case.t_end:.2f}]$ s."
        if vgain > 1.02:
            cap3d += f" Escala visual 3D: ×{vgain:.2f}."
        st.caption(cap3d)
        st.slider(
            "t / T_max",
            0.0,
            1.0,
            float(st.session_state[t_frac_key]),
            0.01,
            key=t_frac_key,
            format="%.2f",
        )

    html = build_bearing_viewer_html(
        x_orb,
        y_orb,
        res["t"],
        case.clearance_m,
        stt,
        95.0,
        start_pct=float(st.session_state[t_frac_key]) * 100.0,
        frame_height=620,
        case_label=case.title[:80],
        case_id=aux["case_id"],
        expo_tag=expo_short_name(case),
        alpha_re=float(aux["s1"].real),
        beta_im=float(abs(aux["s1"].imag)),
        clearance_um=clearance_um,
        unstable=bool(res["unstable"]),
        visual_gain=vgain,
    )

    with col3d:
        components.html(html, height=620, scrolling=False)
    with colinfo:
        st.markdown("#### Estado")
        rad_um = float(np.max(np.hypot(x_orb, y_orb)) * 1e6)
        pct_h = 100.0 * rad_um / max(clearance_um, 1.0)
        st.metric("|r|_max / holgura", f"{pct_h:.0f}%")
        st.metric("α", f"{aux['alpha']:.4g}")
        if aux["case_id"] == "III" and aux["beta"] > 1e-9:
            st.metric("β (rad/s)", f"{aux['beta']:.4g}")
        if root_manual:
            st.caption(
                rf"Planta activa: $K_p={pp.Kp:.4g}$, $K_d={pp.Kd:.4g}$ "
                rf"(recalculados desde los polos elegidos)."
            )

    st.markdown("### Figuras del mismo caso")
    r1, r2 = st.columns(2)
    with r1:
        fp = fig_poles(pp, aux)
        st.pyplot(fp, use_container_width=True)
        plt.close(fp)
    with r2:
        fx = fig_xt(res, clearance_um, aux["case_name"], res["unstable"])
        st.pyplot(fx, use_container_width=True)
        plt.close(fx)

    fe = fig_envelope(res, aux)
    r3, r4 = st.columns(2)
    with r3:
        fo = fig_orbit(
            x_orb,
            y_orb,
            res["t"],
            clearance_um,
            "Órbita del eje en el cojinete magnético",
        )
        st.pyplot(fo, use_container_width=True)
        plt.close(fo)
    with r4:
        if fe is not None:
            st.pyplot(fe, use_container_width=True)
            plt.close(fe)
        else:
            st.markdown("Caso I o II: revise la curva temporal (sin envolvente oscilatoria).")

    if st.sidebar.checkbox("Descargar PNG", value=False):
        zf = io.BytesIO()
        with zipfile.ZipFile(zf, "w", zipfile.ZIP_DEFLATED) as z:
            fp2 = fig_poles(pp, aux)
            z.writestr("plano_s.png", fig_to_png_bytes(fp2))
            plt.close(fp2)
            fx2 = fig_xt(res, clearance_um, aux["case_name"], res["unstable"])
            z.writestr("xt.png", fig_to_png_bytes(fx2))
            plt.close(fx2)
            fo2 = fig_orbit(x_orb, y_orb, res["t"], clearance_um, "orbita")
            z.writestr("orbita.png", fig_to_png_bytes(fo2))
            plt.close(fo2)
        zf.seek(0)
        st.sidebar.download_button("ZIP capturas", zf.getvalue(), "expo_amb.zip")

    st.sidebar.caption("`python -m streamlit run app.py`")


st.set_page_config(
    page_title="Estabilidad dinámica — AMB",
    layout="wide",
    page_icon="⚙️",
)

_nav = st.navigation(
    [
        st.Page(render_simulator, title="Simulador", default=True, url_path=""),
        st.Page("ui_guion.py", title="Guion", url_path="guion"),
    ],
    position="hidden",
)
_nav.run()
