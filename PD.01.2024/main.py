from item import Item
import tkinter as tk
from tkinter import ttk, END
from tkinter.messagebox import showerror

all_items = []

# root window
root = tk.Tk()
root.title('Veikala objektu uzskaititajs')
root.geometry('500x400')
root.resizable(False, False)

# frame for inputs
frame = ttk.Frame(root)

# field options
options = {'padx': 5, 'pady': 5}

# labels
texts_label = ttk.Label(frame, text='Name')
texts_label.grid(column=0, row=0, sticky='W', **options)

gender_label = ttk.Label(frame, text='Type')
gender_label.grid(column=0, row=1, sticky='W', **options)

age_label = ttk.Label(frame, text='Amount')
age_label.grid(column=0, row=2, sticky='W', **options)

birthday_label = ttk.Label(frame, text='Addition (or Object Import)')
birthday_label.grid(column=0, row=3, sticky='W', **options)

# entry fields
texts = tk.StringVar()
texts_entry = ttk.Entry(frame, textvariable=texts)
texts_entry.grid(column=1, row=0, **options)
texts_entry.focus()

# Combobox for gender selection
type = tk.StringVar()
type_combobox = ttk.Combobox(frame, textvariable=type, values=("Programmatūra", "Detaļa"), state="readonly")
type_combobox.grid(column=1, row=1, **options)
type_combobox.current(0)  # Set the default selection to 'Male'

amount = tk.IntVar()
amount_entry = ttk.Entry(frame, textvariable=amount)
amount_entry.grid(column=1, row=2, **options)

addition = tk.StringVar()
addition_entry = ttk.Entry(frame, textvariable=addition)
addition_entry.grid(column=1, row=3, **options)

# listbox update
def change_list():
    listbox.delete(0, END)
    for item in all_items:
        listbox.insert("end", f"{item.amount}, {item.name}, {item.type}")

# Create new Human
def create_button_clicked():
    item_name = texts.get()
    item_type = type.get()
    item_amount = amount.get()
    all_items.append(Item(item_name, item_amount, item_type))
    result_label.config(text=all_items[-1].info())
    change_list()

# Update selected Human
def update_button_clicked():
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No person selected")
        return

    selected_index = selected_index[0]  # Get the index of the selected item
    item = all_items[selected_index]

    # Update the attributes of the selected human
    item.name = texts.get()
    item.type = type.get()
    item.amount = amount.get()

    change_list()

# Populate fields when a person is selected from the listbox
def on_listbox_select(event):
    selected_index = listbox.curselection()
    if not selected_index:
        return

    selected_index = selected_index[0]
    selected_item = all_items[selected_index]

    # Set the current selected human's data to the input fields
    texts.set(selected_item.name)
    type.set(selected_item.type)
    amount.set(selected_item.amount)

# Increment human's age by the number entered in the birthday field
def increment_item_button_clicked():
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No person selected")
        return

    selected_index = selected_index[0]
    selected_item = all_items[selected_index]

    try:
        increment = int(addition.get())
    except ValueError:
        showerror("Input Error", "Please enter a valid number for age increment.")
        return

    # Update the human's age
    selected_item.amount += increment
    change_list()

# Create Human button
create_button = ttk.Button(frame, text='Create item', command=create_button_clicked)
create_button.grid(column=2, row=0, sticky='W', **options)

# Update Human button
update_button = ttk.Button(frame, text='Update item', command=update_button_clicked)
update_button.grid(column=2, row=1, sticky='W', **options)

# Increment Age button
increment_amount_button = ttk.Button(frame, text='item import', command=increment_item_button_clicked)
increment_amount_button.grid(column=2, row=3, sticky='W', **options)

# Result label
result_label = ttk.Label(frame)
result_label.grid(row=5, columnspan=3, **options)

# Add padding to the frame and show it
frame.grid(padx=10, pady=10)

# Frame for the listbox at the bottom
listbox_frame = ttk.Frame(root)
listbox_frame.grid(column=0, row=6, columnspan=3, padx=10, pady=10)

# Listbox for displaying all humans, placed in its own frame
saturs = tk.Variable(value=tuple(all_items))
listbox = tk.Listbox(
    listbox_frame,
    listvariable=saturs,
    height=6,
    width=50,  # Set width to ensure it fits well at the bottom
    selectmode=tk.SINGLE
)

listbox.grid(column=0, row=0, sticky='W')
listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Start the app
root.mainloop()
