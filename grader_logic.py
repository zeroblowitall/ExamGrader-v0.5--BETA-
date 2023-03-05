import json
import re, os

class ExamGrader:
    def __init__(self, exam_folder_path, criteria_file_path):
        self.exam_folder_path = exam_folder_path
        self.criteria_file_path = criteria_file_path
        self.criteria = {}
        self.results_dict = None
        self.total_score = 0

        self.load_criteria()

    def load_criteria(self):
        with open(self.criteria_file_path, 'r') as f:
            self.criteria = json.load(f)

    def grade_exam(self):
        exam_files = [f for f in os.listdir(self.exam_folder_path) if f.endswith('.txt')]

        self.results_dict = {}
        for exam_file in exam_files:
            with open(os.path.join(self.exam_folder_path, exam_file), 'r') as f:
                exam_file_contents = f.read()

            print(f'Grading {exam_file}...')
            self.results_dict[exam_file] = {}
            found_strings = set()
            for key in self.criteria.keys():
                if self.criteria[key]['device'] not in exam_file:
                    continue
                if self.criteria[key]['regex']:
                    if re.search(self.criteria[key]['answer'], exam_file_contents, re.IGNORECASE):
                        if key not in found_strings:
                            self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': self.criteria[key]['weight']}
                            self.total_score += self.criteria[key]['weight']
                            found_strings.add(key)
                        else:
                            self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': 0}
                    else:
                        self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': 0}
                else:
                    if self.criteria[key]['answer'].lower() in exam_file_contents.lower():
                        if key not in found_strings:
                            self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': self.criteria[key]['weight']}
                            self.total_score += self.criteria[key]['weight']
                            found_strings.add(key)
                        else:
                            self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': 0}
                    else:
                        self.results_dict[exam_file][key] = {'answer': self.criteria[key]['answer'], 'weight': self.criteria[key]['weight'], 'points': 0}

    def get_results_dict(self):
        return self.results_dict
