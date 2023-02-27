import tkinter as tk
from tkinter import filedialog
import config_grader
from detailsWindow import DetailsWindow
import json

def select_file(file_type, file_path_var):
    # Open a file dialog to select a file of the specified type
    file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", f'*.{file_type}')])
    if file_path:
        # Assign the file path to the specified variable
        file_path_var.set(file_path)

def on_grade_button_clicked(config_file_var, criteria_file_var, grade_label):
    # Get the file paths from the variables
    config_file = config_file_var.get()
    criteria_file = criteria_file_var.get()

    if not config_file:
        tk.messagebox.showerror('Error', 'Please select a configuration file')
        return

    if not criteria_file:
        tk.messagebox.showerror('Error', 'Please select a criteria file')
        return

    # Grade the configuration file with the given criteria file and display the grade
    grade = config_grader.grade_configuration(config_file, criteria_file)
    grade_label.config(text=f'{grade[0]:.2f}')
    grade_label['fg'] = 'green' if grade[0] >= 70 else 'red'

def on_reset_button_clicked(config_file_var, criteria_file_var, grade_label):
    # Clear the file paths from the variables and reset the grade label
    config_file_var.set('')
    criteria_file_var.set('')
    grade_label.config(text='')

def on_quit_button_clicked():
    # Close the window
    window.destroy()

def on_details_button_clicked(config_file, criteria_file):
    # Load the criteria from the criteria file
    with open(criteria_file, 'r') as f:
        criteria_dict = json.load(f)

    # Open the configuration file and read its contents
    with open(config_file, 'r') as f:
        config = f.read()

    # Grade the configuration file with the given criteria file to get matched criteria
    matched_criteria = config_grader.get_matched_criteria(config, criteria_dict)

    # Create a new window to display the details
    details_window = DetailsWindow(window, criteria_dict, config, matched_criteria)

# Create a Tkinter window
window = tk.Tk()
window.title("Exam Grader V0.1")

# Set the window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = int(screen_height / 2)
window_height = int(screen_height / 2)
window.geometry(f"{window_width}x{window_height}")

# Define the frames
# Create the top frame and add it to the window
top_frame = tk.Frame(window, bg='white', width=screen_width, height=int(screen_height/2))
top_frame.pack(side='top', fill='both', expand=True)
top_frame.pack_propagate(False)  # Prevent the frame from resizing

middle_frame = tk.Frame(window)
middle_frame.pack()

bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM, pady=10)

# Set the window to not be resizable
window.resizable(False, False)

# Define variables for the configuration file and criteria file paths
config_file_var = tk.StringVar()
criteria_file_var = tk.StringVar()

# Add buttons to select the configuration and criteria files
config_button = tk.Button(top_frame, text='Select Config File', command=lambda: select_file('txt', config_file_var))
config_button.grid(row=0, column=0, padx=10, pady=10)

criteria_button = tk.Button(top_frame, text='Select Criteria File', command=lambda: select_file('json', criteria_file_var))
criteria_button.grid(row=1, column=0, padx=10, pady=10)

# Add a button to grade the configuration file with the given criteria file
grade_button = tk.Button(top_frame, text='Grade Configuration', command=lambda: on_grade_button_clicked(config_file_var, criteria_file_var, grade_label))
grade_button.grid(row=2, column=0, padx=10, pady=10)

# Add a Details button to show the details of the grading criteria
details_button = tk.Button(top_frame, text='Details...', command=lambda: on_details_button_clicked(config_file_var.get(), criteria_file_var.get()))
details_button.grid(row=2, column=1, padx=10, pady=10)

# Add labels once the files have been selected
config_file_label = tk.Label(top_frame, textvariable=config_file_var, fg='gray')
config_file_label.grid(row=0, column=1, padx=10, pady=10)

criteria_file_label = tk.Label(top_frame, textvariable=criteria_file_var, fg='gray')
criteria_file_label.grid(row=1, column=1, padx=10, pady=10)

# Add a label to display the grade
grade_box = tk.LabelFrame(window, text='Grade', bd=4, relief='ridge')
grade_box.place(relx=0.8, rely=0.0, relwidth=0.15, relheight=0.1)

grade_label = tk.Label(grade_box, text='--')
grade_label.pack(expand=True, fill='both')

# Add a quit button to close the window
quit_button = tk.Button(bottom_frame, text='Quit', command=on_quit_button_clicked, bg='red')
quit_button.pack(side=tk.RIGHT, padx=10)

# Add a reset button to clear the file paths and grade label
reset_button = tk.Button(bottom_frame, text='Reset', command=lambda: on_reset_button_clicked(config_file_var, criteria_file_var, grade_label), bg='yellow')
reset_button.pack(side=tk.RIGHT, padx=10)

# Start the Tkinter event loop
window.mainloop()
