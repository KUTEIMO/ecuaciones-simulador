# -*- coding: utf-8 -*-
"""
Guion Grupo 6 — estudio rápido (20-25 min de exposición).
URL: http://localhost:8501/guion
"""

from __future__ import annotations

GUION_TITLE = "Guion Grupo 6 — estudio rápido"
GUION_SUBTITLE = "Cada integrante: su pestaña aquí + el caso correspondiente en el menú de la app."

# ---------------------------------------------------------------------------
# Lo mínimo que TODOS deben memorizar (1 minuto)
# ---------------------------------------------------------------------------
CONCEPTOS_TODOS = r"""
### Si solo recuerdan 5 cosas

1. **E.D.O. del rotor:** $m\dfrac{d^2x}{dt^2} + (c + k_i K_d)\dfrac{dx}{dt} + (k_i K_p - k_s)x = 0$

2. **Ecuación auxiliar:** sustituir $x = e^{st}$ → $m s^2 + (c + k_i K_d)s + (k_i K_p - k_s) = 0$

3. **Estable** = todas las raíces con parte real **negativa** (semplano **izquierdo** del plano $s$)

4. **Inestable** = alguna raíz con parte real **positiva** (semiplano **derecho**) → el eje puede chocar

5. **Tres casos según $\Delta$:**
   - $\Delta > 0$ → **Caso I** — raíces reales distintas
   - $\Delta = 0$ → **Caso II** — raíz real doble
   - $\Delta < 0$ → **Caso III** — raíces complejas $s = \alpha \pm \beta i$
"""

CHEAT_KAROL = r"""
### KAROL — tu bloque (~5 min) | Diapositivas 2, 3, 4, 5

**Menú app:** `Caso I — Raíces reales diferentes`  
**Panel:** abrir «Desarrollo paso a paso» (pasos 1 a 5)

| Qué | Detalle |
|-----|---------|
| Idea en una frase | Dos raíces reales distintas → el eje vuelve al centro **sin vibrar** |
| Fórmula clave | $x(t) = C_1 e^{s_1 t} + C_2 e^{s_2 t}$ con $\Delta > 0$ |
| Qué decir al inicio | «El imán solo no basta: hay rigidez negativa; hace falta control. Esta es la E.D.O. y su ecuación auxiliar.» |
| En la app | Pasos 1 y 2, luego gráfica $x(t)$ y plano $s$ (dos puntos en el eje real) |
| Ejercicio | Leer $\Delta$ y $s_1$, $s_2$ en las métricas; escribirlos en el tablero |
| Interpretación | «Re(s) < 0 → estable. En 3D el eje queda dentro del anillo rojo al mover el tiempo.» |
| Cierre | «Alexis explica el Caso II, raíces reales iguales.» |
"""

ALEXIS_TABLERO = r"""
---
## ALEXIS — COPIAR EN EL TABLERO (orden exacto, sin saltar líneas)

**Diapositiva 6 · Caso II — Raíces reales iguales ($\Delta = 0$)**  
Mientras escribes, di en voz alta qué estás haciendo. Al terminar el tablero, en la app elige **Caso II — Raíces reales iguales** y muestra las gráficas.

---

### BLOQUE A — Título y datos (escribir arriba a la izquierda)

```
CASO II — RAÍCES REALES IGUALES (Δ = 0)
Amortiguamiento crítico — AMB (Caso II)
```

**Datos de la planta (copiar tal cual):**

| Símbolo | Valor | Unidad |
|---------|-------|--------|
| $m$ | $1$ | kg |
| $c$ | $0$ | N·s/m |
| $k_i$ | $1$ | — |
| $K_p$ | $2$ | — |
| $K_d$ | $2$ | — |
| $k_s$ | $1$ | N/m (rigidez magnética inestable, diapositivas) |

---

### BLOQUE B — E.D.O. (forma general del cuaderno)

**Línea 1 — plantilla:**

$$
m\frac{d^2x}{dt^2} + (c + k_i K_d)\frac{dx}{dt} + (k_i K_p - k_s)\,x = 0
$$

**Línea 2 — sustituir $m$, $c$, $k_i$, $K_p$, $K_d$, $k_s$ (mostrar cada paréntesis):**

$$
(1)\frac{d^2x}{dt^2} + \bigl(0 + (1)(2)\bigr)\frac{dx}{dt} + \bigl((1)(2) - 1\bigr)x = 0
$$

**Línea 3 — operar dentro de cada paréntesis:**

$$
\frac{d^2x}{dt^2} + (0 + 2)\frac{dx}{dt} + (2 - 1)x = 0
$$

**Línea 4 — resultado intermedio:**

$$
\frac{d^2x}{dt^2} + 2\frac{dx}{dt} + x = 0
$$

---

### BLOQUE C — Método de la solución $x = e^{st}$ (todo el procedimiento)

**Línea 5 — hipótesis del cuaderno:**

$$
x(t) = e^{st}
$$

**Línea 6 — primera derivada (regla de la cadena, escribir el paso):**

$$
\frac{dx}{dt} = \frac{d}{dt}\bigl(e^{st}\bigr) = s\,e^{st}
$$

**Línea 7 — segunda derivada:**

$$
\frac{d^2x}{dt^2} = \frac{d}{dt}\bigl(s\,e^{st}\bigr) = s^2\,e^{st}
$$

**Línea 8 — sustituir (3) en la E.D.O. (línea 4):**

$$
s^2 e^{st} + 2s\,e^{st} + e^{st} = 0
$$

**Línea 9 — factor común $e^{st}$ (explicar: $e^{st} \neq 0$):**

$$
e^{st}\bigl(s^2 + 2s + 1\bigr) = 0
$$

**Línea 10 — ecuación auxiliar:**

$$
s^2 + 2s + 1 = 0
$$

---

### BLOQUE D — Discriminante (fórmula + sustitución completa)

**Línea 11 — forma general con coeficientes del polinomio $as^2 + bs + c = 0$:**

Identificar en la línea 10:  
$a = 1$, $\quad b = 2$, $\quad c = 1$

**Línea 12 — fórmula del discriminante (como diapositivas):**

$$
\Delta = b^2 - 4ac = (c + k_i K_d)^2 - 4m(k_i K_p - k_s)
$$

**Línea 13 — sustituir números en $(c + k_i K_d)$:**

$$
c + k_i K_d = 0 + (1)(2) = 0 + 2 = 2
$$

**Línea 14 — sustituir números en $(k_i K_p - k_s)$:**

$$
k_i K_p - k_s = (1)(2) - 1 = 2 - 1 = 1
$$

**Línea 15 — calcular $\Delta$ paso a paso:**

$$
\Delta = (2)^2 - 4(1)(1) = 4 - 4 = 0
$$

**Línea 16 — conclusión del caso:**

$$
\Delta = 0 \Rightarrow \text{Caso II, raíz real doble}
$$

---

### BLOQUE E — Calcular la raíz $s$ (sin saltar la fórmula)

**Línea 17 — fórmula de raíz doble (cuando $\Delta = 0$):**

$$
s = -\frac{b}{2a} = -\frac{c + k_i K_d}{2m}
$$

**Línea 18 — sustituir $a$, $b$, $m$, $c$, $k_i$, $K_d$:**

$$
s = -\frac{0 + (1)(2)}{2(1)} = -\frac{2}{2}
$$

**Línea 19 — resultado:**

$$
s = -1 \quad (s_1 = s_2 = -1,\ \text{raíz doble})
$$

**Línea 20 — comprobar en la ecuación auxiliar:**

$$
s^2 + 2s + 1 = (-1)^2 + 2(-1) + 1 = 1 - 2 + 1 = 0 \quad\checkmark
$$

---

### BLOQUE F — Solución general del Caso II

**Línea 21 — plantilla (cuaderno / diapositiva):**

$$
x(t) = (C_1 + C_2\,t)\,e^{st}
$$

**Línea 22 — sustituir $s = -1$:**

$$
x(t) = (C_1 + C_2\,t)\,e^{-t}
$$

**Línea 23 — por qué aparece $t$ (una frase al lado):**

«Las dos raíces son iguales; por eso la solución general lleva el factor $t$.»

---

### BLOQUE G — Condiciones iniciales y constantes (procedimiento completo)

**Línea 24 — datos iniciales:**

$$
x(0) = x_0 = 0{,}002\ \mathrm{m} = 2\ \mathrm{mm}, \qquad \left. \frac{dx}{dt} \right|_{t=0} = v_0 = 0
$$

**Línea 25 — calcular C₁ con t = 0:**

$$
\begin{aligned}
x(0) &= (C_1 + C_2 \cdot 0)\,e^{0} = C_1 \cdot 1 = C_1 \\
C_1 &= x_0 = 0{,}002
\end{aligned}
$$

**Línea 26 — derivar x(t) para hallar C₂ (mostrar producto, sin saltar):**

$$
\begin{aligned}
x(t) &= (C_1 + C_2 t)e^{-t} \\
\frac{dx}{dt} &= C_2\,e^{-t} + (C_1 + C_2 t)\cdot(-1)\,e^{-t} \\
\frac{dx}{dt} &= e^{-t}(C_2 - C_1 - C_2 t)
\end{aligned}
$$

**Línea 27 — evaluar en t = 0:**

$$
\begin{aligned}
\left. \frac{dx}{dt} \right|_{t=0} &= e^{0}(C_2 - C_1 - 0) = C_2 - C_1 \\
v_0 &= C_2 - C_1
\end{aligned}
$$

**Línea 28 — despejar $C_2$:**

$$
C_2 = v_0 + C_1 = 0 + 0{,}002 = 0{,}002
$$

Comprobación con fórmula del cuaderno: $C_2 = v_0 - s\,x_0 = 0 - (-1)(0{,}002) = 0{,}002$.

**Línea 29 — solución particular de este ejemplo:**

$$
x(t) = (0{,}002 + 0{,}002\,t)\,e^{-t}\ \mathrm{m}
$$

---

### BLOQUE H — Interpretación (escribir al final del tablero)

```
INTERPRETACIÓN (leer al auditorio):
• Re(s) = -1 < 0  →  ESTABLE (polo en semiplano izquierdo)
• No hay sen/cos  →  NO oscila (a diferencia del Caso III)
• Δ = 0           →  amortiguamiento CRÍTICO: vuelve al centro lo más
                      rápido posible sin vibrar
• Gráfica x(t) decae; plano s muestra un solo polo en s = -1
• 3D: el eje vuelve al centro sin espiral marcada
```

**Frase de cierre (Alexis):** «Entrego a Arbey: **Caso III — raíces complejas conjugadas**.»

---

### CHECKLIST Alexis (antes de borrar el tablero)

- [ ] ¿Quedó escrita la E.D.O. desde la plantilla hasta la forma numérica?
- [ ] ¿Se ve el paso $x = e^{st}$ con las dos derivadas?
- [ ] ¿Está $\Delta = 0$ con sustitución explícita?
- [ ] ¿Está $s = -1$ con la fracción $-\dfrac{c + k_i K_d}{2m}$?
- [ ] ¿Están $C_1$, $C_2$, $x(t)$ final y las unidades [m]?
"""

CHEAT_ALEXIS = r"""
### ALEXIS — tu bloque (~5 min) | Diapositiva 6

**Tú copias en el tablero.** La sección **«COPIAR EN EL TABLERO»** más abajo tiene **cada línea en orden** (no te saltes ningún paso).

**Menú app:** `Caso II — Raíces reales iguales` (abrir **después** de terminar el tablero o en el Bloque H).

| Qué | Detalle |
|-----|---------|
| Idea en una frase | Raíz **doble** ($\Delta = 0$) → vuelve al centro **rápido** y **sin oscilar** |
| Resultado numérico | $s = -1$, $\Delta = 0$, $x(t) = (0{,}002 + 0{,}002t)e^{-t}$ |
| Qué decir mientras copias | «Voy sustituyendo los datos en la E.D.O.… ahora planteo $x=e^{st}$… calculo $\Delta$…» |
| Interpretación | Amortiguamiento **crítico**; $\mathrm{Re}(s) < 0$ → estable |
| Cierre | «Arbey presenta el **Caso III — raíces complejas conjugadas**.» |
"""

CHEAT_ARBEY = r"""
### ARBEY — tu bloque (~5 min) | Diapositivas 7, 8, 9

**Menú app:** primero `Caso III — Raíces complejas conjugadas`, luego (30 s) `AMB — Control digital interactivo`

| Qué | Detalle |
|-----|---------|
| Idea en una frase | Raíces complejas → el eje **vibra**; si $\alpha < 0$ la vibración **se apaga** |
| Fórmula clave | $x(t) = e^{\alpha t}[C_1\cos(\beta t) + C_2\sin(\beta t)]$ |
| $\alpha$ | Parte real de $s$: si es negativa, **estable** |
| $\beta$ | Frecuencia de la oscilación |
| Plano $s$ | Izquierda = seguro / Derecha = peligro |
| Ejercicio | Leer $\alpha$ y $\beta$ en métricas; mostrar gráfica de envolvente |
| Interpretación | «Los polos deben quedar a la izquierda; si $\alpha > 0$ la respuesta es inestable.» |
| Cierre | «Eduardo muestra la turbina X-100, casos A y B.» |
"""

CHEAT_EDUARDO = r"""
### EDUARDO — tu bloque (~5 min) | Diapositivas 10 a 14

**Menú app:** `Turbina X-100 — Caso A` y luego `Turbina X-100 — Caso B`  
**Panel:** Paso 6 en «Desarrollo paso a paso» en cada uno

| Qué | Caso A (MAL) | Caso B (BIEN) |
|-----|--------------|---------------|
| $K_p$, $K_d$ | 15, 0 | 30, 6 |
| E.D.O. | $\dfrac{d^2x}{dt^2} - 5x = 0$ | $\dfrac{d^2x}{dt^2} + 6\dfrac{dx}{dt} + 10x = 0$ |
| Raíces | $s = \pm\sqrt{5} \approx \pm 2{,}23$ | $s = -3 \pm i$ |
| Tipo | Caso I (una raíz **positiva**) | Caso III con $\alpha = -3 < 0$ |
| 3D | Eje **sale** del anillo rojo | Eje **dentro** del anillo |
| Banner | **Inestable** | **Estable** |

**Qué decir (Caso A):** «$K_d = 0$: no hay amortiguamiento digital. La raíz $+\sqrt{5}$ hace crecer $e^{2.23t}$ → colisión.»

**Qué decir (Caso B):** «Subimos $K_p$ y $K_d$; polos en $-3 \pm i$. Espiral estable dentro de la holgura.»

**Comparación (tablero):** misma turbina, distinto control → distinto destino.

**Cierre:** «El control mueve los polos al semiplano izquierdo. Gracias, preguntas.»
"""

CHEAT_PREGUNTAS = r"""
### Preguntas — quién responde

| Pregunta | Responde |
|----------|----------|
| E.D.O., $\Delta$, Caso I | Karol |
| Raíz doble, $\Delta = 0$ | Alexis |
| $\alpha$, $\beta$, plano $s$, digital | Arbey |
| Turbina, Caso A/B, 3D | Eduardo |

**Respuestas de una línea:**
- ¿Por qué falla A? → $K_d = 0$ y raíz positiva $+\sqrt{5}$.
- ¿Qué es estable? → $\mathrm{Re}(s) < 0$ para todas las raíces.
- ¿Qué es $\alpha$? → parte real de $s$; negativa = amortigua.
"""

APERTURA_TODOS = r"""
### Apertura (todos, 15-20 s cada uno) — Diapositiva 1

**Karol:** «Buenos días. Somos el Grupo 6. Tema: estabilidad dinámica en cojinetes magnéticos activos en una turbina de alta velocidad.»

**Alexis:** «Usamos la ecuación auxiliar: el tipo de raíces dice si el rotor levita o choca con el estator.»

**Arbey:** «Veremos tres casos matemáticos y un simulador en vivo.»

**Eduardo:** «Cerramos con la turbina X-100: un diseño que falla y uno que funciona. Unos veinte minutos. Empezamos.»
"""

SECTIONS: list[dict[str, str]] = [
    {
        "id": "karol",
        "speaker": "KAROL — guion completo",
        "duration": "~5,5 min",
        "slide": "Diapositivas 2, 3, 4, 5",
        "sim": "Bloque: **Caso I — Raíces reales diferentes**. Desarrollo paso a paso (1-5). Gráficas + 3D.",
        "text": CHEAT_KAROL
        + r"""

---

#### Guion palabra por palabra (expandir si tienes tiempo)

**Diapo 2 (30 s):** «Sin rodamiento hay poca fricción, pero el imán empuja el eje hacia el estator. Necesitamos electrónica que corrija eso.»

**Diapo 3 (1 min):** Leer la E.D.O. en la app (Paso 1):

$$
m\frac{d^2x}{dt^2} + (c + k_i K_d)\frac{dx}{dt} + (k_i K_p - k_s)x = 0
$$

**Diapo 4 (1 min):** Con $x = e^{st}$:

$$
m s^2 + (c + k_i K_d)s + (k_i K_p - k_s) = 0
$$

«Las soluciones $s_1$, $s_2$ son los polos. Si $\mathrm{Re}(s) > 0$, inestable.»

**Diapo 5 (2 min):** $\Delta > 0$ → $x(t) = C_1 e^{s_1 t} + C_2 e^{s_2 t}$. Monótono, sin vibrar.

**Ejercicio:** métricas → $\Delta$, Re($s_1$). Tablero: copiar $s_1$, $s_2$.

**Interpretación:** plano $s$ a la izquierda; 3D dentro del anillo rojo.
""",
    },
    {
        "id": "alexis",
        "speaker": "ALEXIS — guion completo",
        "duration": "~5,5 min",
        "slide": "Diapositiva 6",
        "sim": "Bloque: **Caso II — Raíces reales iguales**.",
        "text": CHEAT_ALEXIS + ALEXIS_TABLERO,
    },
    {
        "id": "arbey",
        "speaker": "ARBEY — guion completo",
        "duration": "~5,5 min",
        "slide": "Diapositivas 7, 8, 9",
        "sim": "Bloque: **Caso III**, luego **AMB** (30 s: mover $\alpha$ del lazo digital).",
        "text": CHEAT_ARBEY
        + r"""

---

#### Guion palabra por palabra

**Diapo 7:** $\Delta < 0$ → $s = \alpha \pm \beta i$

$$
x(t) = e^{\alpha t}[C_1\cos(\beta t) + C_2\sin(\beta t)]
$$

«$\alpha$ controla si la vibración crece o decrece; $\beta$ la frecuencia.»

**Diapo 8:** «Semiplano izquierdo = seguro; derecho = colisión.» Mostrar figura plano $s$.

**Diapo 9 (breve):** «$K_p$ y $K_d$ mueven los polos. El lazo digital puede diferir del modelo continuo.»

**Interpretación:** con $\alpha < 0$ espiral que entra al centro; con $\alpha > 0$ respuesta inestable.
""",
    },
    {
        "id": "eduardo",
        "speaker": "EDUARDO — guion completo",
        "duration": "~5,5 min",
        "slide": "Diapositivas 10 a 14",
        "sim": "**Caso A** luego **Caso B**. Paso 6. Mover **Instante t** en 3D.",
        "text": CHEAT_EDUARDO
        + r"""

---

#### Guion palabra por palabra

**Diapo 10:** $m = 1$ kg, $k_s = 20$ N/m inestable, $k_i = 1$. Dos controles.

**Caso A — leer Paso 6:**
1. $\dfrac{d^2x}{dt^2} - 5x = 0$
2. $s^2 - 5 = 0$ → $s = \pm\sqrt{5}$
3. $x(t) = C_1 e^{2.23t} + C_2 e^{-2.23t}$

«La raíz positiva diverge. Miren: banner Inestable; el eje sale del anillo.»

**Caso B — leer Paso 6:**
1. $\dfrac{d^2x}{dt^2} + 6\dfrac{dx}{dt} + 10x = 0$
2. $s = -3 \pm i$
3. $x(t) = e^{-3t}[C_1\cos t + C_2\sin t]$

«Es Caso III pero $\alpha = -3 < 0$. Espiral estable; % holgura bajo.»

**Diapo 14:** «Todo se reduce a mantener $\mathrm{Re}(s) < 0$. Gracias.»
""",
    },
]

TIMING_TOTAL = (
    "Total: unos **22-24 min** de exposición + **1-2 min** de preguntas (meta del profesor: 20-25 min)."
)

CHECKLIST_REQUISITOS = r"""
| Requisito | Cómo lo cumplimos |
|-----------|-------------------|
| Todos participan ~5 min | Karol, Alexis, Arbey, Eduardo + apertura grupal |
| Teoría + práctica | Diapositiva + app en cada bloque |
| Paso a paso | Panel «Desarrollo paso a paso» + ejercicios en tablero |
| Interpretar resultados | Sección «Interpretación» en cada cheat sheet |
| 20-25 min | Ver tiempos arriba |
"""

CRITERIOS_EVALUACION = r"""
1. **Conceptos** — Los 5 puntos de «Si solo recuerdan 5 cosas»
2. **Claridad** — Tablas «Qué decir» por persona
3. **Participación** — Una pestaña por integrante
4. **Ejercicios** — Pasos de la app + tablero
5. **Fórmulas** — Usar panel Paso a paso (ya renderiza LaTeX bien)
6. **Práctica** — 3D, % holgura, Estable/Inestable
7. **Organización** — Orden I → II → III → Turbina
8. **Preguntas** — Pestaña «Preguntas»
"""

QUICK_REFERENCE = (
    CONCEPTOS_TODOS
    + "\n\n"
    + CHECKLIST_REQUISITOS
    + "\n\n**App:** http://localhost:8501/ · **Guion (interno):** http://localhost:8501/guion\n"
)
