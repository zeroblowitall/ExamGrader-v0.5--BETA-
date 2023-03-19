import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from button_logic import FilesToCheckButtonLogic, CriteriaFileButtonLogic, GradeExamLogic, ResetLogic, QuitLogic
from custom_button import MyButton
from functools import partial


class ExamGraderGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Define the exam grader attributes
        self.criteria = {}
        self.exam_grader = None

    def init_ui(self):
        self.setup_window()
        self.setup_menu_area()
        self.setup_banner_label()
        self.setup_browse_buttons()
        self.setup_parts_area()
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

        # Load the icons from files / set the window icon and taskbar icon
        window_icon = QtGui.QIcon('images/icon.png')
        taskbar_icon = QtGui.QIcon('images/icon.png')
        self.setWindowIcon(window_icon)
        if sys.platform == 'win32':
            import ctypes
            myappid = 'spindley.examgrader.v0004' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            self.setWindowIcon(taskbar_icon)

    def setup_menu_area(self):
        self.menu_area = QtWidgets.QVBoxLayout()

        self.menu_area.setSpacing(0)
        self.menu_area.setContentsMargins(0, 0, 0, 0)

        # Add buttons for different exam types here
        ITN_button = MyButton('ITN', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', self)
        SRWE_button = MyButton('SRWE', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', self)
        ENSA_button = MyButton('ENSA', 'images/bigwhitebuttonSq.png', 'images/bigwhitehoverbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', 'images/bigwhitepressedbuttonSq.png', self)
        self.menu_area.addWidget(ITN_button)
        self.menu_area.addWidget(SRWE_button)
        self.menu_area.addWidget(ENSA_button)

        self.menu_area.addStretch(1)

    def setup_banner_label(self):
        # Create the banner label
        self.banner_label = QtWidgets.QLabel(self)
        self.banner_label.setPixmap(QtGui.QPixmap('images/banner.png'))

    def setup_grader_buttons_area(self):
        self.grade_exam_button = MyButton('Grade Files', 'images/biggreenbutton.png', 'images/biggreenhoverbutton.png', 'images/biggreenpressedbutton.png', 'images/biggreenpressedbutton.png', self)
        self.show_details_button = MyButton('Show Details...', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.grader_buttons_area = QtWidgets.QVBoxLayout()
        self.grader_buttons_area.addWidget(self.grade_exam_button)
        self.grader_buttons_area.addWidget(self.show_details_button)

    def setup_browse_buttons(self):
        # Create the browse folder and file buttons and labels
        self.browse_folder_button = MyButton('Select Folder', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.folder_path_label = QtWidgets.QLabel(self)
        self.folder_path_label.setStyleSheet('min-height: 120px; max-height: 120px;min-width: 300px;')
        self.browse_file_button = MyButton('Select Criteria', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.criteria_label = QtWidgets.QLabel(self)
        self.criteria_label.setStyleSheet('min-height: 120px; max-height: 120px;min-width: 300px;')

        # Create the browse folder and file layouts
        self.browse_button_layout = QtWidgets.QGridLayout()
        self.folder_box = QtWidgets.QHBoxLayout()
        self.folder_box.addWidget(self.folder_path_label)
        self.criteria_box = QtWidgets.QHBoxLayout()
        self.criteria_box.addWidget(self.criteria_label)
        self.browse_button_layout.addWidget(self.browse_folder_button, 1, 0)
        self.browse_button_layout.addLayout(self.folder_box, 1, 1)
        self.browse_button_layout.addWidget(self.browse_file_button, 2, 0)
        self.browse_button_layout.addLayout(self.criteria_box, 2, 1)

    def setup_parts_area(self):
        # Create the Section buttons Box on the right-hand side of the GUI
        self.parts_area = QtWidgets.QGroupBox(self)
        self.parts_area_layout = QtWidgets.QGridLayout(self.parts_area)
        self.part_dict = {}
        self.overall_score = 0
        max_values = [10, 10, 60, 10, 10]

        # Set a fixed height for the QGroupBox
        self.parts_area.setFixedHeight(400)
        #self.parts_area.setFixedWidth(500)

        for i in range(5):
            part_number = i + 1
            part_name = ''
            if part_number == 1:
                part_name = 'Subnetting'
            elif part_number == 2:
                part_name = 'Initialisation'
            elif part_number == 3:
                part_name = 'Device Config'
            elif part_number == 4:
                part_name = 'Testing'
            elif part_number == 5:
                part_name = 'Information'

            part_label = QtWidgets.QLabel(f'Section {part_number}: {part_name} ', self.parts_area)
            
            # Set the minimum height for each row
            row_height = 70  # Adjust this value to fit your needs
            self.parts_area_layout.setRowMinimumHeight(0, row_height)
            self.parts_area_layout.setRowMinimumHeight(1, row_height)
            self.parts_area_layout.setRowMinimumHeight(2, row_height)
            self.parts_area_layout.setRowMinimumHeight(3, row_height)
            self.parts_area_layout.setRowMinimumHeight(4, row_height)
            part_label.setStyleSheet('color: #B9BABD; font-size: 24px;')
            part_label.setFixedWidth(350)
            self.parts_area_layout.addWidget(part_label, i, 0)

            enter_result = QtWidgets.QLineEdit(self.parts_area)
            enter_result.setFixedWidth(80)
            enter_result.setText('0.0')  # Set default value to 0

            # Create a QDoubleValidator with the desired minimum, maximum, and decimal places
            max_value = max_values[i]
            print(max_values[i]) # Get the max value for the current QLineEdit from the list
            validator = QtGui.QDoubleValidator(0, max_value, 1)  # Adjust min, max, and decimals as needed
            enter_result.setValidator(validator)

            # Connect the textChanged signal to the on_text_changed method
            enter_result.editingFinished.connect(partial(self.on_editing_finished, max_value, enter_result))

            if part_number == 2:
                enter_result.setVisible(False)  # Hide input field for part 2/3
            elif part_number == 3:
                enter_result.setVisible(False)  # Hide input field for part 2/3
            self.parts_area_layout.addWidget(enter_result, i, 1)

            result_label = QtWidgets.QLabel('0.0', self.parts_area)
            result_label.setStyleSheet('color: #B9BABD;font-size: 24px;')
            result_label.setFixedWidth(50)
            self.parts_area_layout.addWidget(result_label, i, 3)

            self.part_dict[part_number] = {
                'name': part_name,
                'label': part_label,
                'result_field': enter_result,
                'result_label': result_label
            }

            # Set the stretch factor for all rows to be equal
            self.parts_area_layout.setRowStretch(i, 1)

        self.parts_area.setLayout(self.parts_area_layout)
        self.parts_area.setStyleSheet('QGroupBox{border: 2px solid #383C43; border-radius: 40px; padding: 5px;background-color: #383C43;}')

    def on_editing_finished(self, max_value, line_edit):
        try:
            text = line_edit.text()
            value = float(text)
            if value > max_value:
                line_edit.setText(str(max_value))
                QtWidgets.QMessageBox.warning(None, "Value Exceeded", f"The maximum allowed value is {max_value}. The value has been set to the maximum.")
            else:
                line_edit.setText(f'{value:.1f}')  # Display the value as a float with 1 decimal place
        except ValueError:
            pass


    def setup_score_box(self):
        # Create the Score box
        self.score_label = QtWidgets.QLabel('Score: 0.0', self)
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setFont(QtGui.QFont('Calibri', 12))

        # Set a fixed size for the score box
        self.score_label.setFixedSize(250, 68)
        self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px;font-size: 30px;")

    def update_score_box_style(self, score):
        if score >= 70.0:
            self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px; padding: 5px;background-color: green; color: black; font-size: 30px;")
        else:
            self.score_label.setStyleSheet("border: 5px solid #B9BABD; border-radius: 30px; padding: 5px;background-color: red; color: white; font-size: 30px;")

    def setup_system_buttons(self):
        # Create the system buttons and layouts
        self.reset_button = MyButton('Reset', 'images/bigwhitebutton.png', 'images/bigwhitehoverbutton.png', 'images/bigwhitepressedbutton.png', 'images/bigwhitepressedbutton.png', self)
        self.quit_button = MyButton('Quit', 'images/bigredbutton.png', 'images/bigredhoverbutton.png', 'images/bigredpressedbutton.png', 'images/bigredpressedbutton.png', self)
        self.system_button_layout = QtWidgets.QHBoxLayout()
        self.system_button_layout.addWidget(self.reset_button)
        self.system_button_layout.addWidget(self.quit_button)

    def setup_main_layout(self):
        # Create the main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.banner_label)
        content_layout = QtWidgets.QHBoxLayout()
        # Add the menu area on the left below the banner
        self.menu_widget = QtWidgets.QWidget()
        self.menu_widget.setLayout(self.menu_area)
        #self.menu_widget.setStyleSheet("background-color: gray;")
        content_layout.addWidget(self.menu_widget)
        # Create a layout for the main content
        main_content_layout = QtWidgets.QVBoxLayout()
        # Add the browse buttons area
        main_content_layout.addLayout(self.browse_button_layout)
        # Add the parts area
        main_content_layout.addWidget(self.parts_area)

        main_content_layout.addSpacing(40) # adjust the number to increase or decrease the space
        # Create a layout for the Grade Files, Show Details..., and Score elements
        grade_details_score_layout = QtWidgets.QHBoxLayout()
        # Add the Grade Exam button
        grade_details_score_layout.addWidget(self.grade_exam_button)
        # Add horizontal spacer between the buttons
        grade_details_score_layout.addSpacing(20)
        # Add the Show Details button
        grade_details_score_layout.addWidget(self.show_details_button)
        # Add horizontal spacer between the buttons and score
        grade_details_score_layout.addSpacing(20)
        # Add the Score label
        grade_details_score_layout.addWidget(self.score_label)
        # Add horizontal spacer to fill the remaining space
        grade_details_score_layout.addStretch(1)
        main_content_layout.addLayout(grade_details_score_layout)
        
        main_content_layout.addSpacing(40) # adjust the number to increase or decrease the space
        # Align the system buttons to the right of the window
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
        self.grade_exam_logic = GradeExamLogic(self.folder_logic, self.criteria_label, self.score_label, self.part_dict, self)
        self.details_button_logic = GradeExamLogic(self.folder_logic, self.criteria_label, self.score_label, self.part_dict, self, show_details=True)
        self.reset_logic = ResetLogic(self.folder_path_label, self.criteria_label, self.score_label, self.part_dict)
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
