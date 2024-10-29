import tkinter as tk
from tkinter import ttk
import random
from collections import defaultdict

# Temporary Data for 90 Students
students = {f"student_{i}": random.sample(["Math", "History", "Biology", "Physics", "Art", "Chemistry", "Music"], 4) for i in range(1, 91)}

teachers = {
    "Math": {"name": "Mr. A", "available_days": ["Mon", "Tue", "Wed"]},
    "History": {"name": "Mrs. B", "available_days": ["Tue", "Wed", "Thu"]},
    "Biology": {"name": "Ms. C", "available_days": ["Mon", "Thu"]},
    "Physics": {"name": "Mr. D", "available_days": ["Mon", "Wed", "Thu"]},
    "Art": {"name": "Mr. E", "available_days": ["Tue", "Thu"]},
    "Chemistry": {"name": "Ms. F", "available_days": ["Mon", "Tue"]},
    "Music": {"name": "Ms. G", "available_days": ["Wed", "Thu"]},
    "PE": {"name": "Coach H", "available_days": ["Mon", "Thu"]},
    "Russian": {"name": "Mr. I", "available_days": ["Tue", "Wed"]},
}

# Timetable constraints
days_of_week = ["Mon", "Tue", "Wed", "Thu"]
max_subjects_per_day = 10
max_students_per_class = 15  # Max number of students per teacher in a class

# Mandatory subjects
mandatory_subjects = ["PE", "Russian"]

# Initialize the timetable for each teacher (4 days x 10 subjects max per day)
teacher_timetable = defaultdict(lambda: {day: defaultdict(list) for day in days_of_week})
student_timetable = defaultdict(lambda: {day: [] for day in days_of_week})

def generate_timetable():
    for student, subjects in students.items():
        # Add mandatory subjects first (PE and Russian twice a week)
        for mandatory in mandatory_subjects:
            days_for_mandatory = random.sample(teachers[mandatory]["available_days"], 2)
            for day in days_for_mandatory:
                # Assign the mandatory subject to the student
                if len(teacher_timetable[teachers[mandatory]['name']][day][mandatory]) < max_students_per_class:
                    teacher_timetable[teachers[mandatory]['name']][day][mandatory].append(student)
                    student_timetable[student][day].append((mandatory, teachers[mandatory]['name']))
        
        # Distribute elective subjects for each student
        for subject in subjects:
            for day in days_of_week:
                if subject in teachers and day in teachers[subject]["available_days"]:
                    # Allow multiple classes for the same subject on the same day
                    if len(teacher_timetable[teachers[subject]['name']][day][subject]) < max_students_per_class:
                        teacher_timetable[teachers[subject]['name']][day][subject].append(student)
                        student_timetable[student][day].append((subject, teachers[subject]['name']))

    # Allow teachers to teach the same subject multiple times a day
    for teacher_key, teacher in teachers.items():
        for day in teacher["available_days"]:
            if day in days_of_week:
                # Randomly decide how many classes of this subject to schedule (up to 3)
                num_classes = random.randint(1, 3)
                for _ in range(num_classes):
                    if len(teacher_timetable[teacher['name']][day][teacher_key]) < max_students_per_class:
                        eligible_students = [s for s in students.keys() if s not in teacher_timetable[teacher['name']][day][teacher_key]]
                        if eligible_students:
                            student_to_add = random.choice(eligible_students)
                            teacher_timetable[teacher['name']][day][teacher_key].append(student_to_add)
                            student_timetable[student_to_add][day].append((teacher_key, teacher['name']))

# Tkinter Setup to display the timetable for each teacher
def display_teacher_timetable():
    generate_timetable()
    root = tk.Tk()
    root.title("Teacher Timetable")

    # Create a notebook widget (tabbed layout)
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    # Button to open individual student timetables
    button = ttk.Button(root, text="View Student Timetables", command=display_student_timetable)
    button.pack(pady=10)

    # Create tabs for each teacher
    for teacher, schedule in teacher_timetable.items():
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=teacher)

        # Create the layout for each day
        for day in days_of_week:
            if schedule[day]:
                ttk.Label(tab, text=f"Schedule for {day}:", font=("Arial", 10, "bold")).pack(pady=5)

                # Numbering classes in the order they happen
                class_number = 1
                for subject, students_list in schedule[day].items():
                    frame = ttk.Frame(tab)
                    frame.pack(fill="x", padx=5, pady=2)

                    # Display subject being taught by the teacher with class number
                    subject_label = ttk.Label(frame, text=f"{class_number}. {subject} (Teacher: {teachers[subject]['name']}):", width=40)
                    subject_label.pack(side="left")

                    # Create a listbox for students in that specific class
                    listbox = tk.Listbox(frame, height=5, selectmode="browse")
                    for student in students_list:
                        listbox.insert(tk.END, student)

                    listbox.pack(side="right", fill="x", expand=True)
                    class_number += 1  # Increment class number

    root.mainloop()

# Function to display the student timetables in a new window
def display_student_timetable():
    window = tk.Toplevel()
    window.title("Student Timetables")

    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, expand=True)

    # Create tabs for each student
    for student, schedule in student_timetable.items():
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=student)

        tree = ttk.Treeview(tab, columns=days_of_week, show='headings', height=10)
        for day in days_of_week:
            tree.heading(day, text=day)

        # Fill each day with the subjects and corresponding teacher's name
        for i in range(max_subjects_per_day):
            day_subjects = []
            for day in days_of_week:
                if len(schedule[day]) > i:
                    subject, teacher = schedule[day][i]
                    day_subjects.append(f"{i + 1}. {subject} (Teacher: {teacher})")
                else:
                    day_subjects.append("")

            tree.insert("", "end", values=day_subjects)

        tree.pack(expand=True, fill="both")

if __name__ == "__main__":
    display_teacher_timetable()
