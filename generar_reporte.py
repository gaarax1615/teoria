"""
Genera el PDF del proyecto final (reporte propio de Samuel García Gómez).
Ejecutar:  .venv/bin/python generar_reporte.py
"""

from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figuras"
OUT = ROOT / "Proyecto_final_Samuel_Garcia_AFD_GLC.pdf"


def estilos():
    base = getSampleStyleSheet()
    styles = {
        "titulo": ParagraphStyle(
            "titulo",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            spaceBefore=14,
            spaceAfter=8,
            textColor=colors.HexColor("#0f172a"),
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#1e293b"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "center": ParagraphStyle(
            "center",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=9.5,
            leftIndent=0,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475569"),
            spaceAfter=10,
        ),
    }
    return styles


def tabla(datos, col_widths=None):
    t = Table(datos, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def capturar_consola(expr: str) -> str:
    r = subprocess.run(
        [sys.executable, str(ROOT / "analizador.py"), expr],
        capture_output=True,
        text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    return f"$ python analizador.py \"{expr}\"\n{out.strip()}"


def leer_fuente(nombre: str, max_chars: int = 12000) -> str:
    texto = (ROOT / nombre).read_text(encoding="utf-8")
    if len(texto) > max_chars:
        return texto[:max_chars] + "\n# ... (continúa en el repositorio) ..."
    return texto


def construir():
    S = estilos()
    story = []

    # ---- Portada ----
    story.append(Spacer(1, 2.2 * cm))
    story.append(Paragraph("UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA", S["center"]))
    story.append(Paragraph("FACULTAD DE INGENIERÍA", S["center"]))
    story.append(Paragraph("Ingeniería en Ciencias de la Computación", S["center"]))
    story.append(Spacer(1, 1.2 * cm))
    story.append(Paragraph("TEORÍA DE LA COMPUTACIÓN", S["center"]))
    story.append(Paragraph("GRUPO: 7CC2", S["center"]))
    story.append(Spacer(1, 1.4 * cm))
    story.append(Paragraph("Proyecto final", S["titulo"]))
    story.append(
        Paragraph(
            "Calculadora de ecuaciones matemáticas<br/>con Autómata Finito Determinista (AFD)<br/>"
            "y Gramática Libre de Contexto (GLC)",
            S["center"],
        )
    )
    story.append(Spacer(1, 1.8 * cm))
    story.append(Paragraph("<b>DOCENTE:</b> Mario Andrés Cuevas Gutiérrez", S["center"]))
    story.append(Paragraph("<b>ALUMNO:</b> Samuel Eduardo García Gómez — 367651", S["center"]))
    story.append(Spacer(1, 1.0 * cm))
    story.append(
        Paragraph(
            "Repositorio: https://github.com/samuelgarciagomez/calculadora-afd-glc",
            S["center"],
        )
    )
    story.append(Paragraph("Noviembre 2026", S["center"]))
    story.append(PageBreak())

    # ---- Descripción ----
    story.append(Paragraph("1. Descripción del proyecto", S["h1"]))
    story.append(
        Paragraph(
            "El objetivo es demostrar la aplicación de un Autómata Finito Determinista y de una "
            "Gramática Libre de Contexto en la interpretación de ecuaciones matemáticas. Se partió "
            "del archivo <font face='Courier'>compilador_proyecto.py</font> entregado como base y se "
            "realizaron las modificaciones pedidas: agregar funciones matemáticas e integrar una "
            "interfaz gráfica.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "La solución propia está organizada en dos módulos. "
            "<font face='Courier'>analizador.py</font> conserva el enfoque de la base (AFD implementado "
            "con una matriz de transiciones) pero ahora lee cadenas de texto, corrige la asociatividad "
            "de operadores y expone una API limpia. "
            "<font face='Courier'>calculadora_gui.py</font> ofrece una ventana Tkinter con teclado, "
            "resultado y la lista de tokens reconocidos por el AFD.",
            S["body"],
        )
    )
    story.append(Paragraph("Cambios respecto a la base:", S["body"]))
    story.append(
        Paragraph(
            "• <b>Funciones.</b> La base traía <font face='Courier'>sqrt</font> y "
            "<font face='Courier'>cos</font>. Se agregaron <font face='Courier'>abs</font>, "
            "<font face='Courier'>exp</font> y <font face='Courier'>ln</font> (logaritmo natural), "
            "para un total de cinco. Se escriben siempre con paréntesis, por ejemplo "
            "<font face='Courier'>abs(-3)+ln(exp(1))</font>.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Interfaz gráfica.</b> Ventana oscura hecha con Tkinter: campo de expresión, botones "
            "de dígitos/operadores/funciones, resultado y tokens del AFD.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Asociatividad.</b> En la base, <font face='Courier'>10-3-2</font> daba 9 porque la "
            "recursión era por la derecha. Ahora suma, resta, multiplicación y división asocian por la "
            "izquierda; la potencia, por la derecha.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Errores.</b> Mensajes en español con la posición del problema (división entre cero, "
            "función desconocida, paréntesis sin cerrar, etc.).",
            S["body"],
        )
    )

    # ---- Autómata ----
    story.append(Paragraph("2. El autómata utilizado", S["h1"]))
    story.append(
        Paragraph(
            "El analizador léxico es un AFD que recorre el texto de izquierda a derecha y entrega un "
            "token al llegar a un estado de aceptación, tomando el lexema más largo posible. La "
            "implementación usa la misma idea de la base: una matriz de transiciones indexada por "
            "estado y clase de carácter.",
            S["body"],
        )
    )

    afd_img = FIG / "afd.png"
    if afd_img.exists():
        story.append(Image(str(afd_img), width=16 * cm, height=8.3 * cm))
        story.append(Paragraph("Figura 1. Diagrama del AFD del analizador léxico.", S["caption"]))

    story.append(
        Paragraph(
            "Definición formal. <b>M = (Q, Σ, δ, q0, F)</b>, donde Q = {q0,…,q11}, q0 es el estado "
            "inicial y F = {q1, q3, q4, q5, q6, q7, q8, q9, q10, q11}. El alfabeto se agrupa en clases: "
            "D (dígitos), L (letras), B (blancos), los símbolos . + - * / ^ ( ) y O (otro, rechazo).",
            S["body"],
        )
    )

    story.append(
        tabla(
            [
                ["Estado de aceptación", "Reconoce", "Token"],
                ["q1", "entero (12)", "num"],
                ["q3", "decimal (3.14)", "num"],
                ["q4", "nombre (abs, ln…)", "nombre"],
                ["q5 … q9", "+ - * / ^", "sum/res/mul/div/pot"],
                ["q10, q11", "(  )", "p_i / p_d"],
            ],
            col_widths=[4.2 * cm, 5.5 * cm, 5.5 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        Paragraph(
            "q2 no es de aceptación: un número como <font face='Courier'>3.</font> se rechaza. Los "
            "espacios se descartan en q0. Al terminar el texto se emite el token de fin de archivo.",
            S["body"],
        )
    )

    # ---- Gramática ----
    story.append(Paragraph("3. La gramática utilizada", S["h1"]))
    story.append(
        Paragraph(
            "La gramática es libre de contexto y LL(1): con un token de anticipación basta para elegir "
            "la producción. Se implementa como analizador descendente recursivo (un método por no terminal).",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "G = (N, T, P, E) con N = {E, E', T, T', U, P, F}, terminales = tokens del AFD, y producciones:",
            S["body"],
        )
    )
    gram = (
        "E  → T E'\n"
        "E' → + T E' | - T E' | ε\n"
        "T  → U T'\n"
        "T' → * U T' | / U T' | ε\n"
        "U  → - U | P\n"
        "P  → F ( ^ U )?\n"
        "F  → num | ( E ) | id ( E )"
    )
    story.append(Preformatted(gram, S["code"]))
    story.append(
        Paragraph(
            "La precedencia sale de la estructura: E es lo más débil (+/−), luego T (×/÷), U (menos unario), "
            "P (potencia) y F (átomos). Los bucles de E y T hacen que + − × ÷ asocien por la izquierda "
            "(<font face='Courier'>10-3-2</font> = 5). La potencia asocia por la derecha "
            "(<font face='Courier'>2^3^2</font> = 512). Como el unario se aplica después de la potencia, "
            "<font face='Courier'>-2^2</font> da −4.",
            S["body"],
        )
    )

    # ---- Pruebas ----
    story.append(Paragraph("4. Pruebas de funcionamiento", S["h1"]))
    story.append(
        Paragraph(
            "Se ejecutaron casos con <font face='Courier'>analizador.py</font>. En todos el resultado "
            "coincidió con el esperado.",
            S["body"],
        )
    )
    story.append(Paragraph("4.1 Expresiones válidas", S["h2"]))
    story.append(
        tabla(
            [
                ["Expresión", "Qué comprueba", "Esperado"],
                ["2+3*4", "Prioridad", "14"],
                ["(2+3)*4", "Paréntesis", "20"],
                ["10-3-2", "Asoc. izquierda (−)", "5"],
                ["8/4/2", "Asoc. izquierda (/)", "1"],
                ["2^3^2", "Asoc. derecha (^)", "512"],
                ["-2^2", "Unario y potencia", "-4"],
                ["abs(-5)+sqrt(9)", "abs y sqrt", "8"],
                ["ln(exp(2))", "ln y exp", "2"],
                ["cos(0)", "cos (base)", "1"],
                ["sqrt(3^2+4^2)", "Función con expresión", "5"],
            ],
            col_widths=[5.2 * cm, 5.5 * cm, 3.5 * cm],
        )
    )
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph("4.2 Expresiones con error", S["h2"]))
    story.append(
        tabla(
            [
                ["Expresión", "Mensaje obtenido"],
                ["5/0", "División entre cero"],
                ["sqrt(-4)", "sqrt: no se admite raíz de un número negativo"],
                ["ln(0)", "ln: el argumento debe ser mayor que cero"],
                ["(2+3", "Se esperaba ')'"],
                ["abc(2)", "Función 'abc' no implementada"],
                ["2 $ 3", "Carácter o número no válido…"],
                ["3.", "Carácter o número no válido…"],
            ],
            col_widths=[4.5 * cm, 10.5 * cm],
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("4.3 Salida de consola (ejemplos)", S["h2"]))
    for expr in ["abs(-5)+sqrt(9)", "2^3^2", "5/0"]:
        story.append(Preformatted(capturar_consola(expr), S["code"]))
        story.append(Spacer(1, 0.15 * cm))

    story.append(
        Paragraph(
            "La interfaz gráfica (<font face='Courier'>python calculadora_gui.py</font>) muestra la misma "
            "evaluación: expresión, resultado en color y la secuencia de tokens del AFD debajo. Los botones "
            "incluyen las cinco funciones y operadores; CE limpia y ⌫ borra el último carácter.",
            S["body"],
        )
    )

    # ---- Código fuente ----
    story.append(PageBreak())
    story.append(Paragraph("5. Código fuente", S["h1"]))
    story.append(
        Paragraph(
            "El código completo está en el repositorio indicado en la portada. A continuación se incluye "
            "el contenido de los dos archivos principales.",
            S["body"],
        )
    )
    story.append(Paragraph("5.1 analizador.py", S["h2"]))
    story.append(Preformatted(leer_fuente("analizador.py", 14000), S["code"]))
    story.append(PageBreak())
    story.append(Paragraph("5.2 calculadora_gui.py", S["h2"]))
    story.append(Preformatted(leer_fuente("calculadora_gui.py", 8000), S["code"]))

    story.append(Spacer(1, 0.6 * cm))
    story.append(
        Paragraph(
            "Para ejecutar: <font face='Courier'>python calculadora_gui.py</font> o "
            "<font face='Courier'>python analizador.py \"expresión\"</font>.",
            S["body"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="Proyecto final AFD+GLC — Samuel Eduardo García Gómez",
        author="Samuel Eduardo García Gómez",
    )

    def pie(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(1.8 * cm, 1.0 * cm, "Proyecto final · Teoría de la Computación · 7CC2")
        canvas.drawRightString(letter[0] - 1.8 * cm, 1.0 * cm, f"Página {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=pie, onLaterPages=pie)
    print("PDF escrito en", OUT)


if __name__ == "__main__":
    construir()
