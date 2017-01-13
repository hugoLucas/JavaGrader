# The purpose of this class is to act as iterator through a source directory containing multiple folders
# filled with java files.
import pathlib, subprocess, os, shutil


class compile:

    def __init__(self, direc, file):
        self.directory_name = direc
        if file is not None:
            self.file_path = file
            self.file_flag = True
        else:
            self.file_flag = False

    def compile_programs(self):
        student_folders_path = pathlib.Path(self.directory_name)
        for student_folder in student_folders_path.iterdir():
            self.copy_file(self.directory_name + "\\" + student_folder.name)
            student_program_files_path = pathlib.Path(student_folder)
            for student_program_file in student_program_files_path.iterdir():
                if student_program_file.name.endswith('.java'):
                    with cd(self.directory_name + "\\" + student_folder.name):
                        call = "javac " + student_program_file.name
                        try:
                            subprocess.check_output(call, stderr= subprocess.STDOUT)
                        except subprocess.CalledProcessError:
                            call = "javac " + self.rename_java_file(student_program_file.name)
                            subprocess.check_output(call, stderr=subprocess.STDOUT)

    def copy_file(self, file_dist):
        if self.file_flag:
            shutil.copy(self.file_path, file_dist)

    def rename_java_file(self, file_name):
        new_name = ''
        full_file_path = str(os.getcwd()) + "\\" + file_name
        with open(full_file_path, 'r') as file:
            for line in file:
                if "public class" in line:
                    new_name = line[13:-1].replace('{', '')
                    new_name = new_name.replace(' ', '')
        os.rename(full_file_path, new_name + '.java')
        return new_name + '.java'

# Credit: Brian M. Hunt (http://stackoverflow.com/users/19212/brian-m-hunt)
class cd:
    # Context manager for changing the current working directory
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)