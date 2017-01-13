
# Object will be used to handle simple tests on java programs that only require a single input and that only
# produce a single output. Although it would be faster to create a class that can handle n inputs and m outputs,
# I first need to learn how to use the sub-process module of Python and so I will start with the easiest possible
# case in order to improve my skills.
import pathlib, subprocess, statistics, os
from compile import cd


class SimpleTest:

    output_file_name = "student_results.txt"
    test_statistics = None
    directory_name = None
    test_list = []

    def __init__(self, direc):
        self.directory_name = direc

    def define_test(self, user_input, expected_output):
        new_tuple = user_input, expected_output
        self.test_list.append(new_tuple)

    def test_programs(self):
        self.test_statistics = statistics.Stats(len(self.test_list))
        if len(self.test_list) != 0:
            student_folders_path = pathlib.Path(self.directory_name)
            for student_folders in student_folders_path.iterdir():
                self.clear_output_file(student_folders.name)
                student_program_files_path = pathlib.Path(student_folders)
                for student_program_files in student_program_files_path.iterdir():
                    if student_program_files.name.endswith(".class"):
                        self.run_tests(student_program_files, student_folders)
            self.test_statistics.print_results()
        else:
            print("Error - no tests provided")

    def run_tests(self, student_program_files, student_folders):
        with cd(self.directory_name + "\\" + student_folders.name):
            for test in self.test_list:
                with open(self.output_file_name, 'a') as output_file:
                    command = "java " + student_program_files.name[:-6]
                    execute_command = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output_file,
                                                       stderr=output_file)
                    execute_command.communicate(test[0].encode())
                    self.process_output_file(test, student_folders.name)
                    output_file.write("TEST ATTEMPT - INPUT: {} OUTPUT: {} \n".format(test[0], test[1]))
                    output_file.write("----------------------------------------------\n")

    def process_output_file(self, test_case, student_name):
        result_flag = False
        result_string = ''
        with open(self.output_file_name, 'r') as output_file:
            for text_line in output_file:
                if text_line.startswith("Exception in thread"):
                    self.extract_exception(text_line)
                    result_string = self.extract_exception(text_line)
                    result_flag = True
                    break
                if test_case[1] in text_line and 'TEST ATTEMPT' not in text_line:
                    result_string = "PASS"
                    result_flag = True
        if not result_flag:
            result_string = "FAILED"
        self.test_statistics.add_result(student_name, result_string)

    def extract_exception(self, text_line):
        word_list = text_line.split('.')
        exception_name = word_list[len(word_list) - 1].split(":")[0]
        return exception_name

    def clear_output_file(self, student_folder_name):
        with cd(self.directory_name + '//' + student_folder_name):
            with open(self.output_file_name, 'w') as output_file:
                pass


class FileTest:

    output_file_name = "student_results.txt"

    def __init__(self, test_directory, file_path):
        self.test_file_path = file_path
        self.directory_name = test_directory

    def run_test(self):
        self.test_statistics = statistics.Stats(-1)
        temp_list = self.test_file_path.split("\\")
        command = "java " + temp_list[len(temp_list) - 1][:-5]
        student_folders_path = pathlib.Path(self.directory_name)
        for student_folders in student_folders_path.iterdir():
            student_program_files_path = pathlib.Path(student_folders)
            with cd(str(student_program_files_path)):
                with open(self.output_file_name, 'w') as output_file:
                    subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output_file,
                                                       stderr=output_file)
                    self.process_output_file(student_folders.name)
        self.test_statistics.print_results()

    def process_output_file(self, student_name):
        result_string = None
        with open(self.output_file_name, 'r') as output_file:
            for text_line in output_file:
                if text_line.startswith("PASS"):
                    result_string = 'PASS'
                    break
        if result_string is None:
            result_string = "FAILED"
        self.test_statistics.add_result(student_name, result_string)