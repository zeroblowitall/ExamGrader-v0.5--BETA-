import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from button_logic import FilesToCheckButtonLogic, CriteriaFileButtonLogic, ResetLogic, QuitLogic
from grade_exam_logic import GradeExamLogic
from custom_button import MyButton
from exam_sections import update_parts_area

class ExamGraderGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.exam_type = "ITN"
        self.init_ui()
        self.criteria = {}
        self.exam_grader = None
    def init_ui(self):
        self.setup_window()
        self.setup_menu_area()
        self.setup_banner_label()
        self.setup_browse_buttons()
        self.parts_area = QtWidgets.QGroupBox(self)
        self.parts_area_layout = QtWidgets.QGridLayout(self.parts_area)
        update_parts_area("ITN", self)
        self.setup_grader_buttons_area()
        self.setup_score_box()
        self.setup_system_buttons()
        self.setup_main_layout()
        self.setup_button_logic()
        self.show()
    def setup_window(self):          
        self.setWindowTitle('Exam Grader')
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))
        self.setGeometry(100, 100, 1000,0)
        window_icon = QtGui.QIcon('images/icon.png')
        taskbar_icon = QtGui.QIcon('images/icon.png')
        self.setWindowIcon(window_icon)
        if sys.platform == 'win32':
            import ctypes
            myappid = 'spindley.examgrader.v0004'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            self.setWindowIcon(taskbar_icon)
    def setup_menu_area(self):
        self.menu_area = QtWidgets.QVBoxLayout()
        self.menu_area.setSpacing(0)
        self.menu_area.setContentsMargins(0, 0, 0, 0)
        self.ITN_button = MyButton('ITN', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhiteselectedbuttonSq.png', self)
        self.SRWE_button = MyButton('SRWE', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhiteselectedbuttonSq.png', self)
        self.ENSA_button = MyButton('ENSA', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhiteselectedbuttonSq.png', self)
        self.menu_area.addWidget(self.ITN_button)
        self.menu_area.addWidget(self.SRWE_button)
        self.menu_area.addWidget(self.ENSA_button)
        self.ITN_button.clicked.connect(lambda: self.set_exam_type_and_update_parts_area("ITN"))
        self.SRWE_button.clicked.connect(lambda: self.set_exam_type_and_update_parts_area("SRWE"))
        self.ENSA_button.clicked.connect(lambda: self.set_exam_type_and_update_parts_area("ENSA"))
        self.menu_area.addStretch(1)
    def set_exam_type_and_update_parts_area(self, exam_type):
        self.exam_type = exam_type
        self.grade_exam_logic.update_exam_type(exam_type)
        update_parts_area(exam_type, self)
        # Highlight the appropriate button
        self.ITN_button.set_highlighted(self.exam_type == "ITN")
        self.SRWE_button.set_highlighted(self.exam_type == "SRWE")
        self.ENSA_button.set_highlighted(self.exam_type == "ENSA")
        self.details_button_logic.update_exam_type(exam_type)
        self.grade_exam_logic.part_dict = self.part_dict
    def setup_banner_label(self): # Create the banner label
        self.banner_label = QtWidgets.QLabel(self)
        self.banner_label.setPixmap(QtGui.QPixmap('images/banner.png'))
    def setup_grader_buttons_area(self):
        self.grade_exam_button = MyButton('Grade Files', 'images/biggreenbutton.png', 'images/biggreenhoverbutton.png', 'images/biggreenpressedbutton.png', 'images/biggreenpressedbutton.png', self)
        self.show_details_button = MyButton('Show Details...', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.grader_buttons_area = QtWidgets.QVBoxLayout()
        self.grader_buttons_area.addWidget(self.grade_exam_button)
        self.grader_buttons_area.addWidget(self.show_details_button)
    def setup_browse_buttons(self): # Create the browse folder and file buttons and labels
        self.browse_folder_button = MyButton('Select Folder', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.folder_path_label = QtWidgets.QLabel(self)
        self.folder_path_label.setStyleSheet('min-height: 120px; max-height: 120px;min-width: 300px;')
        self.browse_file_button = MyButton('Select Criteria', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.criteria_label = QtWidgets.QLabel(self)
        self.criteria_label.setStyleSheet('min-height: 120px; max-height: 120px;min-width: 300px;')
        self.browse_button_layout = QtWidgets.QGridLayout()
        self.folder_box = QtWidgets.QHBoxLayout()
        self.folder_box.addWidget(self.folder_path_label)
        self.criteria_box = QtWidgets.QHBoxLayout()
        self.criteria_box.addWidget(self.criteria_label)
        self.browse_button_layout.addWidget(self.browse_folder_button, 1, 0)
        self.browse_button_layout.addLayout(self.folder_box, 1, 1)
        self.browse_button_layout.addWidget(self.browse_file_button, 2, 0)
        self.browse_button_layout.addLayout(self.criteria_box, 2, 1)
    def on_editing_finished(self, result_field):
        result = float(result_field.text())
        result_field.setText(f'{result:.1f}')
        part_number = None
        for key, part_info in self.part_dict.items():
            if part_info['result_field'] == result_field:
                part_number = key
                break
        if part_number is not None:
            self.part_dict[part_number]['result_label'].setText(f'{result:.1f}')
    def setup_score_box(self): # Create the Score box
        self.score_label = QtWidgets.QLabel('Score: 0.0', self)
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setFont(QtGui.QFont('Calibri', 12))
        self.score_label.setFixedSize(250, 68)
        self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px;font-size: 30px;")
    def update_score_box_style(self, score):
        if score >= 70.0:
            self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px; padding: 5px;background-color: green; color: black; font-size: 30px;")
        else:
            self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px; padding: 5px;background-color: red; color: white; font-size: 30px;")
    def setup_system_buttons(self): # Create the system buttons and layouts
        self.reset_button = MyButton('Reset', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.quit_button = MyButton('Quit', 'images/bigredbutton.png', 'images/bigredhoverbutton.png', 'images/bigredpressedbutton.png', 'images/bigredpressedbutton.png', self)
        self.system_button_layout = QtWidgets.QHBoxLayout()
        self.system_button_layout.addWidget(self.reset_button)
        self.system_button_layout.addWidget(self.quit_button)
    def setup_main_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.banner_label)
        content_layout = QtWidgets.QHBoxLayout()
        self.menu_widget = QtWidgets.QWidget()
        self.menu_widget.setLayout(self.menu_area)
        content_layout.addWidget(self.menu_widget)
        main_content_layout = QtWidgets.QVBoxLayout()
        main_content_layout.addLayout(self.browse_button_layout)
        main_content_layout.addWidget(self.parts_area)
        main_content_layout.addSpacing(40)
        grade_details_score_layout = QtWidgets.QHBoxLayout()
        grade_details_score_layout.addWidget(self.grade_exam_button)
        grade_details_score_layout.addSpacing(20)
        grade_details_score_layout.addWidget(self.show_details_button)
        grade_details_score_layout.addSpacing(20)
        grade_details_score_layout.addWidget(self.score_label)
        grade_details_score_layout.addStretch(1)
        main_content_layout.addLayout(grade_details_score_layout)
        system_button_row = QtWidgets.QHBoxLayout()
        system_button_row.addStretch()
        system_button_row.addLayout(self.system_button_layout)
        main_content_layout.addLayout(system_button_row)
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        self.show()
    def setup_button_logic(self):
        # Create the button logic instances
        self.folder_logic = FilesToCheckButtonLogic(self.folder_path_label)
        self.browse_file_logic = CriteriaFileButtonLogic(self.criteria_label)
        self.grade_exam_logic = GradeExamLogic(self.folder_logic, self.criteria_label, self.score_label, self.part_dict, self, self.exam_type, self)
        self.details_button_logic = GradeExamLogic(self.folder_logic, self.criteria_label, self.score_label, self.part_dict, self, self.exam_type, self, show_details=True)
        self.reset_logic = ResetLogic(self.folder_path_label, self.criteria_label, self.score_label, self.part_dict, self.folder_logic, self.browse_file_logic, self.grade_exam_logic, self)
        self.quit_logic = QuitLogic()
        #Connect the button signals to their slots
        self.browse_folder_button.clicked.connect(self.folder_logic.run)
        self.browse_file_button.clicked.connect(self.browse_file_logic.run)
        self.grade_exam_button.clicked.connect(self.grade_exam_logic.run)
        self.show_details_button.clicked.connect(self.details_button_logic.run)
        self.reset_button.clicked.connect(self.reset_logic.run)
        self.quit_button.clicked.connect(self.quit_logic.run)
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ExamGraderGUI()
    sys.exit(app.exec_())
