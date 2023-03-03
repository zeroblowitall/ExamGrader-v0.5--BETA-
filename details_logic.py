from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout

class GradingDetailsDialog(QDialog):
    def __init__(self, criteria, exam_grader):
        super().__init__()
        self.setWindowTitle('Grading Details')
        self.setGeometry(100, 100, 800, 600)

        print('criteria:', criteria)
        print('exam_grader:', exam_grader)

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Question', 'Weight', 'Result'])

        # Add the data to the table
        for question, data in criteria.items():
            weight = data['weight']
            regex = data['regex']
            answer = data['answer']
            answer2 = data.get('answer2')

            result = exam_grader.get_question_result(question, regex, answer, answer2)
            item_question = QTableWidgetItem(question)
            item_weight = QTableWidgetItem(str(weight))
            item_result = QTableWidgetItem(str(result))
            item_result.setBackground('green' if result else 'red')

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, item_question)
            self.table_widget.setItem(row_position, 1, item_weight)
            self.table_widget.setItem(row_position, 2, item_result)

        # Create the layouts
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_widget)

        main_layout = QVBoxLayout()
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

        print('table_widget rowCount:', self.table_widget.rowCount())
        print('table_widget columnCount:', self.table_widget.columnCount())
