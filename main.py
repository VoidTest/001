from test1 import Human , Sieviete
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


all_humans = []

# root window
root = tk.Tk()
root.title('Human Generator')
root.geometry('300x300')
root.resizable(False, False)


def fahrenheit_to_celsius(f):
    """ Convert fahrenheit to celsius
    """
    return (f - 32) * 5/9


# frame
frame = ttk.Frame(root)

# field options
options = {'padx': 5, 'pady': 5}

# temperature label
texts_label = ttk.Label(frame, text='Name')
texts_label.grid(column=0, row=0, sticky='W', **options)

gender_label = ttk.Label(frame, text='Gender')
gender_label.grid(column=0, row=1, sticky='W', **options)

age_label = ttk.Label(frame, text='Age')
age_label.grid(column=0, row=2, sticky='W', **options)

# temperature entry
texts = tk.StringVar()
texts_entry = ttk.Entry(frame, textvariable=texts)
texts_entry.grid(column=1, row=0, **options)
texts_entry.focus()

gender = tk.StringVar()
gender_entry = ttk.Entry(frame, textvariable=gender)
gender_entry.grid(column=1, row=1, **options)

age = tk.IntVar()
age_entry = ttk.Entry(frame, textvariable=age)
age_entry.grid(column=1, row=2, **options)
# convert button


def create_button_clicked():
    human_name = texts.get()
    human_gender = gender.get()
    human_age = age.get()
    all_humans.append(Human(human_name,human_age,human_gender))
    result_label.config(text=all_humans[-1].info())


convert_button = ttk.Button(frame, text='Create HUMAN')
convert_button.grid(column=2, row=0, sticky='W', **options)
convert_button.configure(command=create_button_clicked)

# result label
result_label = ttk.Label(frame)
result_label.grid(row=3, columnspan=3, **options)

# add padding to the frame and show it
frame.grid(padx=10, pady=10)


# start the app
root.mainloop()