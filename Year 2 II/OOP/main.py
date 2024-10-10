from test1 import Human , Sieviete
import tkinter as tk
from tkinter import ttk, END
from tkinter.messagebox import showerror

all_humans = []

# root window
root = tk.Tk()
root.title('Human Generator')
root.geometry('500x400')  # Increased height to accommodate the listbox at the bottom
root.resizable(False, False)

# frame for inputs
frame = ttk.Frame(root)

# field options
options = {'padx': 5, 'pady': 5}

# labels
texts_label = ttk.Label(frame, text='Name')
texts_label.grid(column=0, row=0, sticky='W', **options)

gender_label = ttk.Label(frame, text='Gender')
gender_label.grid(column=0, row=1, sticky='W', **options)

age_label = ttk.Label(frame, text='Age')
age_label.grid(column=0, row=2, sticky='W', **options)

birthday_label = ttk.Label(frame, text='Birthday (or Age Increment)')
birthday_label.grid(column=0, row=3, sticky='W', **options)

# entry fields
texts = tk.StringVar()
texts_entry = ttk.Entry(frame, textvariable=texts)
texts_entry.grid(column=1, row=0, **options)
texts_entry.focus()

# Combobox for gender selection
gender = tk.StringVar()
gender_combobox = ttk.Combobox(frame, textvariable=gender, values=["Male", "Female", "Other"], state="readonly")
gender_combobox.grid(column=1, row=1, **options)
gender_combobox.current(0)  # Set the default selection to 'Male'

age = tk.IntVar()
age_entry = ttk.Entry(frame, textvariable=age)
age_entry.grid(column=1, row=2, **options)

birthday = tk.StringVar()
birthday_entry = ttk.Entry(frame, textvariable=birthday)
birthday_entry.grid(column=1, row=3, **options)

# listbox update
def change_list():
    listbox.delete(0, END)
    for human in all_humans:
        listbox.insert(f"end", f"{human.age}, {human.name}, {human.sex}")

# Create new Human
def create_button_clicked():
    human_name = texts.get()
    human_gender = gender.get()
    human_age = age.get()
    all_humans.append(Human(human_name, human_age, human_gender))
    result_label.config(text=all_humans[-1].info())
    change_list()

# Update selected Human
def update_button_clicked():
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No person selected")
        return

    selected_index = selected_index[0]  # Get the index of the selected item
    human = all_humans[selected_index]

    # Update the attributes of the selected human
    human.name = texts.get()
    human.sex = gender.get()
    human.age = age.get()

    change_list()

# Populate fields when a person is selected from the listbox
def on_listbox_select(event):
    selected_index = listbox.curselection()
    if not selected_index:
        return

    selected_index = selected_index[0]
    selected_human = all_humans[selected_index]

    # Set the current selected human's data to the input fields
    texts.set(selected_human.name)
    gender.set(selected_human.sex)
    age.set(selected_human.age)

# Increment human's age by the number entered in the birthday field
def increment_age_button_clicked():
    selected_index = listbox.curselection()
    if not selected_index:
        showerror("Selection Error", "No person selected")
        return

    selected_index = selected_index[0]
    selected_human = all_humans[selected_index]

    try:
        increment = int(birthday.get())
    except ValueError:
        showerror("Input Error", "Please enter a valid number for age increment.")
        return

    # Update the human's age
    selected_human.age += increment
    change_list()

# Create Human button
create_button = ttk.Button(frame, text='Create HUMAN', command=create_button_clicked)
create_button.grid(column=2, row=0, sticky='W', **options)

# Update Human button
update_button = ttk.Button(frame, text='Update HUMAN', command=update_button_clicked)
update_button.grid(column=2, row=1, sticky='W', **options)

# Increment Age button
increment_age_button = ttk.Button(frame, text='Increment Age', command=increment_age_button_clicked)
increment_age_button.grid(column=2, row=3, sticky='W', **options)

# Result label
result_label = ttk.Label(frame)
result_label.grid(row=5, columnspan=3, **options)

# Add padding to the frame and show it
frame.grid(padx=10, pady=10)

# Frame for the listbox at the bottom
listbox_frame = ttk.Frame(root)
listbox_frame.grid(column=0, row=6, columnspan=3, padx=10, pady=10)

# Listbox for displaying all humans, placed in its own frame
saturs = tk.Variable(value=tuple(all_humans))
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
