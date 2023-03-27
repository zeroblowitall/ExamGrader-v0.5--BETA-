import json
from PyQt5.QtWidgets import QMessageBox
from grader_logic import ExamGrader
from show_details_logic import ShowDetailsLogic

class GradeExamLogic:
    def __init__(self, folder_logic, criteria_logic, score_label, part_dict, main_window, exam_type, gui_ref, show_details=False):
        self.folder_logic = folder_logic
        self.criteria_logic = criteria_logic
        self.score_label = score_label
        self.part_dict = part_dict
        self.main_window = main_window
        self.exam_grader = None
        self.individual_scores = {}
        self.show_details = show_details
        self.exam_type = exam_type
        self.gui_ref = gui_ref
    def run(self):
        if self.exam_type == "ITN":
            folder_path = self.folder_logic.folder_path
            criteria_path = self.criteria_logic.text().split(': ')[-1] if not self.show_details else self.criteria_logic.text().split(': ')[-1]
            try:
                self.exam_grader = ExamGrader(folder_path, criteria_path)
                with open(criteria_path, 'r') as f:
                    self.criteria = json.load(f)
                self.exam_grader.grade_exam()
                total_score = self.exam_grader.total_score
                section_scores = self.exam_grader.section_scores
                # Calculate the total score for part_number 3
                itn_part_3_score = sum([score for section, score in section_scores.items() if section.startswith('3')])
                for part_number, part_info in self.part_dict.items():
                    result_field = part_info['result_field']
                    result_label = part_info['result_label']
                    if part_number == 2:
                        result_label.setText(str(round(section_scores["2 Device Initialisation"], 2)))
                    elif part_number == 3:
                        result_label.setText(str(round(itn_part_3_score, 2)))
                    else:
                        score = float(result_field.text())
                        self.individual_scores[part_number] = score
                        result_label.setText(str(round(score, 2)))
                total_score += sum(self.individual_scores.values())
                self.score_label.setText(f'Score: {round(total_score, 2)}')
                self.main_window.update_score_box_style(total_score)
                if self.show_details:
                    show_details_logic = ShowDetailsLogic(self.exam_grader, self.individual_scores, criteria_path)
                    show_details_logic.run()
            except FileNotFoundError:
                error_message = f"Error: Please select an Exam Folder and Criteria File"
                QMessageBox.critical(None, "Error", error_message)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                QMessageBox.critical(None, "Error", error_message)
        elif self.exam_type == "SRWE":
            folder_path = self.folder_logic.folder_path
            criteria_path = self.criteria_logic.text().split(': ')[-1] if not self.show_details else self.criteria_logic.text().split(': ')[-1]
            try:
                self.exam_grader = ExamGrader(folder_path, criteria_path)
                with open(criteria_path, 'r') as f:
                    self.criteria = json.load(f)
                self.exam_grader.grade_exam()
                total_score = self.exam_grader.total_score
                section_scores = self.exam_grader.section_scores
                # Calculate the total score for part_number 1-3
                srwe_part_2_score = sum([score for section, score in section_scores.items() if section.startswith('2')])
                srwe_part_3_score = sum([score for section, score in section_scores.items() if section.startswith('3')])
                for part_number, part_info in self.part_dict.items():
                    result_field = part_info['result_field']
                    result_label = part_info['result_label']
                    if part_number == 1:
                        result_label.setText(str(round(section_scores["1 Initialise, Config"], 2)))
                    elif part_number == 2:
                        result_label.setText(str(round(srwe_part_2_score, 2)))
                    elif part_number == 3:
                        result_label.setText(str(round(srwe_part_3_score, 2)))
                    else:
                        score = float(result_field.text())
                        self.individual_scores[part_number] = score
                        result_label.setText(str(round(score, 2)))
                total_score += sum(self.individual_scores.values())
                self.score_label.setText(f'Score: {round(total_score, 2)}')
                self.main_window.update_score_box_style(total_score)
                if self.show_details:
                    show_details_logic = ShowDetailsLogic(self.exam_grader, self.individual_scores, criteria_path)
                    show_details_logic.run()
            except FileNotFoundError:
                error_message = f"Error: Please select an Exam Folder and Criteria File"
                QMessageBox.critical(None, "Error", error_message)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                QMessageBox.critical(None, "Error", error_message)
        elif self.exam_type == "ENSA":
            folder_path = self.folder_logic.folder_path
            criteria_path = self.criteria_logic.text().split(': ')[-1] if not self.show_details else self.criteria_logic.text().split(': ')[-1]
            try:
                self.exam_grader = ExamGrader(folder_path, criteria_path)
                with open(criteria_path, 'r') as f:
                    self.criteria = json.load(f)
                self.exam_grader.grade_exam()
                total_score = self.exam_grader.total_score
                section_scores = self.exam_grader.section_scores
                # Calculate the total score for part_number 1 - 4
                ensa_part_2_score = sum([score for section, score in section_scores.items() if section.startswith('2')])
                ensa_part_3_score = sum([score for section, score in section_scores.items() if section.startswith('3')])
                ensa_part_4_score = sum([score for section, score in section_scores.items() if section.startswith('4')])
                for part_number, part_info in self.part_dict.items():
                    result_field = part_info['result_field']
                    result_label = part_info['result_label']
                    if part_number == 1:
                        result_label.setText(str(round(section_scores["1 Initialise, Config"], 2)))
                    elif part_number == 2:
                        result_label.setText(str(round(ensa_part_2_score, 2)))
                    elif part_number == 3:
                        result_label.setText(str(round(ensa_part_3_score, 2)))
                    elif part_number == 4:
                        result_label.setText(str(round(ensa_part_4_score, 2))) 
                    else:
                        score = float(result_field.text())
                        self.individual_scores[part_number] = score
                        result_label.setText(str(round(score, 2)))
                total_score += sum(self.individual_scores.values())
                self.score_label.setText(f'Score: {round(total_score, 2)}')
                self.main_window.update_score_box_style(total_score)
                if self.show_details:
                    show_details_logic = ShowDetailsLogic(self.exam_grader, self.individual_scores, criteria_path)
                    show_details_logic.run()
            except FileNotFoundError:
                error_message = f"Error: Please select an Exam Folder and Criteria File"
                QMessageBox.critical(None, "Error", error_message)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                QMessageBox.critical(None, "Error", error_message)
    def update_exam_type(self, exam_type):
        self.exam_type = exam_type
