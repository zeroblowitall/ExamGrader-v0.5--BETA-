import tkinter as tk
from tkinter import filedialog
import csv

class DetailsWindow(tk.Toplevel):
    def __init__(self, parent, criteria_dict, config_file, matched_criteria):
        super().__init__(parent)
        self.title('Details')

        # Assign the criteria_dict argument to the criteria_dict attribute
        self.criteria_dict = criteria_dict

        # Store the config_file and matched_criteria variables as attributes
        self.config_file = config_file
        self.matched_criteria = matched_criteria

        # Create a table to display the details
        self.table = tk.Frame(self)
        self.table.pack()

        # Create the header row
        header_row = tk.Frame(self.table)
        header_row.pack(side=tk.TOP, fill=tk.X)
        criterion_label = tk.Label(header_row, text='Criterion', relief=tk.RAISED, width=20)
        criterion_label.pack(side=tk.LEFT, fill=tk.X)
        answer_label = tk.Label(header_row, text='Answer', relief=tk.RAISED, width=20)
        answer_label.pack(side=tk.LEFT, fill=tk.X)
        weight_label = tk.Label(header_row, text='Weight', relief=tk.RAISED, width=20)
        weight_label.pack(side=tk.LEFT, fill=tk.X)
        result_label = tk.Label(header_row, text='Result', relief=tk.RAISED, width=20)
        result_label.pack(side=tk.LEFT, fill=tk.X)

        # Store the config_file variable as an attribute
        self.config_file = config_file

        # Loop through each criterion and add a row to the table for each one
        for criterion, criteria_details in criteria_dict.items():
            answer = criteria_details['answer']
            weight = criteria_details['weight']
            if answer in config_file:
                result = 'Correct'
                bg_color = 'green'
            else:
                result = 'Incorrect'
                bg_color = 'red'

            row = tk.Frame(self.table)
            row.pack(side=tk.TOP, fill=tk.X)
            criterion_label = tk.Label(row, text=criterion, relief=tk.SUNKEN, width=20)
            criterion_label.pack(side=tk.LEFT, fill=tk.X)
            answer_label = tk.Label(row, text=answer, relief=tk.SUNKEN, width=20)
            answer_label.pack(side=tk.LEFT, fill=tk.X)
            weight_label = tk.Label(row, text=weight, relief=tk.SUNKEN, width=20)
            weight_label.pack(side=tk.LEFT, fill=tk.X)
            result_label = tk.Label(row, text=result, relief=tk.SUNKEN, bg=bg_color, width=20)
            result_label.pack(side=tk.LEFT, fill=tk.X)

        # Add a Save button to save the details to a file
        save_button = tk.Button(self, text='Save to CSV', command=self.save_to_csv)
        save_button.pack(side=tk.LEFT, padx=10)

        # Add a Close button to close the details window
        close_button = tk.Button(self, text='Close', command=self.destroy)
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def save_to_csv(self):
        # Open a file dialog to select the output file path
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if not file_path:
            return

        # Open the output file for writing
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write the header row
            writer.writerow(['Criterion', 'Answer', 'Weight', 'Result'])

            # Write each row
        for criterion, criteria_details in self.criteria_dict.items():
            answer = criteria_details['answer']
            weight = criteria_details['weight']
            if criterion in self.matched_criteria:
                result = 'Correct'
                bg_color = 'green'
            else:
                result = 'Incorrect'
                bg_color = 'red'

            writer.writerow([criterion, answer, weight, result])


        # Show a message box to confirm the file has been saved
        tk.messagebox.showinfo('Success', f'Details have been saved to {file_path}')