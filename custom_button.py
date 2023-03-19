from PyQt5 import QtWidgets, QtCore, QtGui

class MyButton(QtWidgets.QPushButton):
    def __init__(self, text, icon_path, hover_path, pressed_path, released_path, parent=None):
        super().__init__(parent)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('color: #44474E; font-size: 25px; font-family: Calibri; font-weight: bold')
        self.label.setText(text)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)

        # Set the button style sheet with the default icon path
        self.setStyleSheet('''
            QPushButton {
                border: none;
                background-image: url(%s);
                background-repeat: no-repeat;
                background-position: center;
            }
        ''' % icon_path)

        # Set the icon paths as attributes for later use
        self.icon_path = icon_path
        self.hover_path = hover_path
        self.pressed_path = pressed_path
        self.released_path = released_path

        # Set the size of the button to match the size of the background image
        pixmap = QtGui.QPixmap(icon_path)
        self.setFixedSize(pixmap.size())

        # Set the size of the label and position it in the center of the button
        label_size = self.label.sizeHint()
        self.label.resize(label_size)
        self.label.move(self.rect().center() - self.label.rect().center())

        # Connect the button events to their respective slots
        self.installEventFilter(self)

        # Change the cursor shape to a pointing hand
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            self.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-image: url(%s);
                    background-repeat: no-repeat;
                    background-position: center;
                }
            ''' % self.hover_path)
        elif event.type() == QtCore.QEvent.Leave:
            self.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-image: url(%s);
                    background-repeat: no-repeat;
                    background-position: center;
                }
            ''' % self.icon_path)
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            self.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-image: url(%s);
                    background-repeat: no-repeat;
                    background-position: center;
                }
            ''' % self.pressed_path)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-image: url(%s);
                    background-repeat: no-repeat;
                    background-position: center;
                }
            ''' % self.released_path)

        return super().eventFilter(obj, event)

