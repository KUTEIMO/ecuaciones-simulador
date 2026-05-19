# -*- coding: utf-8 -*-
"""Render del guion: bloques $$ con st.latex (evita plantillas {dx}, {-t}, etc.)."""

from __future__ import annotations

import re

import streamlit as st

_INLINE_MATH = re.compile(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)")


def _normalize_delimiters(text: str) -> str:
    if not text:
        return text
    out = text
    out = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", out, flags=re.DOTALL)
    out = re.sub(r"\\\((.*?)\\\)", r"$\1$", out, flags=re.DOTALL)
    out = re.sub(r"(?m)^\\\[\s*$", "$$", out)
    out = re.sub(r"(?m)^\\\]\s*$", "$$", out)
    out = re.sub(r"\$\$\s*\$\$", "$$", out)
    return out


def _escape_inline_for_markdown(text: str) -> str:
    """st.markdown interpreta {clave} dentro de $...$ en línea."""

    def _double(m: re.Match[str]) -> str:
        body = m.group(1).replace("{", "{{").replace("}", "}}")
        return "$" + body + "$"

    return _INLINE_MATH.sub(_double, text)


def md(text: str) -> None:
    """Markdown alternado con st.latex (partir por $$, sin regex ambigua)."""
    text = _normalize_delimiters(text)
    parts = text.split("$$")
    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part:
                st.markdown(_escape_inline_for_markdown(part))
        else:
            body = part.strip()
            if body:
                st.latex(body)
