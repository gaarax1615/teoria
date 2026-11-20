"""
Proyecto final — Teoría de la Computación
Calculadora de ecuaciones con AFD (léxico) y GLC (sintaxis).

Partió de compilador_proyecto.py. Cambios principales:
  - Entrada por cadena de texto (además de archivo).
  - Funciones: sqrt, cos (base) + abs, exp, ln (agregadas).
  - Asociatividad izquierda en + - * /; derecha en ^.
  - Mensajes de error en español con posición.

"""

from __future__ import annotations

import io
import math
import sys
from typing import Any


class ErrorExpr(Exception):
    """Error léxico, sintáctico o de evaluación."""


# ---------------------------------------------------------------------------
# AFD — analizador léxico (tabla de transiciones, estilo de la base)
# ---------------------------------------------------------------------------
# Columnas: espacio, dígito, letra, ., +, -, *, /, ^, (, ), salto, EOF, otro
# Estados de aceptación: 4=num, 5=+, 6=-, 7=*, 8=/, 9=^, 10=(, 11=), 13=nombre
_MATRIZ = [
    #   sp  dig  let   .   +   -   *   /   ^   (   )  nl EOF otro
    [0, 1, 12, 2, 5, 6, 7, 8, 9, 10, 11, 0, 15, 16],  # 0
    [4, 1, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],  # 1 entero
    [16, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],  # 2 punto
    [4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],  # 3 decimal
    [16] * 14,  # 4  NUM
    [16] * 14,  # 5  SUM
    [16] * 14,  # 6  RES
    [16] * 14,  # 7  MUL
    [16] * 14,  # 8  DIV
    [16] * 14,  # 9  POT
    [16] * 14,  # 10 PI
    [16] * 14,  # 11 PD
    [13, 13, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],  # 12 letras
    [16] * 14,  # 13 ID
    [16] * 14,  # 14 (reservado)
    [16] * 14,  # 15 EOF
    [16] * 14,  # 16 error
]


def _columna(c: str) -> int:
    if c == "":
        return 12
    if c == "\n":
        return 11
    if c.isspace():
        return 0
    if c.isdigit():
        return 1
    if c.isalpha():
        return 2
    tabla = {".": 3, "+": 4, "-": 5, "*": 6, "/": 7, "^": 8, "(": 9, ")": 10}
    return tabla.get(c, 13)


class Lexer:
    """AFD sobre un flujo de texto (archivo o StringIO)."""

    def __init__(self, fuente: Any):
        self.fuente = fuente

    def next_token(self) -> dict:
        q = 0
        lexema = ""
        inicio = self.fuente.tell()
        while True:
            pos = self.fuente.tell()
            c = self.fuente.read(1)
            col = _columna(c)
            q = _MATRIZ[q][col]
            lexema += c

            if q == 0:
                # espacios descartados; reinicia lexema
                lexema = ""
                inicio = self.fuente.tell()
                continue
            if q == 4:
                self.fuente.seek(pos)
                texto = lexema[:-1] if c else lexema
                return {
                    "type": "num",
                    "lexema": texto,
                    "position": inicio,
                    "value": float(texto),
                }
            if q == 5:
                return {"type": "sum", "lexema": lexema, "position": inicio, "value": 0}
            if q == 6:
                return {"type": "res", "lexema": lexema, "position": inicio, "value": 0}
            if q == 7:
                return {"type": "mul", "lexema": lexema, "position": inicio, "value": 0}
            if q == 8:
                return {"type": "div", "lexema": lexema, "position": inicio, "value": 0}
            if q == 9:
                return {"type": "pot", "lexema": lexema, "position": inicio, "value": 0}
            if q == 10:
                return {"type": "p_i", "lexema": lexema, "position": inicio, "value": 0}
            if q == 11:
                return {"type": "p_d", "lexema": lexema, "position": inicio, "value": 0}
            if q == 13:
                self.fuente.seek(pos)
                texto = lexema[:-1] if c else lexema
                return {
                    "type": "nombre",
                    "lexema": texto,
                    "position": inicio,
                    "value": 0,
                }
            if q == 15:
                return {"type": "endf", "lexema": "", "position": pos, "value": 0}
            if q == 16:
                mal = lexema.rstrip("\0") or c or "?"
                raise ErrorExpr(
                    f"Carácter o número no válido cerca de '{mal}' (pos. {inicio + 1})"
                )



# ---------------------------------------------------------------------------
# Funciones matemáticas (3 nuevas + 2 de la base)
# ---------------------------------------------------------------------------
def _sqrt(x: float) -> float:
    if x < 0:
        raise ErrorExpr("sqrt: no se admite raíz de un número negativo")
    return math.sqrt(x)


def _ln(x: float) -> float:
    if x <= 0:
        raise ErrorExpr("ln: el argumento debe ser mayor que cero")
    return math.log(x)


def _exp(x: float) -> float:
    try:
        return math.exp(x)
    except OverflowError as exc:
        raise ErrorExpr("exp: el resultado es demasiado grande") from exc


FUNCIONES = {
    "sqrt": _sqrt,  # base
    "cos": math.cos,  # base (radianes)
    "abs": abs,  # nueva
    "exp": _exp,  # nueva  e^x
    "ln": _ln,  # nueva  logaritmo natural
}


def _potencia(a: float, b: float) -> float:
    try:
        r = a**b
    except ZeroDivisionError as exc:
        raise ErrorExpr("0 no se puede elevar a un exponente negativo") from exc
    except OverflowError as exc:
        raise ErrorExpr("El resultado de la potencia es demasiado grande") from exc
    if isinstance(r, complex):
        raise ErrorExpr("La potencia no produce un número real")
    return float(r)


# ---------------------------------------------------------------------------
# GLC — descenso recursivo con asociatividad izquierda
#
#   E  -> T E'
#   E' -> + T E' | - T E' | ε
#   T  -> U T'
#   T' -> * U T' | / U T' | ε
#   U  -> - U | P
#   P  -> F P'
#   P' -> ^ U | ε
#   F  -> num | ( E ) | id ( E )
# ---------------------------------------------------------------------------
class Parser:
    def __init__(self, lexer: Lexer):
        self.lex = lexer
        self.tok = self.lex.next_token()
        self.tokens: list[dict] = []

    def _avance(self) -> dict:
        actual = self.tok
        if actual["type"] != "endf":
            self.tokens.append(actual)
        self.tok = self.lex.next_token()
        return actual

    def _mira(self, *tipos: str) -> bool:
        return self.tok["type"] in tipos

    def _exige(self, tipo: str, mensaje: str) -> dict:
        if self.tok["type"] != tipo:
            raise ErrorExpr(f"{mensaje} (pos. {self.tok['position'] + 1})")
        return self._avance()

    def parse(self) -> float:
        valor = self._E()
        if self.tok["type"] != "endf":
            raise ErrorExpr(
                f"Símbolo inesperado '{self.tok['lexema']}' "
                f"(pos. {self.tok['position'] + 1})"
            )
        return valor

    def _E(self) -> float:
        v = self._T()
        while self._mira("sum", "res"):
            op = self._avance()["type"]
            d = self._T()
            v = v + d if op == "sum" else v - d
        return v

    def _T(self) -> float:
        v = self._U()
        while self._mira("mul", "div"):
            op = self._avance()["type"]
            d = self._U()
            if op == "mul":
                v = v * d
            else:
                if d == 0:
                    raise ErrorExpr("División entre cero")
                v = v / d
        return v

    def _U(self) -> float:
        if self._mira("res"):
            self._avance()
            return -self._U()
        return self._P()

    def _P(self) -> float:
        base = self._F()
        if self._mira("pot"):
            self._avance()
            return _potencia(base, self._U())
        return base

    def _F(self) -> float:
        t = self.tok
        if t["type"] == "num":
            self._avance()
            return float(t["value"])
        if t["type"] == "p_i":
            self._avance()
            v = self._E()
            self._exige("p_d", "Se esperaba ')'")
            return v
        if t["type"] == "nombre":
            self._avance()
            nombre = t["lexema"].lower()
            if nombre not in FUNCIONES:
                raise ErrorExpr(f"Función '{t['lexema']}' no implementada")
            self._exige("p_i", f"Se esperaba '(' después de {t['lexema']}")
            arg = self._E()
            self._exige("p_d", "Se esperaba ')'")
            return float(FUNCIONES[nombre](arg))
        raise ErrorExpr(
            f"Se esperaba número, función o '(' "
            f"(pos. {t['position'] + 1}, encontró '{t['lexema'] or 'fin'}')"
        )


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def evaluar(texto: str) -> tuple[list[dict], float]:
    """Devuelve (tokens, valor). Lanza ErrorExpr si falla."""
    if texto is None or not str(texto).strip():
        raise ErrorExpr("La expresión está vacía")
    lexer = Lexer(io.StringIO(str(texto)))
    parser = Parser(lexer)
    valor = parser.parse()
    if not math.isfinite(valor):
        raise ErrorExpr("El resultado está fuera de rango")
    return parser.tokens, valor


def formato(valor: float) -> str:
    if abs(valor - round(valor)) < 1e-12 and abs(valor) < 1e15:
        return str(int(round(valor)))
    return f"{valor:.10g}"


def main() -> None:
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        try:
            # si existe como archivo, se lee; si no, se trata como expresión
            try:
                with open(arg, "r", encoding="utf-8") as f:
                    expr = f.read()
            except OSError:
                expr = arg
            tokens, valor = evaluar(expr)
        except ErrorExpr as e:
            print("ERROR:", e, file=sys.stderr)
            sys.exit(1)
        else:
            print("Tokens:", " ".join(f"{t['type']}({t['lexema']})" for t in tokens))
            print("Resultado:", formato(valor))
            print("OK")
            return

    if len(sys.argv) > 2:
        expr = " ".join(sys.argv[1:])
        try:
            tokens, valor = evaluar(expr)
        except ErrorExpr as e:
            print("ERROR:", e, file=sys.stderr)
            sys.exit(1)
        print("Tokens:", " ".join(f"{t['type']}({t['lexema']})" for t in tokens))
        print("Resultado:", formato(valor))
        print("OK")
        return

    print("Calculadora AFD+GLC. Línea vacía para salir.")
    while True:
        try:
            linea = input("> ")
        except EOFError:
            break
        if not linea.strip():
            break
        try:
            tokens, valor = evaluar(linea)
        except ErrorExpr as e:
            print("ERROR:", e, file=sys.stderr)
        else:
            print("Tokens:", " ".join(f"{t['type']}({t['lexema']})" for t in tokens))
            print("Resultado:", formato(valor))
            print("OK")


if __name__ == "__main__":
    main()
