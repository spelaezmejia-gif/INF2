import tkinter as tk
import numpy as np

class Calculatrice(tk.Tk):
    def __init__(self):
        super().__init__()
        longueur_locale= self.winfo_screenwidth()//2 -300
        hauteur_locale=self.winfo_screenheight()//2 - 400
        self.geometry(f"600x800+{longueur_locale}+{hauteur_locale}")
        self.title("TP Calculatrice")
        self.expr = ""

        i=5
        j=5
        self.un =tk.Button(text="1", command = lambda : appui(1)).grid(row=0+i,column=0+j, padx=20, pady=10)
        self.deux = tk.Button(text="2", command= lambda :appui(2) ).grid(row=0+i, column=1+j, padx=20, pady=10)
        self.trois = tk.Button(text="3", command= lambda :appui(3)).grid(row=0+i, column=2+j, padx=20, pady=10)
        self.quatre = tk.Button(text="4", command= lambda :appui(4)).grid(row=1+i, column=0+j, padx=20, pady=10)
        self.cinq = tk.Button(text="5", command= lambda :appui(5)).grid(row=1+j, column=1+j, padx=20, pady=10)
        self.six = tk.Button(text="6", command= lambda :appui(6)).grid(row=1+i, column=2+j, padx=20, pady=10)
        self.sept = tk.Button(text="7", command=lambda :appui(7)).grid(row=2+i, column=0+j, padx=20, pady=10)
        self.huit = tk.Button(text="8", command=lambda :appui(8)).grid(row=2+i, column=1+j, padx=20, pady=10)
        self.neuf = tk.Button(text="9", command= lambda :appui(9)).grid(row=2+i, column=2+j, padx=20, pady=10)
        self.zero = tk.Button(text="0", command= lambda :appui(0)).grid(row=3+i, column=1+j, padx=20, pady=10)
        self.clear= tk.Button(text="clear", command= lambda: clear()).grid(row=3 + i, column=2 + j, padx=20, pady=10)

        self.ecran = tk.StringVar().focus_set()
        #fonctions
        def appui(cle):
            self.expr+=str(cle)
            self.ecran.set(self.expr)

        def clear():
            self.expr=""
            self.ecran.set("")

        tk.Button(self, text="+", command=lambda: self.calculer("+"))
        tk.Button(self, text="-", command=lambda: self.calculer("-"))
        tk.Button(self, text="*", command=lambda: self.calculer("*"))
        tk.Button(self, text="/", command=lambda: self.calculer("/"))

    def calculer(self, operation: str):
        try:
            num1 = 10
            num2 = 5
        except:
            return

        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "/":
            if num2 == 0:
                print("Pas possible de diviser par 0")
            return None
        else:
            print("Pas ")
            return None


def main() :
    calculatrice = Calculatrice()
    calculatrice.mainloop()
if __name__ == "__main__":
    main()