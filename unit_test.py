import pytest
from program import AttendanceManager,manage_student_file,AttendanceChecker

def test_file_path(tmp_path):

    return tmp_path / "list.txt"

def test_create_new_file(test_file_path):
    manage_student_file("Jan", "Kowalski", 12345, path=str(test_file_path))
 
    assert os.path.isfile(test_file_path)
 
    with open(test_file_path, 'r') as file:
        lines = file.readlines()
    assert lines == ["First Name,Last Name,ID\n", "Jan,Kowalski,12345\n"]

def test_append_to_existing_file(test_file_path):

    with open(test_file_path, 'a') as file:
        file.write("First Name,Last Name,ID\nNme,Srnme,67890\n")
    
    manage_student_file("Jan", "Kowalski", 54321, path=str(test_file_path))
    
    with open(test_file_path, 'r') as file:
        lines = file.readlines()
    
    assert lines == [
        "First Name,Last Name,ID\n",
        "Nme,aSrnme,67890\n",
        "Jan,Kowalski,54321\n"
    ]
