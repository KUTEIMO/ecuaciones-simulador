# -*- coding: utf-8 -*-
"""
Casos de exposición alineados con las 14 diapositivas (Grupo 6 — ecuación auxiliar).

Notación canónica de las diapositivas (Leibniz):
  m (d²x/dt²) + (c + k_i K_d) (dx/dt) + (k_i K_p - k_s) x = 0
En el motor numérico, k_s magnético desestabilizante se modela como ks < 0 y
k_i K_p - k_s = -(ks + k_i K_p) = -k_eff_code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from physics_core import DigitalParams, PlantParams


@dataclass(frozen=True)
class ExpoCase:
    """Un escenario completo para la interfaz (diapositiva + planta + condiciones)."""

    slide_id: str
    title: str
    integrante: str
    bullets: tuple[str, ...]
    pp: PlantParams
    t_end: float
    x0: float
    v0: float
    clearance_m: float
    y0_scale: float
    use_digital: bool
    digital: DigitalParams
    imax: float | None
    slide_ref: str  # referencia corta "Diapositiva N"


def _dp_fast() -> DigitalParams:
    return DigitalParams(Ts=5e-5, tau=1e-5)


# --- Turbina X-100 (diapositivas 10–13) ---------------------------------------
# k_s = 20 N/m inestable → ks = -20; k_i = 1

CASO_A_TURBINE = ExpoCase(
    slide_id="caso_a",
    title="Turbina X-100 — Caso A: divergencia exponencial",
    integrante="Comparación de soluciones y ejercicio de aplicación",
    bullets=(
        r"$m=1\,\mathrm{kg}$, $k_s=20\,\mathrm{N/m}$ (inestable), $k_i=1$, $K_p=15$, $K_d=0$.",
        r"E.D.O.: $\frac{d^2x}{dt^2} - 5x = 0$ → $s=\pm\sqrt{5}$, raíz positiva → $e^{2.23t}\to\infty$.",
        "Interpretación: el eje colisiona con el estator — inestabilidad catastrófica.",
    ),
    pp=PlantParams(m=1.0, c=0.0, ks=-20.0, ki=1.0, Kp=15.0, Kd=0.0),
    t_end=1.8,
    x0=0.08 * 0.0005,  # 8 % de holgura: empieza dentro; luego diverge
    v0=0.0,
    clearance_m=0.0005,
    y0_scale=0.0,
    use_digital=False,
    digital=_dp_fast(),
    imax=None,
    slide_ref="Diapositivas 10–11",
)

CASO_B_TURBINE = ExpoCase(
    slide_id="caso_b",
    title="Turbina X-100 — Caso B: raíces complejas conjugadas (estable)",
    integrante="Comparación de soluciones y ejercicio de aplicación",
    bullets=(
        r"$K_p=30$, $c+k_i K_d=6$ → $\frac{d^2x}{dt^2}+6\frac{dx}{dt}+10x=0$.",
        r"$s=-3\pm i$ → $x(t)=e^{-3t}[C_1\cos t + C_2\sin t]$ (Caso III, $\alpha<0$).",
        "Órbita en el cojinete: espiral que colapsa al origen sin tocar la holgura.",
    ),
    pp=PlantParams(m=1.0, c=0.0, ks=-20.0, ki=1.0, Kp=30.0, Kd=6.0),
    t_end=4.0,
    x0=0.35 * 0.0005,
    v0=0.0,
    clearance_m=0.0005,
    y0_scale=0.0,
    use_digital=False,
    digital=_dp_fast(),
    imax=None,
    slide_ref="Diapositivas 12–13",
)

# --- Casos I, II, III (diapositivas 5–8) — plantas pedagógicas ----------------
# Caso I: ejemplo de exposición 1·x'' + 5·x' + 6·x = 0  →  s = -2, -3

CASO_I_SOBREAMORT = ExpoCase(
    slide_id="caso_i",
    title="Caso I — Raíces reales diferentes",
    integrante="Explicación de raíces reales diferentes",
    bullets=(
        r"$\Delta=(c+k_i K_d)^2-4m(k_i K_p-k_s)>0$ → $x(t)=C_1 e^{s_1 t}+C_2 e^{s_2 t}$, $s_1\neq s_2$.",
        "Respuesta monótona hacia el equilibrio, sin oscilación.",
        "Equivalente AMB: lazo muy amortiguado (ganancia derivativa alta).",
    ),
    pp=PlantParams(m=1.0, c=0.0, ks=-5.0, ki=1.0, Kp=11.0, Kd=5.0),
    t_end=7.0,
    x0=0.006,
    v0=0.0,
    clearance_m=0.02,
    y0_scale=0.0,
    use_digital=False,
    digital=_dp_fast(),
    imax=None,
    slide_ref="Diapositiva 5",
)

CASO_II_CRITICO = ExpoCase(
    slide_id="caso_ii",
    title="Caso II — Raíces reales iguales",
    integrante="Explicación de raíces reales iguales",
    bullets=(
        r"$\Delta=0$ → $s=-\frac{c+k_i K_d}{2m}$ (doble).",
        r"$x(t)=(C_1+C_2 t)\,e^{st}$ — retorno al equilibrio más rápido sin oscilar.",
        "Referencia de diseño: amortiguamiento crítico del modo transversal.",
    ),
    pp=PlantParams(m=1.0, c=0.0, ks=-1.0, ki=1.0, Kp=2.0, Kd=2.0),
    t_end=6.0,
    x0=0.004,
    v0=0.0,
    clearance_m=0.02,
    y0_scale=0.0,
    use_digital=False,
    digital=_dp_fast(),
    imax=None,
    slide_ref="Diapositiva 6",
)

CASO_III_SUB = ExpoCase(
    slide_id="caso_iii",
    title="Caso III — Raíces complejas conjugadas",
    integrante="Explicación de raíces complejas y ejercicios",
    bullets=(
        r"$s=\alpha\pm\beta i$ → $x(t)=e^{\alpha t}[C_1\cos(\beta t)+C_2\sin(\beta t)]$.",
        r"Si $\alpha<0$: vibración amortiguada; si $\alpha>0$: divergencia (plano derecho).",
        "Plano $s$: frontera industrial entre estabilidad y colisión.",
    ),
    pp=PlantParams(m=1.0, c=0.0, ks=-20.0, ki=1.0, Kp=30.0, Kd=6.0),
    t_end=5.0,
    x0=0.35 * 0.0005,
    v0=0.0,
    clearance_m=0.0005,
    y0_scale=0.0,
    use_digital=False,
    digital=_dp_fast(),
    imax=None,
    slide_ref="Diapositivas 7–8",
)

# --- AMB interactivo (diapositiva 9 + aplicación completa) --------------------

AMB_INTERACTIVO = ExpoCase(
    slide_id="amb_alpha",
    title="AMB — Control digital y comparación de soluciones",
    integrante="Comparación continuo vs digital",
    bullets=(
        r"Al variar $K_p$ mediante $\alpha$ se desplazan las raíces del polinomio característico.",
        r"El lazo digital debe mantener $\mathrm{Re}(s)<0$ pese a muestreo y retardo.",
        "Las gráficas comparan la respuesta continua frente a la implementación digital.",
    ),
    pp=PlantParams(m=20.0, c=8.0, ks=-1.0e5, ki=320.0, Kp=425.0, Kd=0.48),
    t_end=0.65,
    x0=110e-6,
    v0=0.0,
    clearance_m=320e-6,
    y0_scale=0.70,
    use_digital=True,
    digital=DigitalParams(Ts=7e-5, tau=1.5e-5),
    imax=32.0,
    slide_ref="Diapositiva 9 + aplicación AMB",
)


# Orden del selector (IDs internos estables; etiquetas en MENU_LABEL_BY_SLIDE_ID)
SLIDE_IDS_ORDER: tuple[str, ...] = (
    "caso_i",
    "caso_ii",
    "caso_iii",
    "caso_a",
    "caso_b",
    "amb_alpha",
)

EXPO_BY_SLIDE_ID: dict[str, ExpoCase] = {
    "caso_i": CASO_I_SOBREAMORT,
    "caso_ii": CASO_II_CRITICO,
    "caso_iii": CASO_III_SUB,
    "caso_a": CASO_A_TURBINE,
    "caso_b": CASO_B_TURBINE,
    "amb_alpha": AMB_INTERACTIVO,
}

MENU_LABEL_BY_SLIDE_ID: dict[str, str] = {
    "caso_i": "Caso I — Raíces reales diferentes",
    "caso_ii": "Caso II — Raíces reales iguales",
    "caso_iii": "Caso III — Raíces complejas conjugadas",
    "caso_a": "Turbina X-100 — Caso A (divergencia)",
    "caso_b": "Turbina X-100 — Caso B (estable)",
    "amb_alpha": "AMB — Control digital interactivo",
}

# Compatibilidad con código que usaba etiquetas largas como clave
EXPO_MENU: dict[str, ExpoCase] = {
    MENU_LABEL_BY_SLIDE_ID[sid]: EXPO_BY_SLIDE_ID[sid] for sid in SLIDE_IDS_ORDER
}

# --- Sincronización tipo de raíz (manual) ↔ bloque de exposición ----------------

FORMA_REALES = "Caso I — Raíces reales diferentes"
FORMA_DOBLE = "Caso II — Raíces reales iguales"
FORMA_COMPLEJAS = "Caso III — Raíces complejas conjugadas"

FORMA_OPTIONS: tuple[str, ...] = (FORMA_REALES, FORMA_DOBLE, FORMA_COMPLEJAS)

FORMA_COMPAT_SLIDES: dict[str, frozenset[str]] = {
    FORMA_REALES: frozenset({"caso_i", "caso_a"}),
    FORMA_DOBLE: frozenset({"caso_ii"}),
    FORMA_COMPLEJAS: frozenset({"caso_iii", "caso_b", "amb_alpha"}),
}


def menu_label(slide_id: str) -> str:
    return MENU_LABEL_BY_SLIDE_ID[slide_id]


def forma_for_slide_id(slide_id: str) -> str:
    """Tipo de raíz pedagógico asociado a cada bloque de diapositiva."""
    if slide_id in ("caso_i", "caso_a"):
        return FORMA_REALES
    if slide_id == "caso_ii":
        return FORMA_DOBLE
    return FORMA_COMPLEJAS


def default_slide_for_forma(forma: str) -> str:
    defaults = {
        FORMA_REALES: "caso_i",
        FORMA_DOBLE: "caso_ii",
        FORMA_COMPLEJAS: "caso_iii",
    }
    return defaults[forma]


def resolve_slide_for_root_forma(forma: str, current_slide_id: str) -> str:
    """
    Bloque de exposición coherente con el tipo de raíz elegido.
    Si el bloque actual ya es compatible, se mantiene (p. ej. Caso A con raíces reales).
    Si no, se elige el bloque canónico o el par turbina A↔B.
    """
    if current_slide_id in FORMA_COMPAT_SLIDES[forma]:
        return current_slide_id
    if current_slide_id == "caso_a" and forma == FORMA_COMPLEJAS:
        return "caso_b"
    if current_slide_id == "caso_b" and forma == FORMA_REALES:
        return "caso_a"
    return default_slide_for_forma(forma)


def forma_is_reales(forma: str) -> bool:
    return forma == FORMA_REALES


def forma_is_doble(forma: str) -> bool:
    return forma == FORMA_DOBLE


def forma_is_complejas(forma: str) -> bool:
    return forma == FORMA_COMPLEJAS


def case_a_step_lines() -> list[tuple[str, str]]:
    """(etiqueta, LaTeX) — sin \\text{} (KaTeX de Streamlit lo rompe)."""
    return [
        (
            "Sustitución",
            r"1\cdot\frac{d^2 x}{dt^2}+0\cdot\frac{dx}{dt}+(15-20)x=0",
        ),
        (
            "Forma reducida",
            r"\Rightarrow\quad \frac{d^2 x}{dt^2}-5x=0",
        ),
        (
            "Ecuación auxiliar",
            r"s^2-5=0\quad\Rightarrow\quad"
            r"s_{1}=+\sqrt{5}\approx+2.23,\quad s_{2}=-\sqrt{5}",
        ),
        (
            "Solución general",
            r"x(t)=C_{1}e^{2.23t}+C_{2}e^{-2.23t}",
        ),
    ]


def case_b_step_lines() -> list[tuple[str, str]]:
    return [
        ("E.D.O. numérica", r"\frac{d^2 x}{dt^2}+6\frac{dx}{dt}+10x=0"),
        (
            "Fórmula cuadrática",
            r"s=\frac{-6\pm\sqrt{36-40}}{2}"
            r"=\frac{-6\pm\sqrt{-4}}{2}=\frac{-6\pm 2i}{2}",
        ),
        ("Raíces", r"\Rightarrow\quad s=-3\pm i\quad(\mathrm{Re}(s)=-3<0)"),
        (
            "Solución general",
            r"x(t)=e^{-3t}\bigl[C_{1}\cos t + C_{2}\sin t\bigr]",
        ),
    ]


def slide_steps(case: ExpoCase) -> list[str | tuple[str, str]]:
    if case.slide_id == "caso_a":
        return case_a_step_lines()
    if case.slide_id == "caso_b":
        return case_b_step_lines()
    return list(case.bullets)
