# -*- coding: utf-8 -*-
"""LaTeX y coeficientes para el panel paso a paso."""

from __future__ import annotations

import cmath
from dataclasses import dataclass
from typing import Any

from physics_core import (
    PlantParams,
    auxiliary_polynomial_text,
    b_effective,
    ki_kp_minus_ks_slide,
    k_s_diapositiva,
)


@dataclass(frozen=True)
class AuxCoeffs:
    a: float
    b: float
    c: float


def aux_coeffs(pp: PlantParams) -> AuxCoeffs:
    return AuxCoeffs(a=pp.m, b=b_effective(pp), c=ki_kp_minus_ks_slide(pp))


def _fmt(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x))}"
    return f"{x:g}"


def _fmt_complex(z: complex) -> str:
    if abs(z.imag) < 1e-9:
        return _fmt(z.real)
    sign = "+" if z.imag >= 0 else "-"
    return rf"{z.real:g}{sign}{abs(z.imag):g}\,j"


def try_integer_factorization(ac: AuxCoeffs) -> dict[str, Any] | None:
    a, b, c = ac.a, ac.b, ac.c
    disc = b * b - 4 * a * c
    if disc < -1e-9:
        return None
    for val in (a, b, c):
        if abs(val - round(val)) > 1e-6:
            return None
    a, b, c = int(round(a)), int(round(b)), int(round(c))
    if a != 1 or a <= 0:
        return None
    target_prod, target_sum = c, b
    for p in range(-abs(target_prod) * 2, abs(target_prod) * 2 + 1):
        if p == 0 or target_prod % p != 0:
            continue
        q = target_prod // p
        if p + q == target_sum:
            return {
                "p": p,
                "q": q,
                "latex": rf"(s + {p})(s + {q}) = 0",
                "roots": (-float(p), -float(q)),
                "vieta": rf"p+q={target_sum},\; pq={target_prod}",
            }
    return None


def block_a_newton_latex() -> str:
    return (
        r"m\,\frac{d^2x}{dt^2} = "
        r"-c\,\frac{dx}{dt} - (k_i K_p - k_s)\,x"
    )


def block_b_ode_numeric_latex(pp: PlantParams) -> str:
    m, b, k = pp.m, b_effective(pp), ki_kp_minus_ks_slide(pp)
    d2 = r"\frac{d^2x}{dt^2}"
    d1 = r"\frac{dx}{dt}"
    parts = []
    if abs(m - 1.0) < 1e-12:
        parts.append(rf"\underbrace{{1}}_{{m}}\,{d2}")
    else:
        parts.append(rf"\underbrace{{{m:g}}}_{{m}}\,{d2}")
    if abs(b) > 1e-12:
        parts.append(rf"+ \underbrace{{{b:g}}}_{{c+k_i K_d}}\,{d1}")
    if abs(k) > 1e-12:
        ktex = f"{k:g}"
        parts.append(rf"+ \underbrace{{{ktex}}}_{{k_i K_p - k_s}}\,x")
    return " ".join(parts) + r" = 0"


def block_b_coeff_breakdown(pp: PlantParams) -> list[tuple[str, str]]:
    ks = k_s_diapositiva(pp)
    b = b_effective(pp)
    k = ki_kp_minus_ks_slide(pp)
    return [
        (r"$m$", rf"{pp.m:g} kg"),
        (r"$c + k_i K_d$", rf"{pp.c:g} + ({pp.ki:g})({pp.Kd:g}) = {b:g}"),
        (r"$k_i K_p - k_s$", rf"({pp.ki:g})({pp.Kp:g}) - {ks:g} = {k:g}"),
    ]


def block_c_derivatives_latex() -> list[str]:
    return [
        r"x(t) = e^{st}",
        r"x' = \frac{d}{dt}\bigl(e^{st}\bigr) = s\,e^{st}",
        r"x'' = \frac{d}{dt}\bigl(s\,e^{st}\bigr) = s^2\,e^{st}",
    ]


def block_d_substitution_lines(pp: PlantParams) -> list[str]:
    ac = aux_coeffs(pp)
    m, b, k = ac.a, ac.b, ac.c
    lead = _fmt(m)
    return [
        rf"{lead}(s^2 e^{{st}}) + {_fmt(b)}(s\,e^{{st}}) + {_fmt(k)}(e^{{st}}) = 0",
        rf"e^{{st}} \cdot \bigl({_fmt(m)} s^2 + {_fmt(b)} s + {_fmt(k)}\bigr) = 0",
        rf"e^{{st}} \neq 0 \;\Rightarrow\; {auxiliary_polynomial_text(pp)}",
    ]


def block_e_factorization(pp: PlantParams) -> dict[str, Any] | None:
    return try_integer_factorization(aux_coeffs(pp))


def block_e_quadratic_formula(pp: PlantParams) -> list[str]:
    ac = aux_coeffs(pp)
    a, b, c = ac.a, ac.b, ac.c
    disc = b * b - 4 * a * c
    sd = cmath.sqrt(disc)
    s1 = (-b + sd) / (2 * a)
    s2 = (-b - sd) / (2 * a)
    return [
        r"s = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        rf"s = \frac{{-{_fmt(b)} \pm \sqrt{{{_fmt(b)}^2 - 4({_fmt(a)})({_fmt(c)})}}}}{{2({_fmt(a)})}}",
        rf"s = \frac{{-{_fmt(b)} \pm \sqrt{{{_fmt(disc)}}}}}{{2({_fmt(a)})}}",
        rf"s_1 = {_fmt_complex(s1)}, \qquad s_2 = {_fmt_complex(s2)}",
    ]


def block_f_discriminant_steps(pp: PlantParams, delta: float) -> list[str]:
    b = b_effective(pp)
    ks = k_s_diapositiva(pp)
    k = ki_kp_minus_ks_slide(pp)
    damp_sub = rf"({pp.c:g} + {pp.ki:g}\cdot{pp.Kd:g})"
    k_sub = rf"({pp.ki:g}\cdot{pp.Kp:g} - {ks:g})"
    return [
        r"\Delta = (c + k_i K_d)^2 - 4m(k_i K_p - k_s)",
        rf"\Delta = {damp_sub}^2 - 4\cdot{_fmt(pp.m)}\cdot{k_sub}",
        rf"\Delta = {_fmt(b)}^2 - 4\cdot{_fmt(pp.m)}\cdot({_fmt(k)}) = {_fmt(delta)}",
    ]


def block_g_solution_latex(aux: dict[str, Any]) -> list[str]:
    cid = aux["case_id"]
    lines: list[str] = []
    if cid == "I":
        lines.append(r"x(t) = C_1 e^{s_1 t} + C_2 e^{s_2 t}")
    elif cid == "II":
        lines.append(r"x(t) = (C_1 + C_2 t)\,e^{s t}")
        lines.append(
            rf"s = -\frac{{c + k_i K_d}}{{2m}} \quad \text{{(raíz doble)}}"
        )
    else:
        lines.append(r"x(t) = e^{\alpha t}\bigl[C_1\cos(\beta t) + C_2\sin(\beta t)\bigr]")
        lines.append(rf"\alpha = {aux['alpha']:.4g},\quad \beta = {aux['beta']:.4g}\ \mathrm{{rad/s}}")
    return lines


def block_h_verification(pp: PlantParams, aux: dict[str, Any]) -> list[str]:
    ac = aux_coeffs(pp)
    s1 = aux["s1"]
    a, b, c = ac.a, ac.b, ac.c
    val = a * s1**2 + b * s1 + c
    return [
        rf"s_1 = {_fmt_complex(s1)}",
        (
            rf"{_fmt(a)}\,s_1^2 + {_fmt(b)}\,s_1 + {_fmt(c)} "
            rf"= {_fmt_complex(val)}"
        ),
    ]
