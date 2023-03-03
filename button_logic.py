from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
from grader_logic import ExamGrader
import json, os

class ButtonLogic:
    def __init__(self, label):
        self.label = label
        print(f"{self.__class__.__name__} logic instantiated")
    def run(self):
        print(f"{self.__class__.__name__} clicked")

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
            self.label.setText(f"Selected Folder: {os.path.basename(folder_path)}")

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
            self.label.setText(f"Selected Criteria File: {os.path.basename(file_path)}")

class GradeExamLogic:
    def __init__(self, folder_label, criteria_label, score_label):
        print('GradeExamButton logic instantiated')
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.exam_grader = None

    def run(self):
        print('GradeExamButton clicked')
        folder_path = self.folder_label.text().split(': ')[-1]
        criteria_file_path = self.criteria_label.text().split(': ')[-1]       
        try:
            # Create an instance of the ExamGrader class
            self.exam_grader = ExamGrader(folder_path, criteria_file_path)
            # Load the criteria
            with open(criteria_file_path, 'r') as f:
                self.criteria = json.load(f)
            # Grade the exam and get the total score
            self.exam_grader.grade_exam()
            total_score = self.exam_grader.total_score
            
            # Update the output text and score label
            self.score_label.setText(f'Score: {total_score}')
            self.criteria = self.exam_grader.criteria
            self.exam_grader = self.exam_grader

        except FileNotFoundError:
            error_message = f"Error: File not found"
            QMessageBox.critical(None, "Error", error_message)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            QMessageBox.critical(None, "Error", error_message)

class ViewDetailsLogic:
    def __init__(self, folder_label, criteria_label, score_label):
        print('GradeExamButton logic instantiated')
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.exam_grader = None

    def run(self):
        print('GradeExamButton clicked')
        folder_path = self.folder_label.text().split(': ')[-1]
        criteria_file_path = self.criteria_label.text().split(': ')[-1]       
        try:
            # Create an instance of the ExamGrader class
            self.exam_grader = ExamGrader(folder_path, criteria_file_path)
            # Load the criteria
            with open(criteria_file_path, 'r') as f:
                self.criteria = json.load(f)
            # Grade the exam and get the total score
            self.exam_grader.grade_exam()
            total_score = self.exam_grader.total_score
            
            # Update the output text and score label
            self.score_label.setText(f'Score: {total_score}')
            self.criteria = self.exam_grader.criteria
            self.exam_grader = self.exam_grader

            results_dict = self.exam_grader.get_results_dict()
            show_details_logic = ShowDetailsLogic(self.exam_grader)  # Pass the ExamGrader object to the constructor
            show_details_logic.run()

        except FileNotFoundError:
            error_message = f"Error: File not found"
            QMessageBox.critical(None, "Error", error_message)

        except Exception as e:
            error_message = f"Error: {str(e)}"
            QMessageBox.critical(None, "Error", error_message)

class ShowDetailsLogic:
    def __init__(self, exam_grader):
        print('ShowDetailsButton logic instantiated')
        self.results_dict = exam_grader

    def run(self):
        print('ShowDetailsButton clicked')
        if self.results_dict is not None:
            # Create a new window to display the table
            table_window = QDialog()
            table_window.setWindowTitle('Exam Details')

            # Create a table to display the exam details
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(['Question', 'Score'])

            # Add the exam details to the table
            for i, (question, score) in enumerate(self.results_dict.criteria.items()):
                table.insertRow(i)
                table.setItem(i, 0, QTableWidgetItem(question))
                table.setItem(i, 1, QTableWidgetItem(str(score)))

            # Create a layout for the table and add it to the window
            layout = QVBoxLayout()
            layout.addWidget(table)
            table_window.setLayout(layout)

            # Show the window
            table_window.exec_()
        else:
            print('ExamGrader instance not found.')

class ResetLogic:
    def __init__(self, folder_label, criteria_label, score_label):
        print('ResetButton logic instantiated')
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label

    def run(self):
        print('ResetButton clicked')
        self.folder_label.clear()
        self.criteria_label.clear()
        self.score_label.setText('Score: 0')

class QuitLogic:
    def __init__(self):
        print('QuitButton logic instantiated')

    def run(self):
        print('QuitButton clicked')
        choice = QMessageBox.question(None, "Quit", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QApplication.quit()
