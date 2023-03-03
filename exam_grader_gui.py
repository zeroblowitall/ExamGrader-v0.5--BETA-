from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from button_logic import FilesToCheckButtonLogic, CriteriaFileButtonLogic, GradeExamLogic, ShowDetailsLogic, ResetLogic, QuitLogic
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

class ExamGraderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Exam Grader')
        self.setGeometry(100, 100, 800,0)
        # Load the icon from a file
        app_icon = QIcon('SpindleyLogo.png')

        # Set the application icon
        QApplication.setWindowIcon(app_icon)

        # Create the browse folder button and label
        self.browse_folder_button = QPushButton('Select Folder', self)
        self.browse_folder_button.setFixedWidth(200)
        self.browse_folder_button.setFixedHeight(100)
        self.folder_path_label = QLabel(self)

        # Create the browse file button and label
        self.browse_file_button = QPushButton('Select Criteria', self)
        self.browse_file_button.setFixedWidth(200)
        self.browse_file_button.setFixedHeight(100)
        self.criteria_file_label = QLabel(self)

        # Create the Score box
        self.score_box = QGridLayout()
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont('Calibri', 11))
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor('red'))
        self.score_label.setPalette(palette)
        self.score_label.setAutoFillBackground(True)
        self.score_label.setStyleSheet("border: 5px solid gray")
        self.score_box.addWidget(self.score_label, 0, 0, 2, 1)
        self.grade_exam_button = QPushButton('Grade Files', self)
        self.grade_exam_button.setFixedWidth(300)
        self.score_box.addWidget(self.grade_exam_button, 0, 1, 1, 1)
        self.show_details_button = QPushButton('Show Details...', self)
        self.show_details_button.setFixedWidth(300)
        self.score_box.addWidget(self.show_details_button, 1, 1, 1, 1)

        # Create the Reset and Quit buttons
        self.reset_button = QPushButton('Reset', self)
        self.quit_button = QPushButton('Quit', self)

        # Define the exam grader attributes
        self.criteria = {}
        self.exam_grader = None

        # Create the button logic instances
        self.browse_folder_logic = FilesToCheckButtonLogic(self.folder_path_label)
        self.browse_file_logic = CriteriaFileButtonLogic(self.criteria_file_label)
        self.reset_logic = ResetLogic(self.folder_path_label, self.criteria_file_label, self.score_label)
        self.quit_logic = QuitLogic()
        self.grade_exam_logic = GradeExamLogic(self.folder_path_label, self.criteria_file_label, self.score_label)
        self.show_details_logic = ShowDetailsLogic(self.get_criteria, self.get_exam_grader)
     

        #Connect the button signals to their slots
        self.browse_folder_button.clicked.connect(self.browse_folder_logic.run)
        self.browse_file_button.clicked.connect(self.browse_file_logic.run)
        self.reset_button.clicked.connect(self.reset_logic.run)
        self.quit_button.clicked.connect(self.quit_logic.run)
        self.grade_exam_button.clicked.connect(self.grade_exam_logic.run)
        self.show_details_button.clicked.connect(self.show_details_logic.run)

        # Create the layouts
        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.browse_folder_button)
        button_layout1.addWidget(self.folder_path_label)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.browse_file_button)
        button_layout2.addWidget(self.criteria_file_label)
        button_layout2.addWidget(QLabel())  # To fill up the remaining space

        button_layout6 = QHBoxLayout()
        button_layout6.addWidget(self.reset_button)
        button_layout6.addWidget(self.quit_button)

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)
        main_layout.addLayout(self.score_box)
        main_layout.addWidget(self.reset_button)
        main_layout.addWidget(self.quit_button)

        self.setLayout(main_layout)
        self.show()

    def update_folder_path_label(self, folder_path):
        if folder_path:
            # Show the last two folders of the selected folder path
            folder_path_display = "/".join(folder_path.split("/")[0:])
            self.folder_path_label.setText(f"Selected Folder: {folder_path_display}")

    def update_criteria_file_label(self, file_path):
        if file_path:
            # Show the last two folders and the file name of the selected file path
            criteria_file_display = "/".join(file_path.split("/")[-3:])
            self.criteria_file_label.setText(f"Selected Criteria File: {criteria_file_display}")
    
    def get_criteria(self):
        return self.criteria

    def get_exam_grader(self):
        return self.exam_grader

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ExamGraderGUI()
    sys.exit(app.exec_())
