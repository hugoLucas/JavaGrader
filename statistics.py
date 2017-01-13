import prettytable, copy


class Stats:

    def __init__(self, num_of_tests):
        self.number_of_tests = num_of_tests
        self.results = {}

    def add_result(self, student_name, student_result):
        if student_name in self.results:
            if type(self.results[student_name]) is str:
                temp_lis = [str(self.results[student_name]), student_result]
                self.results[student_name] = temp_lis
            else:
                self.results[student_name].append(student_result)
        else:
            self.results[student_name] =  student_result

    def print_results(self):
        table = prettytable.PrettyTable(self.make_table_header())
        table.align = "l"
        sorted_keys = sorted(self.results.keys())
        for key in sorted_keys:
            temp_list = []
            if self.number_of_tests <= 1:
                temp_list = [key, self.results[key]]
            else:
                temp_list = [key] + self.results[key]
            table.add_row(temp_list)
        print(table)

    def make_table_header(self):
        header_list = ['Student Name']
        if self.number_of_tests > 0:
            for x in range(1, self.number_of_tests + 1):
                header_list.append('Test #' + str(x))
        elif self.number_of_tests == -1:
            header_list.append('File Test')
        return header_list