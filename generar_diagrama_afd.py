"""Genera la figura del AFD para el reporte."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).with_name("figuras")
OUT.mkdir(exist_ok=True)


def dibujar():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title("AFD del analizador léxico", fontsize=13, pad=12)

    # posiciones (nombre_estado, x, y, aceptacion?)
    nodos = {
        "q0": (1.2, 2.8, False),
        "q1": (3.2, 4.2, True),
        "q2": (5.2, 4.2, False),
        "q3": (7.2, 4.2, True),
        "q4": (3.2, 1.4, True),
        "q5+": (5.0, 2.8, True),
        "q6-": (5.8, 2.8, True),
        "q7*": (6.6, 2.8, True),
        "q8/": (7.4, 2.8, True),
        "q9^": (8.2, 2.8, True),
        "q10(": (5.0, 1.0, True),
        "q11)": (6.2, 1.0, True),
    }

    for nombre, (x, y, acc) in nodos.items():
        c = Circle((x, y), 0.38, fill=True, facecolor="#e8f4fc", edgecolor="#1e3a5f", lw=1.5)
        ax.add_patch(c)
        if acc:
            c2 = Circle((x, y), 0.48, fill=False, edgecolor="#1e3a5f", lw=1.2)
            ax.add_patch(c2)
        etiqueta = nombre.replace("q5+", "q5\n+").replace("q6-", "q6\n-")
        etiqueta = etiqueta.replace("q7*", "q7\n*").replace("q8/", "q8\n/")
        etiqueta = etiqueta.replace("q9^", "q9\n^").replace("q10(", "q10\n(")
        etiqueta = etiqueta.replace("q11)", "q11\n)")
        ax.text(x, y, etiqueta if "\n" in etiqueta else nombre, ha="center", va="center", fontsize=8)

    def flecha(a, b, texto, rad=0.0, color="#334155"):
        x1, y1, _ = nodos[a]
        x2, y2, _ = nodos[b]
        patch = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>",
            mutation_scale=12,
            color=color,
            lw=1.1,
            shrinkA=18,
            shrinkB=18,
        )
        ax.add_patch(patch)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + rad * 0.8
        ax.text(mx, my, texto, fontsize=7, color="#0f172a", ha="center")

    # flecha inicial
    ax.annotate("", xy=(0.82, 2.8), xytext=(0.2, 2.8), arrowprops=dict(arrowstyle="-|>", color="#1e3a5f"))

    flecha("q0", "q1", "D", 0.05)
    flecha("q1", "q1", "D", 0.6)
    flecha("q0", "q2", ".", -0.15)
    flecha("q1", "q2", ".", 0.0)
    flecha("q2", "q3", "D", 0.0)
    flecha("q3", "q3", "D", 0.55)
    flecha("q0", "q4", "L", -0.2)
    flecha("q4", "q4", "L", -0.55)
    flecha("q0", "q5+", "+", 0.25)
    flecha("q0", "q6-", "-", 0.1)
    flecha("q0", "q7*", "*", -0.05)
    flecha("q0", "q8/", "/", -0.2)
    flecha("q0", "q9^", "^", -0.35)
    flecha("q0", "q10(", "(", -0.15)
    flecha("q0", "q11)", ")", -0.25)

    # leyenda
    box = FancyBboxPatch((0.3, 0.15), 4.2, 0.55, boxstyle="round,pad=0.05", facecolor="#f1f5f9", edgecolor="#94a3b8")
    ax.add_patch(box)
    ax.text(0.45, 0.42, "D=dígito  L=letra  · doble círculo = aceptación  · B (blanco) en q0 se descarta", fontsize=7.5, va="center")

    ruta = OUT / "afd.png"
    fig.tight_layout()
    fig.savefig(ruta, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("escrito", ruta)


if __name__ == "__main__":
    dibujar()
