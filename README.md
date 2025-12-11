<div align="center">

# 🤖 G-Form AutoFiller 3000
### La herramienta definitiva de automatización para Google Forms

![Python](https://img.shields.io/badge/Python-3.x-FEC426?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Automation](https://img.shields.io/badge/Status-Autónomo-0052cc?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br>

**¿Cansado de llenar encuestas manualmente?**  
*Deja que el robot trabaje por ti.*

[Características](#-características-destacadas) • [Instalación](#-instalación-rápida) • [Uso](#-instrucciones-de-uso) • [Cómo Funciona](#-arquitectura-y-lógica)

</div>

---

> [!IMPORTANT]
> **Aviso de Responsabilidad**: Esta herramienta simula comportamiento humano avanzado. Úsala éticamente para pruebas de carga o gestión de formularios propios.

---

## 💎 Características Destacadas

| Función | Descripción | Nivel de Automatización |
| :--- | :--- | :---: |
| **🧠 Cerebro Aleatorio** | Selecciona respuestas de forma inteligente, no solo "al azar". | ⭐⭐⭐⭐⭐ |
| **🕵️‍♂️ Detección Dinámica** | Identifica Radio Buttons y Checkboxes sin importar la estructura del HTML. | ⭐⭐⭐⭐⭐ |
| **🎭 Máscara Humana** | Esperas aleatorias (15-30s) entre envíos para evitar baneos de IP. | ⭐⭐⭐⭐ |
| **🚀 Multi-Sección** | Navega automáticamente por formularios de 1 a N páginas. | ⭐⭐⭐⭐⭐ |

<br>

## ⚡ Instalación Rápida

<details>
<summary><strong>👇 Haz clic para desplegar los requisitos</strong></summary>

1.  **Python 3.10+**: Asegúrate de tener Python instalado.
2.  **Google Chrome**: El navegador más rápido para nuestras pruebas.
3.  **Librerías**: Solo necesitas una.

</details>

Corre este comando en tu terminal para instalar el motor del auto:

```bash
pip install selenium
```

---

## 🎮 Instrucciones de Uso

### Paso 1: Configuración 🛠️

Edita el archivo `llenador_aleatorio.py` e inserta tu objetivo:

```python
# Busca esta línea al inicio del archivo
URL = "https://forms.gle/TU_ENLACE_AQUI"
```

### Paso 2: Ejecución 🚀

```bash
python llenador_aleatorio.py
```

### Paso 3: Define tu estrategia 🔢

El sistema te preguntará:
> `¿Cuántas veces deseas completar el formulario?`

Ingresa la cifra deseada y observa la magia.

> [!TIP]
> Para pruebas rápidas usa **2 o 3 repeticiones**. Para pruebas de carga serias, puedes dejarlo corriendo toda la noche.

---

## 🧠 Arquitectura y Lógica

El script utiliza un algoritmo de decisión para interactuar con los elementos del DOM de Google Forms.

```mermaid
graph TD
    A[Inicio] --> B{¿Botones en Pantalla?}
    B -->|Radio| C[Seleccionar 1 Opción]
    B -->|Checkbox| D[Seleccionar Subconjunto (1 a N-1)]
    B -->|Siguiente| E[Clic 'Siguiente']
    E --> B
    B -->|Enviar| F[Clic 'Enviar']
    F --> G[Espera Aleatoria 15-30s]
    G --> H{¿Más iteraciones?}
    H -->|Sí| A
    H -->|No| I[Fin del Proceso]
```

### Lógica de Selección
*   **Radio Buttons 🔘**: `random.choice(opciones)` -> Elige 1.
*   **Checkboxes ☑️**: `random.sample(opciones, k)` donde `k` es un número entre 1 y el total menos uno. *Nunca deja la pregunta vacía ni marca todo mecánicamente.*

---

<div align="center">

By **Antigravity** 🚀  
*Simulando humanidad, un click a la vez.*

</div>
