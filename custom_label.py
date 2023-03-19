from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class FileListLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("""
            FileListLabel {
                border: 2px solid black;
                background-color: white;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def update_content(self, folder_name, file_list):
        content = f'<b>{folder_name}</b><br>'
        content += '<br>'.join(file_list)
        self.setText(content)
        self.setAlignment(Qt.AlignTop)