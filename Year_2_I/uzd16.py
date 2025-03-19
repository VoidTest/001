import tkinter as tk
from tkinter import ttk

# Function to update the entry field
def update_entry(text):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + text)

# Function to evaluate the expression
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Function to clear the entry field
def clear():
    entry.delete(0, tk.END)

# Initialize the root window
root = tk.Tk()
root.title("Calculator")

# Create a main frame to hold widgets
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

# Entry widget for displaying input and result
entry = ttk.Entry(main_frame, width=20, font=('Arial', 18), justify='right')
entry.grid(row=0, column=0, columnspan=4, pady=10)

# Button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

# Add buttons to the grid
for (text, row, col) in buttons:
    if text == '=':
        btn = ttk.Button(main_frame, text=text, command=calculate)
    else:
        btn = ttk.Button(main_frame, text=text, command=lambda t=text: update_entry(t))
    btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)

# Clear button
ttk.Button(main_frame, text='C', command=clear).grid(row=5, column=0, columnspan=4, padx=5, pady=5, ipadx=115, ipady=10)

# Make the GUI responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Run the main loop
root.mainloop()
