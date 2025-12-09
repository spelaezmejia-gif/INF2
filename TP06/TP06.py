import tkinter as tk
import math

class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text: str,
        command=None,
        width: int = 92,
        height: int = 60,
        radius: int = 14,
        bg: str = "#4E4E4E",
        hover_bg: str = "#5A5A5A",
        fg: str = "white",
        font=("Helvetica", 18, "bold"),
        shadow: bool = True,
        shadow_offset: int = 2,
        shadow_color: str = "#2A2A2A",
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0,
            bd=0,
        )
        self.command = command
        self.w = width
        self.h = height
        self.r = radius

        self.bg_normal = bg
        self.bg_hover = hover_bg
        self.fg = fg
        self.font = font

        self.shadow = shadow
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color

        self.text = text

        self._draw(self.bg_normal)

        self.create_text(
            self.w / 2,
            self.h / 2,
            text=self.text,
            fill=self.fg,
            font=self.font,
            tags="label",
        )

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _rounded_rect(self, x1, y1, x2, y2, r, *, fill, tag):
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90,  extent=90,  style="pieslice", fill=fill, outline="", tags=tag)
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0,   extent=90,  style="pieslice", fill=fill, outline="", tags=tag)
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90,  style="pieslice", fill=fill, outline="", tags=tag)
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90,  style="pieslice", fill=fill, outline="", tags=tag)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline="", tags=tag)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline="", tags=tag)

    def _draw(self, color):
        self.delete("shape")

        pad = 2
        x1, y1 = pad, pad
        x2, y2 = self.w - pad, self.h - pad

        if self.shadow:
            s = self.shadow_offset
            self._rounded_rect(
                x1 + s, y1 + s, x2 + s, y2 + s,
                self.r, fill=self.shadow_color, tag="shape"
            )

        self._rounded_rect(x1, y1, x2, y2, self.r, fill=color, tag="shape")
        self.tag_raise("label")

    def _on_click(self, _):
        if self.command:
            self.command()

    def _on_enter(self, _):
        self._draw(self.bg_hover)

    def _on_leave(self, _):
        self._draw(self.bg_normal)
        self.config(cursor="")

class Calculatrice(tk.Tk):
    def __init__(self):
        super().__init__()

        larg_fenetre = 660
        haut_fenetre = 660
        larg_ecran = self.winfo_screenwidth()
        haut_ecran = self.winfo_screenheight()
        pos_x = larg_ecran // 2 - larg_fenetre // 2
        pos_y = haut_ecran // 2 - haut_fenetre // 2
        self.geometry(f"{larg_fenetre}x{haut_fenetre}+{pos_x}+{pos_y}")
        self.title("Calculatrice")
        self.resizable(False, False)

        self.bg_color = "#2B2B2B"
        self.configure(bg=self.bg_color)

        for c in range(5):
            self.grid_columnconfigure(c, weight=1)
        for r in range(0, 8):
            self.grid_rowconfigure(r, weight=1)

        self._expr_display = ""
        self._expr_eval = ""
        self._ecran = tk.StringVar()
        self.historique = []

        self.entree = tk.Entry(
            self,
            textvariable=self._ecran,
            justify="right",
            font=("Helvetica", 20),
            bg="#1F1F1F",
            fg="white",
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#3A3A3A",
        )
        self.entree.grid(row=0, column=0, columnspan=4, padx=18, pady=(14, 8), sticky="ew")
        self.entree.focus_set()

        panel = tk.Frame(self, bg=self.bg_color, bd=0)
        panel.grid(row=0, column=4, rowspan=8, sticky="nsew", padx=(6, 12), pady=12)

        tk.Label(
            panel, text="Historique",
            bg=self.bg_color, fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(pady=(0, 8))

        self.liste_histo = tk.Listbox(
            panel,
            width=18,
            height=18,
            bg="#1F1F1F",
            fg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#3A3A3A",
            font=("Helvetica", 16),
        )
        self.liste_histo.pack(fill="both", expand=True)

        self._creer_boutons()

    def appui(self, valeur: str, valeur_eval: str = None) -> None:
        if valeur_eval is None:
            valeur_eval = valeur

        self._expr_display += str(valeur)
        self._expr_eval += str(valeur_eval)
        self._ecran.set(self._expr_display)
        self.entree.icursor(tk.END)

    def clear(self) -> None:
        self._expr_display = ""
        self._expr_eval = ""
        self._ecran.set("")
        self.entree.icursor(tk.END)

    def calculer(self) -> None:
        if not self._expr_eval:
            return

        ancienne_expr = self._expr_display
        expr_eval = self._expr_eval.replace(",", ".")

        env = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "pi": math.pi
        }

        try:
            resultat = eval(expr_eval, {"__builtins__": None}, env)
        except Exception:
            self._ecran.set("Erreur")
            self._expr_display = ""
            self._expr_eval = ""
        else:
            try:
                valeur_float = float(resultat)
            except Exception:
                texte_resultat = str(resultat).replace(".", ",")
            else:
                texte_resultat = str(int(valeur_float)) if valeur_float.is_integer() else str(valeur_float).replace(".", ",")

            self._ecran.set(texte_resultat)
            self._expr_display = texte_resultat
            self._expr_eval = texte_resultat.replace(",", ".")

            ligne = f"{ancienne_expr} = {texte_resultat}"
            self.historique.append(ligne)
            self.liste_histo.insert(tk.END, ligne)

        self.entree.icursor(tk.END)

    def _creer_boutons(self) -> None:
        BTN_W, BTN_H, R = 92, 60, 14
        PADX, PADY = 14, 12

        gray = dict(
            width=BTN_W,
            height=BTN_H,
            radius=R,
            bg="#4B4B4B",
            hover_bg="#5A5A5A",
            fg="white",
            font=("Helvetica", 18, "bold"),
            shadow=True,
            shadow_offset=2,
            shadow_color="#242424"
        )
        blue = dict(
            width=BTN_W,
            height=BTN_H,
            radius=R,
            bg="#6A86E8",
            hover_bg="#7C95EE",
            fg="white",
            font=("Helvetica", 18, "bold"),
            shadow=True,
            shadow_offset=2,
            shadow_color="#242424"
        )

        RoundedButton(self, "sin", command=lambda: self.appui("sin(", "sin("), **gray).grid(row=1, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, "cos", command=lambda: self.appui("cos(", "cos("), **gray).grid(row=1, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, "tan", command=lambda: self.appui("tan(", "tan("), **gray).grid(row=1, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "π",   command=lambda: self.appui("π", "pi"),       **gray).grid(row=1, column=3, padx=PADX, pady=PADY)

        RoundedButton(self, "7", command=lambda: self.appui("7"), **gray).grid(row=3, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, "8", command=lambda: self.appui("8"), **gray).grid(row=3, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, "9", command=lambda: self.appui("9"), **gray).grid(row=3, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "/", command=lambda: self.appui("/"), **blue).grid(row=3, column=3, padx=PADX, pady=PADY)

        RoundedButton(self, "4", command=lambda: self.appui("4"), **gray).grid(row=4, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, "5", command=lambda: self.appui("5"), **gray).grid(row=4, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, "6", command=lambda: self.appui("6"), **gray).grid(row=4, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "*", command=lambda: self.appui("*"), **blue).grid(row=4, column=3, padx=PADX, pady=PADY)

        RoundedButton(self, "1", command=lambda: self.appui("1"), **gray).grid(row=5, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, "2", command=lambda: self.appui("2"), **gray).grid(row=5, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, "3", command=lambda: self.appui("3"), **gray).grid(row=5, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "-", command=lambda: self.appui("-"), **blue).grid(row=5, column=3, padx=PADX, pady=PADY)

        RoundedButton(self, "C", command=self.clear, **gray).grid(row=6, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, "0", command=lambda: self.appui("0"), **gray).grid(row=6, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, ",", command=lambda: self.appui(",", "."), **gray).grid(row=6, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "+", command=lambda: self.appui("+"), **blue).grid(row=6, column=3, padx=PADX, pady=PADY)

        RoundedButton(self, "(",  command=lambda: self.appui("("), **gray).grid(row=2, column=0, padx=PADX, pady=PADY)
        RoundedButton(self, ")",  command=lambda: self.appui(")"), **gray).grid(row=2, column=1, padx=PADX, pady=PADY)
        RoundedButton(self, "√x", command=lambda: self.appui("√(", "sqrt("), **gray).grid(row=2, column=2, padx=PADX, pady=PADY)
        RoundedButton(self, "π²", command=lambda: self.appui("π²", "pi**2"), **gray).grid(row=2, column=3, padx=PADX, pady=PADY)

        RoundedButton(
            self,
            "=",
            command=self.calculer,
            width=4 * BTN_W + 3 * (2 * PADX),
            height=70,
            radius=16,
            bg="#6A86E8",
            hover_bg="#7C95EE",
            fg="white",
            font=("Helvetica", 22, "bold"),
            shadow=True,
            shadow_offset=2,
            shadow_color="#242424"
        ).grid(row=7, column=0, columnspan=4, padx=PADX, pady=(PADY, 16))

def main() -> None:
    calc = Calculatrice()
    calc.mainloop()

if __name__ == "__main__":
    main()
