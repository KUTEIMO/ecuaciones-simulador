# -*- coding: utf-8 -*-
"""
Escena 3D para exposición: estator, holgura, electroimanes (cruz), eje, disco y palas.
Todo en metros; (x_m, y_m) de la simulación se amplifican con visual_gain.
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go


def make_bearing_scene(
    x_m: float,
    y_m: float,
    clearance_m: float,
    spin_rad: float,
    visual_gain: float,
    state: str,
) -> go.Figure:
    ox = float(x_m * visual_gain)
    oy = float(y_m * visual_gain)
    pal = {
        "stable": ("#34495e", "#27ae60", "#2980b9", "#85c1e9"),
        "marginal": ("#9a7d0a", "#f39c12", "#d68910", "#f9e79f"),
        "danger": ("#78281f", "#e74c3c", "#c0392b", "#fadbd8"),
    }
    st_c, sh_c, hub_c, bl_c = pal.get(state, pal["stable"])

    fig = go.Figure()

    # Estator: varios círculos apilados (tubo visual)
    R_out = 0.10
    for z in np.linspace(-0.028, 0.028, 7):
        th = np.linspace(0, 2 * np.pi, 80)
        zf = float(z)
        fig.add_trace(
            go.Scatter3d(
                x=R_out * np.cos(th),
                y=R_out * np.sin(th),
                z=np.full_like(th, zf),
                mode="lines",
                line=dict(color=st_c, width=3),
                name="Estator" if zf < -0.02 else None,
                showlegend=bool(zf < -0.02),
            )
        )

    R_in = 0.056
    # Electroimanes: segmentos radiales
    for k, ang in enumerate((0, np.pi / 2, np.pi, 3 * np.pi / 2)):
        r1, r2 = R_in * 0.88, R_out * 0.92
        fig.add_trace(
            go.Scatter3d(
                x=[r1 * np.cos(ang), r2 * np.cos(ang)],
                y=[r1 * np.sin(ang), r2 * np.sin(ang)],
                z=[0.0, 0.0],
                mode="lines",
                line=dict(color="#1f618d", width=8),
                name="Electroimán" if k == 0 else None,
                showlegend=bool(k == 0),
            )
        )

    c_show = max(R_in * 0.9, R_in * 0.9 + clearance_m * visual_gain * 0.45)
    thh = np.linspace(0, 2 * np.pi, 90)
    fig.add_trace(
        go.Scatter3d(
            x=c_show * np.cos(thh),
            y=c_show * np.sin(thh),
            z=np.zeros_like(thh),
            mode="lines",
            line=dict(color="#c0392b", width=5),
            name="Holgura / backup",
        )
    )

    # Eje: hélice de círculos desplazados (ox, oy)
    r_shaft = 0.022
    zs = np.linspace(-0.17, 0.20, 22)
    for iz, z in enumerate(zs):
        zf = float(z)
        th = np.linspace(0, 2 * np.pi, 36)
        fig.add_trace(
            go.Scatter3d(
                x=ox + r_shaft * np.cos(th),
                y=oy + r_shaft * np.sin(th),
                z=np.full_like(th, zf),
                mode="lines",
                line=dict(color=sh_c, width=2),
                name="Eje" if iz == 0 else None,
                showlegend=bool(iz == 0),
            )
        )

    z_disk = 0.20
    R_bl = 0.092
    n_b = 8
    for k in range(n_b):
        ang0 = 2 * np.pi * k / n_b + spin_rad
        x1 = ox + R_bl * np.cos(ang0)
        y1 = oy + R_bl * np.sin(ang0)
        fig.add_trace(
            go.Scatter3d(
                x=[ox, x1],
                y=[oy, y1],
                z=[z_disk, z_disk],
                mode="lines",
                line=dict(color=bl_c, width=4),
                name="Palas turbina" if k == 0 else None,
                showlegend=bool(k == 0),
            )
        )
    th2 = np.linspace(0, 2 * np.pi, 40)
    fig.add_trace(
        go.Scatter3d(
            x=ox + 0.03 * np.cos(th2),
            y=oy + 0.03 * np.sin(th2),
            z=np.full_like(th2, z_disk),
            mode="lines",
            line=dict(color=hub_c, width=5),
            name="Disco",
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[ox],
            y=[oy],
            z=[0.0],
            mode="markers",
            marker=dict(size=11, color="orange", symbol="diamond", line=dict(width=1, color="black")),
            name="Centro simulado (x,y)",
        )
    )

    ttl = "AMB + eje + turbina (3D educativa)"
    if state == "danger":
        ttl += " — contacto o inestabilidad"
    elif state == "marginal":
        ttl += " — régimen marginal"

    fig.update_layout(
        title=ttl,
        scene=dict(
            xaxis_title="X [m]",
            yaxis_title="Y [m]",
            zaxis_title="Z [m]",
            aspectmode="data",
            camera=dict(eye=dict(x=1.5, y=-1.55, z=0.5)),
        ),
        height=540,
        margin=dict(t=48, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
    )
    return fig


def make_orbit_3d(t: np.ndarray, x: np.ndarray, y: np.ndarray, clearance_m: float, z_mm_per_s: float) -> go.Figure:
    z = z_mm_per_s * t
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=x * 1e6,
            y=y * 1e6,
            z=z,
            mode="lines",
            line=dict(width=4, color="#1a5276"),
            name="Órbita",
            customdata=t,
            hovertemplate="x=%{x:.1f} µm y=%{y:.1f} µm t=%{customdata:.4f}s<extra></extra>",
        )
    )
    cu = clearance_m * 1e6
    th = np.linspace(0, 2 * np.pi, 80)
    fig.add_trace(
        go.Scatter3d(
            x=cu * np.cos(th),
            y=cu * np.sin(th),
            z=np.zeros_like(th),
            mode="lines",
            line=dict(color="red", width=3),
            name="Clearance",
        )
    )
    fig.update_layout(
        title="Órbita en µm; eje vertical = tiempo (mm)",
        scene=dict(xaxis_title="x µm", yaxis_title="y µm", zaxis_title="z [mm]", aspectmode="data"),
        height=420,
    )
    return fig
