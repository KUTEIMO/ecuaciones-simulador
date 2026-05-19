# -*- coding: utf-8 -*-
"""Exportación PNG para diapositivas."""

from __future__ import annotations

import io

import matplotlib.pyplot as plt


def fig_to_png_bytes(fig: plt.Figure, dpi: int = 150) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
