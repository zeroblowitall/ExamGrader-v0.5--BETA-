import json
import re

class ExamGrader:
    def __init__(self, exam_folder_path, criteria_file_path):
        self.exam_folder_path = exam_folder_path
        self.criteria_file_path = criteria_file_path
        self.criteria = {}
        self.total_score = 0

        self.load_criteria()
    
    def load_criteria(self):
        with open(self.criteria_file_path, 'r') as f:
            self.criteria = json.load(f)

    def grade_exam(self):
        exam_files = ['R1config.txt', 'S1config.txt']

        for exam_file in exam_files:
            with open(f"{self.exam_folder_path}/{exam_file}", 'r') as f:
                exam_file_contents = f.read()

            print(f'Grading {exam_file}...')
            for key in self.criteria.keys():
                if self.criteria[key]['regex']:
                    if re.search(self.criteria[key]['answer'], exam_file_contents, re.IGNORECASE):
                        self.total_score += self.criteria[key]['weight']
                        print(f"+{self.criteria[key]['weight']} points: {key}")
                    else:
                        print(f"0 points: {key}")
                elif key == "IPv4 address":
                    # Check the IP address based on the file being graded
                    if exam_file == 'R1config.txt' and self.criteria[key]['answer'].lower() in exam_file_contents.lower():
                        self.total_score += self.criteria[key]['weight']
                        print(f"+{self.criteria[key]['weight']} points: {key}")
                    elif exam_file == 'S1config.txt' and self.criteria[key]['answer2'].lower() in exam_file_contents.lower():
                        self.total_score += self.criteria[key]['weight']
                        print(f"+{self.criteria[key]['weight']} points: {key}")
                    else:
                        print(f"0 points: {key}")
                else:
                    if self.criteria[key]['answer'].lower() in exam_file_contents.lower():
                        self.total_score += self.criteria[key]['weight']
                        print(f"+{self.criteria[key]['weight']} points: {key}")
                    else:
                        print(f"0 points: {key}")

        # Print the total score
        print(f'Total Score: {self.total_score}')

