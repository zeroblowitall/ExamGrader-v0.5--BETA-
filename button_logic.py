import os, sys
from PyQt5.QtWidgets import QStyledItemDelegate, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtCore import Qt
import exam_sections
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('images/icon.png'))
class ButtonLogic:
    def __init__(self, label):
        self.label = label
        self.folder_path = ""
        self.criteria_path = None
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
            self.folder_path = folder_path
            folder_name = os.path.basename(folder_path)
            files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            content = f'<b>{folder_name}</b><br>'
            content += ', '.join(files_in_folder)
            self.label.setText(content)
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
class CriteriaFileButtonLogic(ButtonLogic):
    def run(self):
        super().run()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Criteria File", "", "JSON Files (*.json)", options=options
        )
        if file_path:
            self.criteria_path = file_path
            self.label.setText(f"{os.path.basename(file_path)}")
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
class ResetLogic:
    def __init__(self, folder_label, criteria_label, score_label, part_dict, folder_logic, criteria_file_logic, grade_exam_logic, exam_grader_gui):
        self.folder_label = folder_label
        self.criteria_label = criteria_label
        self.score_label = score_label
        self.part_dict = part_dict
        self.folder_logic = folder_logic
        self.criteria_file_logic = criteria_file_logic
        self.grade_exam_logic = grade_exam_logic
        self.exam_grader_gui = exam_grader_gui

    def run(self):
        self.folder_label.clear()
        self.criteria_label.clear()
        self.score_label.setText('Score: 0.0')
        for part_number, part_info in self.part_dict.items():
            part_info['result_field'].setText('0.0')
            part_info['result_label'].setText('0.0')
        self.folder_logic.folder_path = ''
        self.criteria_file_logic.criteria_path = ''
        self.grade_exam_logic.exam_grader = None
        self.exam_grader_gui.set_exam_type_and_update_parts_area("ITN")
class QuitLogic:
    def __init__(self):
        None
    def run(self):
        choice = QMessageBox.question(None, "Quit", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QApplication.quit()
class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # Check if the current index is a section header
        if index.data() and index.data().startswith('Section') and index.column() == 0:
            # Set the pen to white color with 2px width
            pen = QPen(Qt.white, 2)
            painter.setPen(pen)
            # Draw a rectangle border around the section header cell
            painter.drawRect(option.rect)
            