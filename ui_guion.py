# -*- coding: utf-8 -*-
"""Página /guion — estudio rápido Grupo 6."""

from __future__ import annotations

import streamlit as st

from guion_expo import (
    APERTURA_TODOS,
    CHEAT_ARBEY,
    CHEAT_EDUARDO,
    CHEAT_KAROL,
    CHEAT_PREGUNTAS,
    CONCEPTOS_TODOS,
    CRITERIOS_EVALUACION,
    GUION_SUBTITLE,
    GUION_TITLE,
    QUICK_REFERENCE,
    SECTIONS,
    TIMING_TOTAL,
)
from guion_latex import md

st.set_page_config(
    page_title="Guion Grupo 6",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_guion_page() -> None:
    st.title(GUION_TITLE)
    st.caption(GUION_SUBTITLE)
    st.markdown("**Uso interno** — solo el equipo. App: `http://localhost:8501/`")

    tab0, tab_k, tab_a, tab_r, tab_e, tab_p, tab_full = st.tabs(
        [
            "Todos (5 ideas)",
            "Karol",
            "Alexis",
            "Arbey",
            "Eduardo",
            "Preguntas",
            "Guion completo",
        ]
    )

    with tab0:
        md(CONCEPTOS_TODOS)
        st.divider()
        md(APERTURA_TODOS)
        st.info(TIMING_TOTAL)

    with tab_k:
        md(CHEAT_KAROL)
        sec = next(s for s in SECTIONS if s["id"] == "karol")
        st.divider()
        st.markdown(f"**Diapositivas:** {sec['slide']}")
        st.markdown(f"**Menú app:** {sec['sim']}")
        md(sec["text"])

    with tab_a:
        st.error(
            "**ALEXIS — Tú copias en el tablero.** "
            "Baja a la sección **«COPIAR EN EL TABLERO»** y sigue las líneas en orden (Bloques A → H)."
        )
        sec = next(s for s in SECTIONS if s["id"] == "alexis")
        st.markdown(f"**Diapositivas:** {sec['slide']}")
        st.markdown(f"**Menú app (al final):** {sec['sim']}")
        md(sec["text"])

    with tab_r:
        md(CHEAT_ARBEY)
        sec = next(s for s in SECTIONS if s["id"] == "arbey")
        st.divider()
        st.markdown(f"**Diapositivas:** {sec['slide']}")
        st.markdown(f"**Menú app:** {sec['sim']}")
        md(sec["text"])

    with tab_e:
        md(CHEAT_EDUARDO)
        sec = next(s for s in SECTIONS if s["id"] == "eduardo")
        st.divider()
        st.markdown(f"**Diapositivas:** {sec['slide']}")
        st.markdown(f"**Menú app:** {sec['sim']}")
        md(sec["text"])

    with tab_p:
        md(CHEAT_PREGUNTAS)

    with tab_full:
        with st.expander("Checklist profesor", expanded=False):
            md(QUICK_REFERENCE)
        with st.expander("Criterios evaluación", expanded=False):
            md(CRITERIOS_EVALUACION)
        for i, block in enumerate(SECTIONS, 1):
            st.markdown(f"### {i}. {block['speaker']}")
            st.caption(f"{block['duration']} · {block['slide']}")
            st.markdown(f"**Menú app:** {block['sim']}")
            md(block["text"])


render_guion_page()
