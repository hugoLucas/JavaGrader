from compile import compile
from test import SimpleTest, FileTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, sys


class JavaGraderGUI(QDialog):

    directory_button = None

    def __init__(self):
        super().__init__()

        # Create each of the three main GUI sections
        self.directory_section()
        self.test_type_selection_section()
        self.test_parameters_section()

        # Add them to the main window layout and display
        self.master_layout = QVBoxLayout()
        self.master_layout.addWidget(self.direc_sel_box)
        self.master_layout.addWidget(self.test_sel_box)
        self.master_layout.addWidget(self.param_box)
        self.setLayout(self.master_layout)
        self.simple_parameters()
        self.display_window()

        # Add data structs needed for testing
        self.test_case_list = []
        self.directory_selected = None

    # Make window visible and set default dimensions and properties
    def display_window(self):
        self.setWindowTitle('Java Grader')
        self.setFixedWidth(300)
        self.setFixedHeight(280)
        self.show()

    # Top-most section which house the test directory selection button
    def directory_section(self):
        self.direc_sel_box = QGroupBox('Directory Selection')

        direction_sel_layout = QHBoxLayout()
        self.directory_button = QPushButton("Select")
        self.directory_button.clicked.connect(self.get_directory_name)
        direction_sel_layout.addWidget(self.directory_button)

        self.direc_sel_box.setLayout(direction_sel_layout)

    # Prompts user for directory and saves string value to pass to testing classes
    def get_directory_name(self):
        selected_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory", 'c:\\'))
        if selected_directory is not None and len(selected_directory) > 0:
            self.directory_selected = selected_directory
            self.directory_button.setText(self.directory_selected)

    # Second section which allows user to determine what type of test they want to conduct
    def test_type_selection_section(self):
        self.test_sel_box = QGroupBox('Test Type')

        test_sel_box = QHBoxLayout()
        simple_test_radio_button = QRadioButton('Simple')
        simple_test_radio_button.clicked.connect(self.simple_parameters)
        simple_test_radio_button.setChecked(True)
        test_sel_box.addWidget(simple_test_radio_button)

        file_test_radio_button = QRadioButton('File')
        file_test_radio_button.clicked.connect(self.file_parameters)
        test_sel_box.addWidget(file_test_radio_button)

        self.test_sel_box.setLayout(test_sel_box)

    # Third sectoion, left blank in order to house user selected parameters
    def test_parameters_section(self):
        self.param_box = QGroupBox('Test Parameters')

    # Creates GUI elements needed to take inputs required to run a simple test
    def simple_parameters(self):
        self.switch_parameter_options()
        self.expected_input_line = QLineEdit()
        self.expected_output_line = QLineEdit()
        self.expected_input_line.setAlignment(Qt.AlignLeft)
        self.expected_output_line.setAlignment(Qt.AlignLeft)

        simple_test_form = QFormLayout()
        simple_test_form.addRow("User Input:", self.expected_input_line)
        simple_test_form.addRow("Expected Output:", self.expected_output_line)

        simple_test_buttons = QHBoxLayout()
        add_test_button = QPushButton("Add Test")
        add_test_button.clicked.connect(self.add_test_case)
        view_tests_button = QPushButton("View Tests")
        view_tests_button.clicked.connect(self.view_current_tests)
        simple_test_buttons.addWidget(add_test_button)
        simple_test_buttons.addWidget(view_tests_button)

        run_test_button = QPushButton("Run Tests!")
        run_test_button.clicked.connect(self.run_simple_tests)
        simple_test_form.addRow(simple_test_buttons)
        simple_test_form.addRow(run_test_button)
        self.param_box.setLayout(simple_test_form)
        self.switch_window_size(300, 280)

    # Adds current user input to list of test cases to run
    def add_test_case(self):
        user_input = self.expected_input_line.text()
        user_output = self.expected_output_line.text()
        if len(user_input) == 0 or len(user_output) == 0:
            self.display_message("Invalid test case")
        else:
            self.test_case_list.append([user_input, user_output])
            self.expected_output_line.setText('')
            self.expected_input_line.setText('')
            self.display_message("Test Case Added")

    # Creates a dialog window which allows the user to see what tests they have added to the system
    def view_current_tests(self):
        if len(self.test_case_list) == 0:
            self.display_message("No tests have been added!")
        else:
            test_case_string = ""
            for x in range(0, len(self.test_case_list)):
                test_input = self.test_case_list[x][0]
                test_output = self.test_case_list[x][1]
                test_str = 'Test Case {}: Input = {}, Output = {}'.format(x + 1, test_input, test_output)
                test_case_string += test_str + os.linesep
            self.display_message(test_case_string)

    # Compiles all files to be tested and passes all user inputted test file to appropriate classes
    def run_simple_tests(self):
        if len(self.test_case_list) == 0:
            self.display_message("Test cases needed")
        elif self.directory_selected is None:
            self.display_message("Test directory needed")
        else:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            test_set_up = compile(self.directory_selected, None)
            test_set_up.compile_programs()

            test_run = SimpleTest(self.directory_selected)
            for test in self.test_case_list:
                test_run.define_test(test[0], test[1])
            test_run.test_programs()
            QApplication.restoreOverrideCursor()

    # Creates GUI elements needed to take inputs required to run a file test
    def file_parameters(self):
        self.switch_parameter_options()
        self.select_file_button = QPushButton("Select Java File")
        self.select_file_button.clicked.connect(self.get_file_name)
        run_test_button = QPushButton("Run Tests!")
        run_test_button.clicked.connect(self.run_file_test)

        file_test_buttons = QGridLayout()
        file_test_buttons.addWidget(self.select_file_button, 1, 1)
        file_test_buttons.addWidget(run_test_button, 2, 1)
        self.param_box.setLayout(file_test_buttons)
        self.switch_window_size(300, 230)

    # Determines file to base file testing off of
    def get_file_name(self):
        selected_file = QFileDialog.getOpenFileName(self, 'Test File', 'c:\\', ".java")
        if selected_file is not None and len(selected_file) > 0:
            self.file_selected = selected_file
            self.directory_button.setText(self.select_file_button)

    # Compiles all files to be tested and displays results
    def run_file_test(self):
        if self.file_selected is None:
            self.display_message("Test file needed")
        else:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            file_compile = compile(self.directory_selected, self.file_selected)
            file_compile.compile_programs()
            file_test = FileTest(self.directory_selected, self.file_selected)
            file_test.run_test()
            QApplication.restoreOverrideCursor()

    # Helper method to transition GUI from a simple to file test or vise versa
    def switch_parameter_options(self):
        self.param_box.deleteLater()
        self.test_parameters_section()
        self.master_layout.addWidget(self.param_box)

    # Sets to the GUI window size to the specified dimensions
    def switch_window_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.show()

    # Displays an information message to the user
    def display_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()

if __name__ == "__main__":
    #test_set_up = compile('C:\\Users\\Hugo Lucas\\Desktop\\file_dir\\Lab #1  Recursive Factorial')
    application = QApplication([])
    win = JavaGraderGUI()
    sys.exit(application.exec_())