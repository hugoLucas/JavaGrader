import sys, pathlib, os, shutil
from compile import cd

class DirectoryMaker:

    def __init__(self):
        self.source_directory = sys.argv[1]
        if len(sys.argv) == 2:
            self.name_index = 1
        elif len(sys.argv) == 3:
            self.name_index = int(sys.argv[2])

    def iterate_through_files(self):
        source_folder = pathlib.Path(self.source_directory)
        for student_file in source_folder.iterdir():
            if '.java' in student_file.name :
                full_file_name_list = student_file.name.split('_')
                assignment_name = full_file_name_list[0]
                new_directory = self.source_directory + '\\' + assignment_name
                if not os.path.exists(new_directory):
                    os.makedirs(new_directory)
                self.move_files(full_file_name_list, student_file.name, new_directory)

    def move_files(self, full_file_name_list, full_file_name, destination_directory):
        folder_name = full_file_name_list[self.name_index]
        new_file_name = full_file_name_list[len(full_file_name_list) - 1]
        with cd(destination_directory):
            new_folder_path = destination_directory + '\\' + folder_name
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            shutil.copy(self.source_directory + '\\' + full_file_name, new_folder_path)
            os.rename(new_folder_path + '\\' + full_file_name, new_folder_path + '\\' + new_file_name)

if __name__ == "__main__":
    maker = DirectoryMaker()
    maker.iterate_through_files()