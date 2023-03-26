from PyQt5 import QtWidgets, QtGui
from functools import partial

def update_parts_area(exam_type, gui_ref):
    # Clear the existing parts_area_layout
    for i in reversed(range(gui_ref.parts_area_layout.count())): 
        gui_ref.parts_area_layout.itemAt(i).widget().setParent(None)
    gui_ref.part_dict = {}
    gui_ref.overall_score = 0
    max_values = {
        "ITN": [10, 10, 60, 10, 10],
        "SRWE": [45, 30, 20, 5, 5],
        "ENSA": [45, 30, 20, 5, 5],
    }
    sections = {
        "ITN": [
            "Subnetting",
            "Initialisation",
            "Device Config",
            "Testing",
            "Information",
        ],
        "SRWE": [
            "Initialise, Config",
            "VLANs, Trunks, Eth.",
            "Routing, DHCP",
            "Testing",
            "N/A",
        ],
        "ENSA": [
            "Initialise, Config",
            "OSPFv2",
            "Optimise OSPFv2",
            "ACLs, NAT, Backup",
            "Testing",
        ],
    }
    num_sections = len(sections[exam_type])
    manual_input_sections = {
        "ITN": [True, False, False, True, True],
        "SRWE": [False, False, False, True, False],
        "ENSA": [False, False, False, False, True],
    }
    for i in range(num_sections):
        part_number = i + 1
        part_name = sections[exam_type][i]
        part_label = QtWidgets.QLabel(f'Section {part_number}: {part_name} ', gui_ref.parts_area)
        row_height = 70  # Adjust this value to fit your needs
        gui_ref.parts_area_layout.setRowMinimumHeight(0, row_height)
        gui_ref.parts_area_layout.setRowMinimumHeight(1, row_height)
        gui_ref.parts_area_layout.setRowMinimumHeight(2, row_height)
        gui_ref.parts_area_layout.setRowMinimumHeight(3, row_height)
        gui_ref.parts_area_layout.setRowMinimumHeight(4, row_height)
        part_label.setStyleSheet('color: #B9BABD; font-size: 24px;')
        part_label.setFixedWidth(350)
        gui_ref.parts_area_layout.addWidget(part_label, i, 0)
        enter_result = QtWidgets.QLineEdit(gui_ref.parts_area)
        enter_result.setFixedWidth(80)
        enter_result.setText('0.0') 
        # Create a QDoubleValidator with the desired minimum, maximum, and decimal places
        max_value = max_values[exam_type][i]  # Change this line
        validator = QtGui.QDoubleValidator(0, max_value, 1)  # Adjust min, max, and decimals as needed
        enter_result.setValidator(validator)
        # Connect the textChanged signal to the on_text_changed method
        enter_result.editingFinished.connect(partial(gui_ref.on_editing_finished, max_value, enter_result))
        # Set the visibility based on the exam type and current section
        enter_result.setVisible(manual_input_sections[exam_type][i])
        gui_ref.parts_area_layout.addWidget(enter_result, i, 1)
        result_label = QtWidgets.QLabel('0.0', gui_ref.parts_area)
        result_label.setStyleSheet('color: #B9BABD;font-size: 24px;')
        result_label.setFixedWidth(50)
        gui_ref.parts_area_layout.addWidget(result_label, i, 3)
        gui_ref.part_dict[part_number] = {
            'name': part_name,
            'label': part_label,
            'result_field': enter_result,
            'result_label': result_label
        }
        gui_ref.parts_area_layout.setRowStretch(i, 1) # Set the stretch factor for all rows to be equal
    gui_ref.parts_area.setLayout(gui_ref.parts_area_layout)
    gui_ref.parts_area.setStyleSheet('QGroupBox{border: 2px solid #383C43; border-radius: 40px; padding: 5px;background-color: #383C43;}')
