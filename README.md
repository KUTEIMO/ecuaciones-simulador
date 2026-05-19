# Simulador — Ecuaciones diferenciales (AMB / turbinas)

Aplicación Streamlit de **estabilidad dinámica** para cojinetes magnéticos activos (AMB) en turbinas de alta velocidad. Incluye casos de exposición, pasos analíticos y visualización 3D.

## Requisitos

- Python 3.10 o superior
- Git

## Clonar y ejecutar (otro PC)

```bash
git clone https://github.com/KUTEIMO/ecuaciones-simulador.git
cd ecuaciones-simulador
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

**Linux / macOS:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

La app abre en el navegador (por defecto `http://localhost:8501`).

## Estructura principal

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Entrada Streamlit |
| `physics_core.py` | Modelo y respuesta analítica |
| `expo_cases.py` | Casos de exposición |
| `guion_expo.py` / `guion_latex.py` | Guion y LaTeX |
| `bearing_3d.py` | Visualización 3D |

## Repositorio

https://github.com/KUTEIMO/ecuaciones-simulador
