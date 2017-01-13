# JavaGrader
Provided with a directory of folders each containing .java files, this program will iterate through the directory and compile all .java files in the directory and test them following parameters outlined by the user or against parameters outlined in another .java file provided by the user. 

# Simple Test
<img src="https://cloud.githubusercontent.com/assets/16531006/21949314/0e775eea-d9a6-11e6-8c27-6697ed9ed5cd.png" width="30%"></img>

In a simple test the user provides a specific input to and the expected output of the Java program in order to define a test. Once a user has specified at least one test, the can select the "Run Tests!" button in order to begin the testing of all .java files in the directory and its subfolders. The results for these tests will be summarized for the user in the table at the end of the program execution. 

# File Test
<img src="https://cloud.githubusercontent.com/assets/16531006/21949294/d2877ac8-d9a5-11e6-865b-67f633327fce.png" width="30%"></img>

In a file test a user specifies a .java file base all tests upon. This file is copied into all subfolders and is ran instead of the the other .java files. This file should contain code to test the other files present in the directory by any means the user finds best. The only requirement is that input file provide some form of output quantifying the correctness of the other .java files. This output will be read by the Python program and summarized for the user at the end of execution.
