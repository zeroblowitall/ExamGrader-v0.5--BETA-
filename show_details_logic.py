import json, csv
from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QLabel
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from datetime import datetime
import button_logic

class ShowDetailsLogic:
    def __init__(self, exam_grader, individual_scores, criteria_file_path):
        self.results_dict = exam_grader.get_results_dict()
        self.individual_scores = individual_scores
        self.criteria_file_path = criteria_file_path
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
            total_score_label.setStyleSheet('font-size:30px;')
            # Create a table to display the exam details
            table = QTableWidget()
            table.setItemDelegate(button_logic.CustomItemDelegate())
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(['Device', 'Question', 'Result', 'Score', 'Weight'])
            # Read the criteria sections from the criteria file
            with open(self.criteria_file_path) as f:
                criteria_dict = json.load(f)
            sections = {}
            for key, value in criteria_dict.items():
                section = value.get('section', 'Default')
                if section not in sections:
                    sections[section] = []
                sections[section].append(key)
            # Add the manually entered scores to the total score
            total_score = sum(self.individual_scores.values())
            # Add the manually entered part scores to the table
            part_rows = {}
            for part_num, part_score in self.individual_scores.items():
                if part_num != 2:  # Skip section 2 (Device Initialization)
                    section_name = f'Section {part_num}'
                    if section_name not in part_rows:
                        part_rows[section_name] = []
                    part_rows[section_name].append((part_num, part_score))
            # Add the rows for Part 1
            part_rows_list = part_rows.get('Section 1', [])
            if part_rows_list:
                table.insertRow(table.rowCount())
                section_item = QTableWidgetItem(f'Section 1 Subnetting.     Score: {round(sum([row[1] for row in part_rows_list]), 2)}')
                section_item.setFlags(Qt.NoItemFlags)
                section_item.setBackground(QColor('lightgray'))
                section_item.setForeground(QColor('black'))
                table.setItem(table.rowCount() - 1, 0, section_item)
                table.setSpan(table.rowCount() - 1, 0, 1, table.columnCount())
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
            for section_name, section_keys in sections.items():
                section_rows_list = []
                section_total_score = 0
                for row in section_rows.get(section_name, []):
                    section_rows_list.append(row)
                    section_total_score += row[3]  # Add up the score for each row in this section
                if section_rows_list:
                    # Add the section name and total score row
                    table.insertRow(table.rowCount())
                    section_item = QTableWidgetItem(f'Section {section_name}.     Score: {round(section_total_score, 2)}')
                    section_item.setFlags(Qt.NoItemFlags)
                    section_item.setBackground(QColor('lightgray'))
                    section_item.setForeground(QColor('black'))
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
                                    table.item(table.rowCount() - 1, j).setBackground(QColor('#90CAC7'))
                                else:
                                    table.item(table.rowCount() - 1, j).setBackground(QColor('#B26D70'))
                total_score += section_total_score # Add the section score to the total score
            # Add the rows for Part 4 and 5
            for part_num in [4, 5]:
                part_rows_list = part_rows.get(f'Section {part_num}', [])
                section_name_list = ["Testing","Information"]
                if part_rows_list:
                    table.insertRow(table.rowCount())
                    if part_num == 4:
                        section_item = QTableWidgetItem(f'Section {part_num} {section_name_list[0]}.     Score: {round(sum([row[1] for row in part_rows_list]), 2)}')
                    elif part_num == 5:
                        section_item = QTableWidgetItem(f'Section {part_num} {section_name_list[1]}.     Score: {round(sum([row[1] for row in part_rows_list]), 2)}')
                    section_item.setFlags(Qt.NoItemFlags)
                    section_item.setBackground(QColor('lightgray'))
                    section_item.setForeground(QColor('black'))
                    table.setItem(table.rowCount() - 1, 0, section_item)
                    table.setSpan(table.rowCount() - 1, 0, 1, table.columnCount())
            # Calculate pass/fail status
            pass_threshold = 70.0
            pass_status = 'PASS' if total_score >= pass_threshold else 'FAIL'
            if pass_status == 'PASS':
                total_score_label.setText(f'Score: {round(total_score, 2)} - Pass')
                total_score_groupbox.setStyleSheet('background-color: #90CAC7')
            else:
                total_score_label.setText(f'Score: {round(total_score, 2)} - Fail')
                total_score_groupbox.setStyleSheet('background-color: #B26D70')
            # Add the total score label to the total score groupbox
            total_score_groupbox_layout = QHBoxLayout()
            total_score_groupbox_layout.addWidget(total_score_label)
            total_score_groupbox.setLayout(total_score_groupbox_layout)
            table.resizeColumnsToContents()
            # Calculate the width of each column
            column_widths = [table.columnWidth(i) for i in range(table.columnCount())]
            table_width = sum(column_widths) # Calculate the total width of the table
            layout = QVBoxLayout()
            layout.addWidget(total_score_groupbox)
            layout.addWidget(table)
            table_window.setLayout(layout)
            button_box = QHBoxLayout()
            save_button = QPushButton('Save')
            close_button = QPushButton('Close')            
            button_box.addWidget(save_button)
            button_box.addWidget(close_button)
            layout.addLayout(button_box)
            close_button.clicked.connect(table_window.close)
            save_button.clicked.connect(lambda: self.save_to_csv(section_rows))
            main_window = QApplication.activeWindow()
            main_window_pos = main_window.pos()
            main_window_size = main_window.size()
            table_window.move(main_window_pos.x() + main_window_size.width(), main_window_pos.y())
            min_size = QSize(table_width + 150, 1000)
            table_window.setMinimumSize(min_size)
            table_window.exec_()
        else:
            print('ExamGrader instance not found.')
    def save_to_csv(self, section_rows):
        # Get the current timestamp for the filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"exam_results_{timestamp}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Section', 'Device', 'Question', 'Result', 'Score', 'Weight'])
            for section_name, rows in section_rows.items():
                for row in rows:
                    writer.writerow([section_name] + list(row))
        QMessageBox.information(None, 'Save Results', f'The exam results have been saved to "{filename}".')