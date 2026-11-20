# Calculadora con AFD y GLC

Proyecto final de **Teoría de la Computación** (UACH, grupo 7CC2).  
Alumno: **Samuel Eduardo García Gómez — 367651**  
Docente: Mario Andrés Cuevas Gutiérrez

Evaluador de expresiones matemáticas:

1. Un **Autómata Finito Determinista (AFD)** hace el análisis léxico (tokens).
2. Una **Gramática Libre de Contexto (GLC)** con descenso recursivo valida y calcula.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `analizador.py` | AFD (tabla de transiciones), GLC y funciones |
| `calculadora_gui.py` | Interfaz gráfica (Tkinter) |
| `compilador_proyecto_base.py` | Archivo base del curso (referencia) |

## Requisitos

Python 3 con Tkinter (incluido en la instalación estándar). Sin dependencias externas.

## Uso

```bash
python calculadora_gui.py
python analizador.py "2+3*abs(-4)"
python analizador.py            # modo interactivo
```

## Funciones

| Función | Descripción |
| --- | --- |
| `sqrt(x)` | Raíz cuadrada (base) |
| `cos(x)` | Coseno en radianes (base) |
| `abs(x)` | Valor absoluto |
| `exp(x)` | Exponencial e^x |
| `ln(x)` | Logaritmo natural |

Ejemplos: `abs(-5)+sqrt(9)` → 8, `ln(exp(2))` → 2, `10-3-2` → 5.
