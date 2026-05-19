# -*- coding: utf-8 -*-
"""
Motor físico-matemático — AMB + rotor Jeffcott (linealizado).
Notación Leibniz en docstrings del módulo app.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Any

import cmath
import numpy as np
from scipy.integrate import odeint


@dataclass(frozen=True)
class PlantParams:
    m: float
    c: float
    ks: float
    ki: float
    Kp: float
    Kd: float


@dataclass(frozen=True)
class DigitalParams:
    Ts: float
    tau: float


def kp_min(ks: float, ki: float) -> float:
    if ki <= 0:
        return float("nan")
    return float(-ks / ki)


def characteristic_roots(pp: PlantParams) -> tuple[complex, complex]:
    a = pp.m
    b = b_effective(pp)
    k_eff = k_effective(pp)
    disc = b * b - 4.0 * a * k_eff
    sd = cmath.sqrt(disc)
    d2 = 2.0 * a
    return (-b + sd) / d2, (-b - sd) / d2


def plant_from_characteristic_roots(
    template: PlantParams,
    s1: complex,
    s2: complex | None = None,
) -> PlantParams:
    """
    Fija m, c, k_s, k_i y ajusta K_p, K_d para que
    m s² + (c + k_i K_d) s + (k_s + k_i K_p) = 0 tenga raíces s1, s2.

    Coeficientes: b = -m(s1+s2), k_eff = m·s1·s2  (identidad de Vieta).
    """
    if s2 is None:
        s2 = s1
    m = template.m
    if m <= 0 or template.ki <= 0:
        raise ValueError("m y k_i deben ser positivos para asignar raíces.")
    z1, z2 = complex(s1), complex(s2)
    sum_s = z1 + z2
    prod_s = z1 * z2
    if abs(sum_s.imag) < 1e-8:
        sum_s = complex(sum_s.real, 0.0)
    if abs(prod_s.imag) < 1e-8:
        prod_s = complex(prod_s.real, 0.0)
    b = -m * sum_s.real
    k_eff = m * prod_s.real
    Kd = (b - template.c) / template.ki
    Kp = (k_eff - template.ks) / template.ki
    return PlantParams(
        m=template.m,
        c=template.c,
        ks=template.ks,
        ki=template.ki,
        Kp=float(Kp),
        Kd=float(Kd),
    )


def roots_to_gains_summary(template: PlantParams, s1: complex, s2: complex) -> dict[str, float]:
    pp = plant_from_characteristic_roots(template, s1, s2)
    return {
        "Kp": pp.Kp,
        "Kd": pp.Kd,
        "b_eff": b_effective(pp),
        "k_eff": k_effective(pp),
    }


def discriminant_auxiliary(pp: PlantParams) -> float:
    """Δ = (c + k_i K_d)² − 4 m (k_s + k_i K_p) — mismo polinomio que las diapositivas con k_s<0."""
    a = pp.m
    b = b_effective(pp)
    k_eff = k_effective(pp)
    return float(b * b - 4.0 * a * k_eff)


def classify_auxiliary_case(pp: PlantParams, tol: float = 1e-6) -> dict[str, Any]:
    """
    Caso I: Δ > 0 (raíces reales distintas).
    Caso II: Δ ≈ 0 (raíz real doble).
    Caso III: Δ < 0 (raíces complejas conjugadas).
    """
    delta = discriminant_auxiliary(pp)
    s1, s2 = characteristic_roots(pp)
    if delta > tol:
        case_id, case_name = "I", "Raíces reales diferentes"
    elif delta < -tol:
        case_id, case_name = "III", "Raíces complejas conjugadas"
    else:
        case_id, case_name = "II", "Raíces reales iguales"
    alpha = float(s1.real)
    beta = float(abs(s1.imag))
    return {
        "case_id": case_id,
        "case_name": case_name,
        "delta": delta,
        "s1": s1,
        "s2": s2,
        "alpha": alpha,
        "beta": beta,
        "stable": s1.real < 0 and s2.real < 0,
    }


def k_s_diapositiva(pp: PlantParams) -> float:
    """Rigidez magnética como en diapositivas (valor positivo si ks < 0 en el modelo)."""
    return float(abs(pp.ks) if pp.ks < 0 else pp.ks)


def ki_kp_minus_ks_slide(pp: PlantParams) -> float:
    """Coeficiente de $x$ en diapositivas: $k_i K_p - k_s$ (con $k_s>0$ del tablero)."""
    return float(pp.ki * pp.Kp - k_s_diapositiva(pp))


def leibniz_ode_general_text() -> str:
    """Plantilla simbólica del cuaderno (sin sustituir números)."""
    return (
        r"m\,\frac{d^2x}{dt^2} + (c + k_i K_d)\,\frac{dx}{dt} "
        r"+ (k_i K_p - k_s)\,x = 0"
    )


def leibniz_ode_text(pp: PlantParams) -> str:
    """
    E.D.O. homogénea con parámetros ya sustituidos (forma numérica del tablero).
    """
    m = pp.m
    b = b_effective(pp)
    k = ki_kp_minus_ks_slide(pp)
    d2 = r"\frac{d^2x}{dt^2}" if abs(m - 1.0) < 1e-12 else rf"{m:g}\,\frac{{d^2x}}{{dt^2}}"
    parts = [d2]
    if abs(b) > 1e-12:
        parts.append(rf"+ {b:g}\,\frac{{dx}}{{dt}}")
    if abs(k) > 1e-12:
        parts.append(r"+ x" if abs(k - 1.0) < 1e-12 else rf"+ {k:g}\,x")
    return " ".join(parts) + r" = 0"


def leibniz_discriminant_text(pp: PlantParams, delta: float | None = None) -> str:
    """Δ con sustitución numérica (como en diapositivas)."""
    b = b_effective(pp)
    ks = k_s_diapositiva(pp)
    k_lin = ki_kp_minus_ks_slide(pp)
    d = float(delta) if delta is not None else discriminant_auxiliary(pp)
    damp_sub = rf"({pp.c:g} + {pp.ki:g}\cdot{pp.Kd:g})"
    k_sub = rf"({pp.ki:g}\cdot{pp.Kp:g} - {ks:g})"
    return (
        r"\Delta = (c + k_i K_d)^2 - 4m(k_i K_p - k_s) "
        rf"= {damp_sub}^2 - 4\cdot{pp.m:g}\cdot{k_sub} "
        rf"= {b:g}^2 - 4\cdot{pp.m:g}\cdot({k_lin:g}) = {d:g}"
    )


def auxiliary_polynomial_text(pp: PlantParams) -> str:
    """Polinomio característico con coeficientes numéricos (equivalente a la E.D.O.)."""
    m = pp.m
    b = b_effective(pp)
    k = ki_kp_minus_ks_slide(pp)
    lead = "s^2" if abs(m - 1.0) < 1e-12 else rf"{m:g}\,s^2"
    kc = "1" if abs(k - 1.0) < 1e-12 else f"{k:g}"
    return rf"{lead} + {b:g}\,s + {kc} = 0"


def analytic_response(t: np.ndarray, pp: PlantParams, x0: float, v0: float) -> np.ndarray:
    """Solución analítica de la E.D.O. continua según tipo de raíz (CI en t=0)."""
    t = np.asarray(t, dtype=float)
    s1, s2 = characteristic_roots(pp)
    delta = discriminant_auxiliary(pp)
    if delta > 1e-9:
        # Raíces reales distintas
        if abs(s1 - s2) < 1e-12:
            delta = 0.0
        else:
            c2 = (v0 - s1 * x0) / (s2 - s1)
            c1 = x0 - c2
            return np.real(c1 * np.exp(s1 * t) + c2 * np.exp(s2 * t))
    if abs(delta) <= 1e-9:
        s = s1
        c1 = x0
        c2 = v0 - s * x0
        return np.real((c1 + c2 * t) * np.exp(s * t))
    alpha = float(s1.real)
    beta = float(s1.imag)
    if abs(beta) < 1e-12:
        c1 = x0
        c2 = v0 - alpha * x0
        return np.real((c1 + c2 * t) * np.exp(alpha * t))
    c1 = x0
    c2 = (v0 - alpha * x0) / beta
    expat = np.exp(alpha * t)
    return np.real(expat * (c1 * np.cos(beta * t) + c2 * np.sin(beta * t)))


def k_effective(pp: PlantParams) -> float:
    return pp.ks + pp.ki * pp.Kp


def b_effective(pp: PlantParams) -> float:
    return pp.c + pp.ki * pp.Kd


def stability_routh(pp: PlantParams) -> dict[str, Any]:
    """Condiciones del PDF: m>0, c+k_i K_d>0, k_s+k_i K_p>0 para coeficientes >0."""
    m_ok = pp.m > 0
    b_ok = b_effective(pp) > 0
    k_ok = k_effective(pp) > 0
    s1, s2 = characteristic_roots(pp)
    poles_ok = s1.real < 0 and s2.real < 0
    return {
        "m_ok": m_ok,
        "b_ok": b_ok,
        "k_ok": k_ok,
        "poles_ok": poles_ok,
        "s1": s1,
        "s2": s2,
        "k_eff": k_effective(pp),
        "b_eff": b_effective(pp),
    }


def ode_rhs(y: np.ndarray, t: float, pp: PlantParams) -> np.ndarray:
    x, v = float(y[0]), float(y[1])
    return np.array(
        [v, (-b_effective(pp) * v - k_effective(pp) * x) / pp.m],
        dtype=float,
    )


def simulate_continuous(pp: PlantParams, t: np.ndarray, x0: float, v0: float) -> np.ndarray:
    y0 = np.array([x0, v0], dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return odeint(ode_rhs, y0, t, args=(pp,), rtol=1e-9, atol=1e-11)


def clip_i(i: float, imax: float | None) -> float:
    if imax is None or imax <= 0:
        return i
    return float(np.clip(i, -imax, imax))


def simulate_digital(
    pp: PlantParams,
    dp: DigitalParams,
    t: np.ndarray,
    x0: float,
    v0: float,
    y0_scale: float = 0.28,
    imax: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    m, c, ks, ki = pp.m, pp.c, pp.ks, pp.ki
    Kp, Kd = pp.Kp, pp.Kd
    Ts, tau = max(dp.Ts, 1e-9), dp.tau
    n = len(t)
    dt = float(t[1] - t[0]) if n > 1 else 1.0
    x = np.zeros(n)
    y = np.zeros(n)
    vx = np.zeros(n)
    vy = np.zeros(n)
    x[0], y[0] = x0, x0 * y0_scale
    vx[0], vy[0] = v0, v0

    cap = max(64, int(np.ceil(tau / dt)) + 16)
    buf_t = np.zeros(cap)
    buf_x = np.zeros(cap)
    buf_y = np.zeros(cap)
    buf_vx = np.zeros(cap)
    buf_vy = np.zeros(cap)
    ri, rc = 0, 0

    def push(tt: float, xx: float, yy: float, vvx: float, vvy: float) -> None:
        nonlocal ri, rc
        buf_t[ri], buf_x[ri], buf_y[ri], buf_vx[ri], buf_vy[ri] = tt, xx, yy, vvx, vvy
        ri = (ri + 1) % cap
        rc = min(cap, rc + 1)

    def snap() -> tuple[np.ndarray, ...]:
        if rc < cap:
            o, sl = np.arange(rc), slice(0, rc)
        else:
            o, sl = np.roll(np.arange(cap), -ri), slice(None)
        return buf_t[o][sl], buf_x[o][sl], buf_y[o][sl], buf_vx[o][sl], buf_vy[o][sl]

    def interp(th: np.ndarray, xh: np.ndarray, vh: np.ndarray, tq: float, xi: float, vi: float) -> tuple[float, float]:
        if len(th) == 0:
            return xi, vi
        if tq <= th[0]:
            return float(xh[0]), float(vh[0])
        if tq >= th[-1]:
            return float(xh[-1]), float(vh[-1])
        return float(np.interp(tq, th, xh)), float(np.interp(tq, th, vh))

    def rk4(xx: float, vv: float, ff: float) -> tuple[float, float]:
        def rhs(xp: float, vp: float, f: float) -> tuple[float, float]:
            return vp, (-c * vp - ks * xp + f) / m

        k1x, k1v = rhs(xx, vv, ff)
        k2x, k2v = rhs(xx + 0.5 * dt * k1x, vv + 0.5 * dt * k1v, ff)
        k3x, k3v = rhs(xx + 0.5 * dt * k2x, vv + 0.5 * dt * k2v, ff)
        k4x, k4v = rhs(xx + dt * k3x, vv + dt * k3v, ff)
        return (
            xx + (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x),
            vv + (dt / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v),
        )

    push(0.0, x[0], y[0], vx[0], vy[0])
    k_last, Fx, Fy = -1, 0.0, 0.0
    for i in range(n - 1):
        tt = float(t[i])
        kp = int(np.floor(tt / Ts + 1e-12))
        if kp != k_last:
            k_last = kp
            tq = kp * Ts - tau
            th, xh, yh, vxh, vyh = snap()
            xm, vm = interp(th, xh, vxh, tq, x0, v0)
            ym, vym = interp(th, yh, vyh, tq, x0 * y0_scale, v0)
            Fx = ki * clip_i(-(Kp * xm + Kd * vm), imax)
            Fy = ki * clip_i(-(Kp * ym + Kd * vym), imax)
        x[i + 1], vx[i + 1] = rk4(x[i], vx[i], Fx)
        y[i + 1], vy[i + 1] = rk4(y[i], vy[i], Fy)
        push(float(t[i + 1]), x[i + 1], y[i + 1], vx[i + 1], vy[i + 1])
    return x, y, vx, vy


def run_case(
    pp: PlantParams,
    dp: DigitalParams,
    t_end: float,
    npts: int,
    x0: float,
    v0: float,
    clearance: float,
    imax: float | None = None,
    y0_scale: float = 0.28,
    use_digital: bool = True,
) -> dict[str, Any]:
    t = np.linspace(0.0, t_end, npts)
    r = stability_routh(pp)
    aux = classify_auxiliary_case(pp)
    yc = simulate_continuous(pp, t, x0, v0)
    xc = yc[:, 0]
    vc = yc[:, 1]
    xa = analytic_response(t, pp, x0, v0)
    if use_digital:
        xd, yd, vxd, vyd = simulate_digital(pp, dp, t, x0, v0, y0_scale=y0_scale, imax=imax)
    else:
        xd = xc.copy()
        yd = xc * y0_scale
        vxd = vc.copy()
        vyd = vc * y0_scale
    amp_c = float(np.max(np.abs(xc)))
    amp_d = float(np.max(np.abs(xd)))
    amp_o = float(np.max(np.hypot(xd, yd)))
    unstable = not r["poles_ok"]
    contact = amp_c > clearance or amp_d > clearance or amp_o > clearance
    return {
        "t": t,
        "x_cont": xc,
        "v_cont": vc,
        "x_analytic": xa,
        "x_dig": xd,
        "y_dig": yd,
        "vx_dig": vxd,
        "vy_dig": vyd,
        "routh": r,
        "aux": aux,
        "amp_cont_um": amp_c * 1e6,
        "amp_dig_um": amp_d * 1e6,
        "unstable": unstable,
        "contact": contact,
        "alert": unstable or contact,
        "use_digital": use_digital,
    }
