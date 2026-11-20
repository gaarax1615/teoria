"""
Interfaz gráfica de la calculadora (Tkinter).
Ejecutar:  python calculadora_gui.py
"""

import tkinter as tk
from tkinter import ttk

from analizador import ErrorExpr, evaluar, formato

# Botones distintos a la calculadora del compañero (otras funciones y orden)
FILAS = [
    ["abs(", "exp(", "ln(", "sqrt(", "cos("],
    ["(", ")", "^", "CE", "⌫"],
    ["7", "8", "9", "/", "*"],
    ["4", "5", "6", "-", "+"],
    ["1", "2", "3", "0", "."],
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Evaluador AFD + GLC — Samuel García")
        self.configure(bg="#1e293b")
        self.resizable(False, False)

        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        marco = tk.Frame(self, bg="#1e293b", padx=12, pady=12)
        marco.pack(fill="both", expand=True)

        tk.Label(
            marco,
            text="Expresión",
            fg="#94a3b8",
            bg="#1e293b",
            font=("Menlo", 10),
            anchor="w",
        ).pack(fill="x")

        self.entrada = tk.Entry(
            marco,
            font=("Menlo", 18),
            justify="right",
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#334155",
            highlightcolor="#38bdf8",
        )
        self.entrada.pack(fill="x", ipady=10, pady=(2, 8))
        self.entrada.bind("<Return>", lambda _e: self.calcular())
        self.entrada.focus_set()

        self.lbl_resultado = tk.Label(
            marco,
            text="—",
            font=("Menlo", 22, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            anchor="e",
        )
        self.lbl_resultado.pack(fill="x", pady=(0, 4))

        self.lbl_detalle = tk.Label(
            marco,
            text="Tokens del AFD aparecerán aquí",
            font=("Menlo", 9),
            fg="#64748b",
            bg="#1e293b",
            anchor="w",
            justify="left",
            wraplength=380,
        )
        self.lbl_detalle.pack(fill="x", pady=(0, 10))

        teclado = tk.Frame(marco, bg="#1e293b")
        teclado.pack()

        for r, fila in enumerate(FILAS):
            for c, texto in enumerate(fila):
                bg = "#334155"
                fg = "#f8fafc"
                if texto in ("CE", "⌫"):
                    bg = "#7f1d1d"
                elif texto.endswith("(") or texto in ("(", ")", "^"):
                    bg = "#0e7490"
                btn = tk.Button(
                    teclado,
                    text=texto,
                    width=6,
                    height=2,
                    font=("Menlo", 11),
                    bg=bg,
                    fg=fg,
                    activebackground="#475569",
                    activeforeground="#f8fafc",
                    relief="flat",
                    command=lambda t=texto: self.pulsar(t),
                )
                btn.grid(row=r, column=c, padx=3, pady=3)

        tk.Button(
            marco,
            text="Evaluar  =",
            font=("Menlo", 13, "bold"),
            bg="#0369a1",
            fg="#f8fafc",
            activebackground="#0284c7",
            relief="flat",
            height=2,
            command=self.calcular,
        ).pack(fill="x", pady=(10, 0))

    def pulsar(self, texto: str) -> None:
        if texto == "CE":
            self.entrada.delete(0, tk.END)
            self.lbl_resultado.config(text="—", fg="#38bdf8")
            self.lbl_detalle.config(text="Tokens del AFD aparecerán aquí", fg="#64748b")
        elif texto == "⌫":
            actual = self.entrada.get()
            if actual:
                self.entrada.delete(len(actual) - 1, tk.END)
        else:
            self.entrada.insert(tk.END, texto)
        self.entrada.focus_set()

    def calcular(self) -> None:
        try:
            tokens, valor = evaluar(self.entrada.get())
        except ErrorExpr as err:
            self.lbl_resultado.config(text="Error", fg="#f87171")
            self.lbl_detalle.config(text=str(err), fg="#fca5a5")
            return
        self.lbl_resultado.config(text=formato(valor), fg="#4ade80")
        lista = " ".join(f"{t['type']}({t['lexema']})" for t in tokens)
        self.lbl_detalle.config(text="AFD → " + lista, fg="#94a3b8")


if __name__ == "__main__":
    App().mainloop()
