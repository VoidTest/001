from item import Item
import tkinter as tk
from tkinter import ttk, END, Radiobutton
from tkinter.messagebox import showerror

all_items = []
total_profit = 0  # Variable to keep track of total profit

# root window
root = tk.Tk()
root.title('Veikala objektu uzskaititajs')
root.geometry('600x400')  # Increased width to accommodate price field
root.resizable(False, False)

# frame for inputs
frame = ttk.Frame(root)

# field options
options = {'padx': 5, 'pady': 5}

# labels
texts_label = ttk.Label(frame, text='Name')
texts_label.grid(column=0, row=0, sticky='W', **options)

type_label = ttk.Label(frame, text='Type')
type_label.grid(column=0, row=1, sticky='W', **options)

amount_label = ttk.Label(frame, text='Amount')
amount_label.grid(column=0, row=4, sticky='W', **options)

price_label = ttk.Label(frame, text='Price')  # New label for price
price_label.grid(column=0, row=5, sticky='W', **options)

# entry fields
texts = tk.StringVar()
texts_entry = ttk.Entry(frame, textvariable=texts)
texts_entry.grid(column=1, row=0, **options)
texts_entry.focus()

# Replacing the Combobox with Radiobuttons for type selection
item_type = tk.StringVar(value="Programmatūra")  # Default value

radiobutton1 = Radiobutton(frame, text="Programmatūra", variable=item_type, value="Programmatūra")
radiobutton2 = Radiobutton(frame, text="Detaļa", variable=item_type, value="Detaļa")
radiobutton3 = Radiobutton(frame, text="Dators", variable=item_type, value="Dators")

radiobutton1.grid(column=1, row=1, sticky='W', **options)
radiobutton2.grid(column=1, row=2, sticky='W', **options)
radiobutton3.grid(column=1, row=3, sticky='W', **options)

amount = tk.IntVar()
amount_entry = ttk.Entry(frame, textvariable=amount)
amount_entry.grid(column=1, row=4, **options)

# New field for price input
price = tk.DoubleVar()
price_entry = ttk.Entry(frame, textvariable=price)
price_entry.grid(column=1, row=5, **options)

# Manufacturer label and entry
manufacturer_label = ttk.Label(frame, text='Manufacturer')
manufacturer_entry = ttk.Entry(frame)
manufacturer_label.grid(column=0, row=7, sticky='W', **options)
manufacturer_entry.grid(column=1, row=7, **options)

manufacturer_label.grid_remove()
manufacturer_entry.grid_remove()

# Toggle manufacturer entry
def toggle_manufacturer():
    selected_type = item_type.get()
    if selected_type == "Dators":
        manufacturer_label.grid()
        manufacturer_entry.grid()
    else:
        manufacturer_label.grid_remove()
        manufacturer_entry.grid_remove()

for rb in [radiobutton1, radiobutton2, radiobutton3]:
    rb.config(command=toggle_manufacturer)

def change_list():
    listbox.delete(0, END)
    for item in all_items:
        if item.manufacturer:
            listbox.insert("end", f"Name:  {item.name},  Type: {item.type}, Amount: {item.amount}, Price: {item.price}, Manufacturer: {item.manufacturer}")
        else:
            listbox.insert("end", f"Name:  {item.name},  Type: {item.type}, Amount: {item.amount}, Price: {item.price}")

# Create new Item
def create_button_clicked():
    item_name = texts.get().strip()
    item_type_value = item_type.get()
    item_amount = amount.get()
    item_price = price.get()

    # Check if the item name is empty
    if not item_name:
        showerror("Input Error", "Please enter a name for the item.")
        return

    # If Dators is selected, get manufacturer input
    if item_type_value == "Dators":
        manufacturer = manufacturer_entry.get().strip()
        if not manufacturer:
            showerror("Input Error", "Please enter a manufacturer for Dators.")
            return
    else:
        manufacturer = None

    new_item = Item(item_name, item_amount, item_type_value, price=item_price, manufacturer=manufacturer)
    all_items.append(new_item)

    change_list()

# Update selected Item
def update_button_clicked():
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No item selected")
        return

    selected_index = selected_index[0]
    item = all_items[selected_index]

    item.name = texts.get()
    item.type = item_type.get()
    item.amount = amount.get()
    item.price = price.get() 

    if item.type == "Dators":
        manufacturer = manufacturer_entry.get()
        if not manufacturer:
            showerror("Input Error", "Please enter a manufacturer for Dators.")
            return
        item.manufacturer = manufacturer

    change_list()

# Populate fields when an item is selected from the listbox
def on_listbox_select(event):
    selected_index = listbox.curselection()
    if not selected_index:
        return

    selected_index = selected_index[0]
    selected_item = all_items[selected_index]

    texts.set(selected_item.name)
    item_type.set(selected_item.type)
    amount.set(selected_item.amount)
    price.set(selected_item.price) 

    if selected_item.type == "Dators":
        manufacturer_entry.delete(0, END)
        manufacturer_entry.insert(0, selected_item.manufacturer)
        manufacturer_label.grid()
        manufacturer_entry.grid()
    else:
        manufacturer_label.grid_remove()
        manufacturer_entry.grid_remove()

# Sell item and update profit
def sell_item_button_clicked():
    global total_profit
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No item selected")
        return

    selected_index = selected_index[0]
    selected_item = all_items[selected_index]

    if selected_item.amount <= 0:
        showerror("Stock Error", "Cannot sell. Item is out of stock.")
        return

    selected_item.amount -= 1

    total_profit += selected_item.price

    change_list()
    profit_label.config(text=f"Total Profit: {total_profit:.2f} EUR")

# Create Item button
create_button = ttk.Button(frame, text='Create item', command=create_button_clicked)
create_button.grid(column=2, row=0, sticky='W', **options)

# Update Item button
update_button = ttk.Button(frame, text='Update item', command=update_button_clicked)
update_button.grid(column=2, row=1, sticky='W', **options)

# Sell Item button
sell_item_button = ttk.Button(frame, text='Sell Item', command=sell_item_button_clicked)
sell_item_button.grid(column=2, row=2, sticky='W', **options)

# New label for displaying total profit
profit_label = ttk.Label(frame, text=f"Total Profit: {total_profit:.2f} EUR")
profit_label.grid(row=8, columnspan=3, **options)

frame.grid(padx=10, pady=10)

listbox_frame = ttk.Frame(root)
listbox_frame.grid(column=0, row=9, columnspan=3, padx=10, pady=10)

saturs = tk.Variable(value=tuple(all_items))
listbox = tk.Listbox(
    listbox_frame,
    listvariable=saturs,
    height=6,
    width=80,
    selectmode=tk.SINGLE
)

listbox.grid(column=0, row=0, sticky='W')
listbox.bind('<<ListboxSelect>>', on_listbox_select)

root.mainloop()
