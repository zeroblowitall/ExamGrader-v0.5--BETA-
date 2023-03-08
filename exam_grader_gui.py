from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QMainWindow
from button_logic import FilesToCheckButtonLogic, CriteriaFileButtonLogic, GradeExamLogic, ResetLogic, QuitLogic,ViewDetailsLogic
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt

class ExamGraderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Exam Grader')
        self.setWindowIcon(QIcon('images/icon1.png'))
        self.setGeometry(100, 100, 800,0)

        # Load the icons from files
        window_icon = QIcon('images/icon1.png')
        taskbar_icon = QIcon('images/icon1.png')

        # Set the window icon
        self.setWindowIcon(window_icon)

        # Set the taskbar icon
        if sys.platform == 'win32':
            import ctypes
            myappid = 'spindley.examgrader.v0004' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            self.setWindowIcon(taskbar_icon)

        # Create the banner label
        banner_label = QLabel(self)
        banner_label.setPixmap(QPixmap('images/banner5.png'))

        # TODO Set the background
        # self.setStyleSheet("background-image: url('images/bg.jpg');")

        # Define the exam grader attributes
        self.criteria = {}
        self.exam_grader = None

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

        # Create the button logic instances
        self.browse_folder_logic = FilesToCheckButtonLogic(self.folder_path_label)
        self.browse_file_logic = CriteriaFileButtonLogic(self.criteria_file_label)
        self.grade_exam_logic = GradeExamLogic(self.folder_path_label, self.criteria_file_label, self.score_label)
        self.details_button_logic = ViewDetailsLogic(self.folder_path_label, self.criteria_file_label, self.score_label)
        self.reset_logic = ResetLogic(self.folder_path_label, self.criteria_file_label, self.score_label)
        self.quit_logic = QuitLogic()
    
        #Connect the button signals to their slots
        self.browse_folder_button.clicked.connect(self.browse_folder_logic.run)
        self.browse_file_button.clicked.connect(self.browse_file_logic.run)
        self.grade_exam_button.clicked.connect(self.grade_exam_logic.run)
        self.show_details_button.clicked.connect(self.details_button_logic.run)
        self.reset_button.clicked.connect(self.reset_logic.run)
        self.quit_button.clicked.connect(self.quit_logic.run)

        # Create the layouts
        browse_button_layout = QHBoxLayout()
        browse_button_layout.addWidget(self.browse_folder_button)
        browse_button_layout.addWidget(self.folder_path_label)

        file_button_layout = QHBoxLayout()
        file_button_layout.addWidget(self.browse_file_button)
        file_button_layout.addWidget(self.criteria_file_label)

        button_layout6 = QHBoxLayout()
        button_layout6.addWidget(self.reset_button)
        button_layout6.addWidget(self.quit_button)

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(banner_label)
        main_layout.addLayout(browse_button_layout)
        main_layout.addLayout(file_button_layout)
        main_layout.addLayout(self.score_box)
        main_layout.addWidget(self.reset_button)
        main_layout.addWidget(self.quit_button)

        self.setLayout(main_layout)
        self.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ExamGraderGUI()
    sys.exit(app.exec_())
