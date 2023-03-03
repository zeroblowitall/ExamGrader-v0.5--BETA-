from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from details_logic import GradingDetailsDialog
import grader_logic
import os, re, json

class FilesToCheckButtonLogic:
    def __init__(self, folder_label):
        print('FilesToCheckButton logic instantiated')
        self.folder_label = folder_label

    def run(self):
        print('FilesToCheckButton clicked')
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(None, "Select Exam Folder", options=options)
        if folder_path:
            print(folder_path)
            self.folder_label.setText(f"Selected Folder: {folder_path.split('/')[-1]}")

class CriteriaFileButtonLogic:
    def __init__(self, file_label):
        print('CriteriaFileButton logic instantiated')
        self.file_label = file_label

    def run(self):
        print('CriteriaFileButton clicked')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Criteria File", "", "JSON Files (*.json)", options=options)
        if file_path:
            print(file_path)
            self.file_label.setText(f"Selected Criteria File: {file_path.split('/')[-1]}")

class GradeExamLogic:
    def __init__(self, folder_label, criteria_label, score_label):
        print('GradeExamButton logic instantiated')
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label

    def run(self):
        print('GradeExamButton clicked')
        folder_path = self.folder_label.text().split(': ')[-1]
        criteria_file_path = self.criteria_label.text().split(': ')[-1]
        
        try:
            # Create an instance of the ExamGrader class
            self.exam_grader = grader_logic.ExamGrader(folder_path, criteria_file_path)

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

        except Exception as e:
            error_message = f"Error: You must select a folder and criteria file"
            QMessageBox.critical(None, "Error", error_message)

class ShowDetailsLogic:
    def __init__(self, criteria_fn, exam_grader_fn):
        print('ShowDetailsButton logic instantiated')
        self.criteria_fn = criteria_fn
        self.exam_grader_fn = exam_grader_fn

    def run(self):
        print('ShowDetailsButton clicked')
        criteria = self.criteria_fn()
        exam_grader = self.exam_grader_fn()
        grading_details_dialog = GradingDetailsDialog(criteria, exam_grader)
        grading_details_dialog.exec_()

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

