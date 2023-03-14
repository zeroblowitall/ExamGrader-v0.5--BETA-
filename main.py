import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from button_logic import FilesToCheckButtonLogic, CriteriaFileButtonLogic, GradeExamLogic, ResetLogic, QuitLogic,ViewDetailsLogic
from custom_button import MyButton
class ExamGraderGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Exam Grader')
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))
        self.setGeometry(100, 100, 1000,0)

        # Load the icons from files / set the window icon and taskbar icon
        window_icon = QtGui.QIcon('images/icon.png')
        taskbar_icon = QtGui.QIcon('images/icon.png')
        self.setWindowIcon(window_icon)
        if sys.platform == 'win32':
            import ctypes
            myappid = 'spindley.examgrader.v0004' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            self.setWindowIcon(taskbar_icon)

        # Create the banner label
        banner_label = QtWidgets.QLabel(self)
        banner_label.setPixmap(QtGui.QPixmap('images/banner.png'))

        # Define the exam grader attributes
        self.criteria = {}
        self.exam_grader = None

        # Create the browse folder and file buttons and labels
        self.browse_folder_button = MyButton('Select Folder', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.folder_path_label = QtWidgets.QLabel(self)
        self.folder_path_label.setStyleSheet('color: #44474E; font-size: 20px;')
        self.browse_file_button = MyButton('Select Criteria', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.criteria_file_label = QtWidgets.QLabel(self)
        self.criteria_file_label.setStyleSheet('color: #44474E; font-size: 20px;')
        # Create the browse folder and file layouts
        browse_button_layout = QtWidgets.QGridLayout()
        browse_button_layout.addWidget(self.browse_folder_button, 1, 0)
        browse_button_layout.addWidget(self.folder_path_label, 2, 0)
        browse_button_layout.addWidget(self.browse_file_button, 3, 0)
        browse_button_layout.addWidget(self.criteria_file_label, 4, 0)

        # Create the group of buttons and labels on the right-hand side of the GUI
        parts_area = QtWidgets.QGroupBox(self)
        parts_area_layout = QtWidgets.QGridLayout(parts_area)
        part_dict = {}
        self.overall_score = 0

        for i in range(5):
            part_number = i + 1
            part_name = ''
            if part_number == 1:
                part_name = 'Subnetting'
            elif part_number == 2:
                part_name = 'Init & Config'
            elif part_number == 3:
                continue  # This part is merged with part 2
            elif part_number == 4:
                part_name = 'Testing'
            elif part_number == 5:
                part_name = 'Information'

            if part_number == 2:
                part_label = QtWidgets.QLabel(f'Part 2 & 3: {part_name}. ', parts_area)
            else:
                part_label = QtWidgets.QLabel(f'Part {part_number}: {part_name}. ', parts_area)
            part_label.setStyleSheet('color: #B9BABD; font-size: 24px;')
            part_label.setFixedWidth(350)
            parts_area_layout.addWidget(part_label, i, 0)

            enter_result = QtWidgets.QLineEdit(parts_area)
            enter_result.setFixedWidth(80)
            enter_result.setText('0.0')  # Set default value to 0
            if part_number == 2:
                enter_result.setVisible(False)  # Hide input field for part 2/3
            parts_area_layout.addWidget(enter_result, i, 1)

            result_label = QtWidgets.QLabel('0.0', parts_area)
            result_label.setStyleSheet('color: #B9BABD;font-size: 24px;')
            result_label.setFixedWidth(50)
            parts_area_layout.addWidget(result_label, i, 3)

            part_dict[part_number] = {
                'name': part_name,
                'label': part_label,
                'result_field': enter_result,
                'result_label': result_label
            }

        parts_area.setLayout(parts_area_layout)
        parts_area.setStyleSheet('QGroupBox{border: 2px solid gray; border-radius: 40px; padding: 5px;background-color: #383C43;}')

        # Create the Score box
        self.score_box = QtWidgets.QGridLayout()
        self.score_label = QtWidgets.QLabel('Score: 0.0', self)
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setFont(QtGui.QFont('Calibri', 12))
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor('red'))
        self.score_label.setPalette(palette)
        self.grade_exam_button = MyButton('Grade Files', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.show_details_button = MyButton('Show Details...', 'images/biggreenbutton.png', 'images/biggreenhoverbutton.png', 'images/biggreenpressedbutton.png', 'images/biggreenpressedbutton.png', self)
        self.score_box.addWidget(self.score_label, 0, 2, 0, 1) # two rows, one column
        self.score_label.setStyleSheet("border: 5px solid gray; border-radius: 30px;font-size: 30px;")
        self.score_box.addWidget(self.grade_exam_button, 0, 0, 1, 2)
        self.score_box.addWidget(self.show_details_button, 0, 1, 1, 2)

        # Create the system buttons and layouts
        self.reset_button = MyButton('Reset', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.quit_button = MyButton('Quit', 'images/bigredbutton.png', 'images/bigredhoverbutton.png', 'images/bigredpressedbutton.png', 'images/bigredpressedbutton.png', self)
        system_button_layout = QtWidgets.QHBoxLayout()
        system_button_layout.addWidget(self.reset_button)
        system_button_layout.addWidget(self.quit_button)

        # Create the main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(banner_label)

        # Create a layout for the top row of the GUI
        top_row_layout = QtWidgets.QHBoxLayout()
        top_row_layout.addLayout(browse_button_layout)
        top_row_layout.addWidget(parts_area)
        main_layout.addLayout(top_row_layout)

        main_layout.addLayout(self.score_box)
        main_layout.addLayout(system_button_layout)

        self.setLayout(main_layout)
        self.show()

        # Create the button logic instances
        self.browse_folder_logic = FilesToCheckButtonLogic(self.folder_path_label)
        self.browse_file_logic = CriteriaFileButtonLogic(self.criteria_file_label)
        self.grade_exam_logic = GradeExamLogic(self.folder_path_label, self.criteria_file_label, self.score_label, part_dict)
        self.details_button_logic = ViewDetailsLogic(self.folder_path_label, self.criteria_file_label, self.score_label, part_dict)
        self.reset_logic = ResetLogic(self.folder_path_label, self.criteria_file_label, self.score_label, part_dict)
        self.quit_logic = QuitLogic()
        #Connect the button signals to their slots
        self.browse_folder_button.clicked.connect(self.browse_folder_logic.run)
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
