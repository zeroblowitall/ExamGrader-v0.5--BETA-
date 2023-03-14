import json, os, csv, sys
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QLabel
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from datetime import datetime
from grader_logic import ExamGrader


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('images/icon.png'))

class ButtonLogic:
    def __init__(self, label):
        self.label = label
    def run(self):
        None

class FilesToCheckButtonLogic(ButtonLogic):
    def run(self):
        super().run()
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(
            None, "Select Exam Folder", options=options
        )
        if folder_path:
            print(folder_path)
            self.label.setText(f"Folder: {os.path.basename(folder_path)}")

class CriteriaFileButtonLogic(ButtonLogic):
    def run(self):
        super().run()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Criteria File", "", "JSON Files (*.json)", options=options
        )
        if file_path:
            print(file_path)
            self.label.setText(f"File: {os.path.basename(file_path)}")

class GradeExamLogic:
    def __init__(self, folder_label, criteria_label, score_label, part_dict):
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.part_dict = part_dict
        self.exam_grader = None
        self.individual_scores = {}

    def run(self):
        folder_path_display = self.folder_label.text().split(': ')[-1]
        folder_path = os.path.abspath(folder_path_display)
        criteria_file_path = self.criteria_label.text().split(': ')[-1]
        print(criteria_file_path)  
        try:
            # Create an instance of the ExamGrader class
            self.exam_grader = ExamGrader(folder_path_display, criteria_file_path)
            # Load the criteria
            with open(criteria_file_path, 'r') as f:
                self.criteria = json.load(f)
            # Grade the exam and get the total score
            self.exam_grader.grade_exam()
            total_score = self.exam_grader.total_score
            
            # Update the individual scores and score label in the GUI
            for part_number, part_info in self.part_dict.items():
                result_field = part_info['result_field']
                result_label = part_info['result_label']
                score = int(result_field.text())
                self.individual_scores[part_number] = score
                result_label.setText(str(score))

            total_score += sum(self.individual_scores.values())
            self.score_label.setText(f'Total Score: {round(total_score, 2)}')

        except FileNotFoundError:
            error_message = f"Error: Please select an Exam Folder and Criteria File"
            QMessageBox.critical(None, "Error", error_message)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            QMessageBox.critical(None, "Error", error_message)

        # Update the folder_label widget with the simplified path
        self.folder_label.setText(f"Folder: {os.path.basename(folder_path_display)}")

class ViewDetailsLogic:
    def __init__(self, folder_label, criteria_label, score_label, part_dict):
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.part_dict = part_dict
        self.exam_grader = None
        self.individual_scores = {}

    def run(self):
        folder_path_display = self.folder_label.text().split(': ')[-1]
        folder_path = os.path.abspath(folder_path_display)
        criteria_file_path = self.criteria_label.text().split(': ')[-1]
        print(criteria_file_path)  
        try:
            # Create an instance of the ExamGrader class
            self.exam_grader = ExamGrader(folder_path_display, criteria_file_path)
            # Load the criteria
            with open(criteria_file_path, 'r') as f:
                self.criteria = json.load(f)
            # Grade the exam and get the total score
            self.exam_grader.grade_exam()
            total_score = self.exam_grader.total_score
            
            # Update the individual scores and score label in the GUI
            for part_number, part_info in self.part_dict.items():
                result_field = part_info['result_field']
                result_label = part_info['result_label']
                score = int(result_field.text())
                self.individual_scores[part_number] = score
                result_label.setText(str(score))

            total_score += sum(self.individual_scores.values())
            self.score_label.setText(f'Total Score: {round(total_score, 2)}')

            show_details_logic = ShowDetailsLogic(self.exam_grader)  # Pass the ExamGrader object to the constructor
            show_details_logic.run()

        except FileNotFoundError:
            error_message = f"Error: Please select an Exam Folder and Criteria File"
            QMessageBox.critical(None, "Error", error_message)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            QMessageBox.critical(None, "Error", error_message)

        # Update the folder_label widget with the simplified path
        self.folder_label.setText(f"Folder: {os.path.basename(folder_path_display)}")

class ShowDetailsLogic:
    def __init__(self, exam_grader):
        self.results_dict = exam_grader.get_results_dict()

    def run(self):
        if self.results_dict is not None:
            # Create a new window to display the table
            table_window = QDialog()
            table_window.setWindowTitle('Exam Details')
            table_window.setWindowIcon(QIcon('images/icon.png'))

            # Create a QGroupBox for the total score details
            total_score_groupbox = QGroupBox()
            total_score_label = QLabel()
            total_score_label.setAlignment(Qt.AlignCenter)
            total_score_label.setMargin(10)

            # Create a table to display the exam details
            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(['Device', 'Question', 'Result', 'Score', 'Weight'])

            # Read the criteria sections from the criteria.json file
            with open('criteria.json') as f:
                criteria_dict = json.load(f)
            sections = {}
            for key, value in criteria_dict.items():
                section = value.get('section', 'Default')
                if section not in sections:
                    sections[section] = []
                sections[section].append(key)

            # Group the rows by section
            section_rows = {}
            for exam_file, results in self.results_dict.items():
                device = exam_file.split('.')[0]
                for key, value in results.items():
                    question = f"{key}"
                    answer = value['answer']
                    weight = value['weight']
                    points = value['points']
                    result = 'Correct' if points > 0 else 'Incorrect'
                    score = weight if points > 0 else 0
                    section = criteria_dict.get(key, {}).get('section', 'Default')
                    row = (device, question, result, score, weight)
                    if section not in section_rows:
                        section_rows[section] = []
                    section_rows[section].append(row)

            # Add the exam details to the table by section
            total_score = 0
            for section_name, section_keys in sections.items():
                section_rows_list = []
                for row in section_rows.get(section_name, []):
                    section_rows_list.append(row)
                if section_rows_list:
                    # Add the section name row
                    table.insertRow(table.rowCount())
                    section_item = QTableWidgetItem(f'{section_name} Section')
                    section_item.setFlags(Qt.NoItemFlags)
                    section_item.setBackground(QColor('lightgray'))
                    table.setItem(table.rowCount() - 1, 0, section_item)
                    table.setSpan(table.rowCount() - 1, 0, 1, table.columnCount())
                    # Add the rows for this section
                    for row in section_rows_list:
                        table.insertRow(table.rowCount())
                        for j, item in enumerate(row):
                            table.setItem(table.rowCount() - 1, j, QTableWidgetItem(str(item)))
                            # Set the background color of the result column
                            if j == 2:
                                if item == 'Correct':
                                    table.item(table.rowCount() - 1, j).setBackground(QColor('green'))
                                else:
                                    table.item(table.rowCount() - 1, j).setBackground(QColor('red'))
                        total_score += row[3]

            # Calculate pass/fail status
            pass_threshold = 45.0
            pass_status = 'PASS' if total_score >= pass_threshold else 'FAIL'
            if pass_status == 'PASS':
                total_score_label.setText(f'Total Score: {round(total_score, 2)} - Pass')
                total_score_groupbox.setStyleSheet('background-color: green')
            else:
                total_score_label.setText(f'Total Score: {round(total_score, 2)} - Fail')
                total_score_groupbox.setStyleSheet('background-color: red')
            
            # Add the total score label to the total score groupbox
            total_score_groupbox_layout = QHBoxLayout()
            total_score_groupbox_layout.addWidget(total_score_label)
            total_score_groupbox.setLayout(total_score_groupbox_layout)

            # Resize the columns to fit the contents
            table.resizeColumnsToContents()

            # Calculate the width of each column
            column_widths = [table.columnWidth(i) for i in range(table.columnCount())]
            # Calculate the total width of the table
            table_width = sum(column_widths)

            # Create a layout for the table and add it to the window
            layout = QVBoxLayout()
            layout.addWidget(total_score_groupbox)
            layout.addWidget(table)
            table_window.setLayout(layout)

            # Create a button box to hold the Close and Save buttons
            button_box = QHBoxLayout()
            save_button = QPushButton('Save')
            close_button = QPushButton('Close')            
            button_box.addWidget(save_button)
            button_box.addWidget(close_button)
            layout.addLayout(button_box)

            # Connect the Close button to the table window's close method
            close_button.clicked.connect(table_window.close)

            # Connect the Save button to a function that saves the results to a CSV file
            save_button.clicked.connect(lambda: self.save_to_csv(section_rows))

            # Position the window to the right of the main window
            main_window = QApplication.activeWindow()
            main_window_pos = main_window.pos()
            main_window_size = main_window.size()
            table_window.move(main_window_pos.x() + main_window_size.width(), main_window_pos.y())

            # Set the minimum size of the window
            min_size = QSize(table_width + 150, 1000)
            table_window.setMinimumSize(min_size)

            # Show the window
            table_window.exec_()
        else:
            print('ExamGrader instance not found.')

    def save_to_csv(self, section_rows):
        # Get the current timestamp for the filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Create the filename for the CSV file
        filename = f"exam_results_{timestamp}.csv"

        # Write the exam results to the CSV file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Section', 'Device', 'Question', 'Result', 'Score', 'Weight'])
            for section_name, rows in section_rows.items():
                for row in rows:
                    writer.writerow([section_name] + list(row))
    
        # Show a message box to confirm that the results were saved
        QMessageBox.information(None, 'Save Results', f'The exam results have been saved to "{filename}".')

class ResetLogic:
    def __init__(self, folder_label, criteria_label, score_label, part_dict):
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.part_dict = part_dict

    def run(self):
        self.folder_label.clear()
        self.criteria_label.clear()
        self.score_label.setText('Score: 0')
        for part_number, part_info in self.part_dict.items():
            part_info['result_field'].setText('0')
            part_info['result_label'].setText('0')


class QuitLogic:
    def __init__(self):
        None

    def run(self):
        choice = QMessageBox.question(None, "Quit", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QApplication.quit()
