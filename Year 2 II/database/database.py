import tkinter as tk
from tkinter import ttk, END
from tkinter.messagebox import showerror
import sqlite3

conn = sqlite3.connect("Year 2 II/database/files/my.db")

def kverijs(text):
    cur = conn.cursor()
    cur.execute(text)
    conn.commit()


tabulas_dzesana = "DROP TABLE skoleni"

tabulas_izveide = """
CREATE TABLE IF NOT EXISTS skoleni(
    id_skolenam INTEGER PRIMARY KEY AUTOINCREMENT,
    vards TEXT
    uzvards TEXT
    vecums INTEGER
)

"""

datu_pievienosana = """
INSERT INTO skoleni (vards, uzvards, vecums)
VALUES('Anna', 'Bērziņa', '18')
"""

kverijs(datu_pievienosana)

def datu_pieliksana(tabula, kolonnas, dati):
    vaicajums = """
INSERT INTO {tabula} ({kolonnas})
VALUES({dati})
"""
    kverijs(vaicajums)

datu_pieliksana("skoleni",("vards","uzvards","vecums"), ("Jānis", "test", "12"))









# # root window
# root = tk.Tk()
# root.title('Human Generator')
# root.geometry('500x400')  # Increased height to accommodate the listbox at the bottom
# root.resizable(False, False)

# # frame for inputs
# frame = ttk.Frame(root)

# # field options
# options = {'padx': 5, 'pady': 5}

# frame.grid(padx= 5, pady= 5)

# # Start the app
# root.mainloop()
