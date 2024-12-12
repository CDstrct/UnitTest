import pytest
import os
from program import AttendanceManager,manage_student_file,AttendanceChecker

@pytest.fixture
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
        "Nme,Srnme,67890\n",
        "Jan,Kowalski,54321\n"
    ]
class MockManager:
    def __init__(self):
        self.all_attendance = {}

    def add(self, date, user_id, status):
        if user_id not in self.all_attendance:
            self.all_attendance[user_id] = {}
        self.all_attendance[user_id][date] = status

    def edit(self, date, user_id, status):
        if user_id in self.all_attendance and date in self.all_attendance[user_id]:
            self.all_attendance[user_id][date] = status

@pytest.fixture
def mock_manager():
    return MockManager()

@pytest.fixture
def attendance_checker(mock_manager):
    from program import AttendanceChecker 
    return AttendanceChecker(mock_manager)

def test_add_new_attendance(attendance_checker, mock_manager, mock_input):
    # Now no manual input is needed as it is mocked
    attendance_checker.check_in("2023-12-01", "user1", "true")

    assert "user1" in mock_manager.all_attendance
    assert "2023-12-01" in mock_manager.all_attendance["user1"]
    assert mock_manager.all_attendance["user1"]["2023-12-01"] is True

def test_update_existing_attendance(attendance_checker, mock_manager, mock_input):
    mock_manager.add("2023-12-01", "user1", True)
    attendance_checker.check_in("2023-12-01", "user1", "false")

    assert mock_manager.all_attendance["user1"]["2023-12-01"] == False

def test_no_existing_record(attendance_checker, mock_manager, mock_input):
    attendance_checker.check_in("2023-12-02", "user2", "false")
    assert "user2" in mock_manager.all_attendance
    assert "2023-12-02" in mock_manager.all_attendance["user2"]
    assert mock_manager.all_attendance["user2"]["2023-12-02"] == False

def test_preserve_existing_unchanged(attendance_checker, mock_manager, mock_input):
    mock_manager.add("2023-12-01", "user3", True)
    attendance_checker.check_in("2023-12-01", "user3", "true")
    assert mock_manager.all_attendance["user3"]["2023-12-01"] == True





import csv

def test_add_attendance():
    manager = AttendanceManager()
    manager.add("2024-12-01", 1, True)

    assert 1 in manager.all_attendance
    assert "2024-12-01" in manager.all_attendance[1]
    assert manager.all_attendance[1]["2024-12-01"] == True

def test_edit_attendance():
    manager = AttendanceManager()
    manager.add("2024-12-01", 1, True)
    manager.edit("2024-12-01", 1, False)

    assert manager.all_attendance[1]["2024-12-01"] == False


def test_edit_nonexistent_attendance():
    manager = AttendanceManager()
    manager.edit("2024-12-01", 1, False)  

    assert 1 not in manager.all_attendance

def test_delete_attendance():
    manager = AttendanceManager()
    manager.add("2024-12-01", 1, True)
    manager.delete("2024-12-01", 1)

    assert "2024-12-01" not in manager.all_attendance[1]

def test_delete_nonexistent_attendance():
    manager = AttendanceManager()
    manager.delete("2024-12-01", 1) 

    assert 1 not in manager.all_attendance

def test_generate_report():
    manager = AttendanceManager()
    manager.add("2024-12-01", 1, True)
    manager.add("2024-12-02", 1, False)
    manager.add("2024-12-01", 2, True)

    report = manager.generate_report()

    expected_report = (
        "Attendance Report:\n"
        "User 1:\n"
        "  - 2024-12-01: True\n"
        "  - 2024-12-02: False\n"
        "User 2:\n"
        "  - 2024-12-01: True\n"
    )

    assert report == expected_report

def test_export_to_csv(tmp_path):
    manager = AttendanceManager()
    manager.add("2024-12-01", 1, True)
    manager.add("2024-12-02", 1, False)
    manager.add("2024-12-01", 2, True)

    csv_file = tmp_path / "attendance.csv"
    manager.export_to_csv(csv_file)

    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    expected_rows = [
        ["User ID", "Date", "Status"],
        ["1", "2024-12-01", "True"],
        ["1", "2024-12-02", "False"],
        ["2", "2024-12-01", "True"],
    ]

    assert rows == expected_rows
