import os

def manage_student_file(first_name, last_name, student_id, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write("First Name,Last Name,ID\n")
    with open(path, 'a') as file:
        file.write(f"{first_name},{last_name},{student_id}\n")
    # Part 3: Attendance Checker

class AttendanceChecker:
    def __init__(self, manager):
        self.manager = manager

    def check_in(self, date, user_id, status):

     status_bool = status.lower() == "true"
     self.manager.add(date, user_id, status_bool)

            new_status = input("Enter new attendance status (True for present, False for absent): ").strip().lower() == 'true'
            self.manager.edit(date, user_id, new_status)
        else:
            print(f"No attendance record found for user {user_id} on {date}.")
            new_status = input("Enter attendance status (True for present, False for absent): ").strip().lower() == 'true'
            self.manager.add(date, user_id, new_status)


class AttendanceManager:
    def __init__(self):
        self.all_attendance = {}

    def add(self, date, user_id, was):
        if user_id not in self.all_attendance:
            self.all_attendance[user_id] = {}
        self.all_attendance[user_id][date] = was
        print(f"User with id {user_id} on {date} attendance status marked as {was}.")

    def edit(self, date, user_id, was):
        if user_id in self.all_attendance and date in self.all_attendance[user_id]:
            self.all_attendance[user_id][date] = was
            print(f"User with id {user_id} on {date} attendance status updated to {was}.")
        else:
            print(f"No entry found for user with id {user_id} on {date}.")

    def delete(self, date, user_id):
        if user_id in self.all_attendance and date in self.all_attendance[user_id]:
            del self.all_attendance[user_id][date]
            print(f"Attendance entry for user with id {user_id} on {date} deleted.")
        else:
            print(f"No entry found for user with id {user_id} on {date}.")

    def generate_report(self):
        report = "Attendance Report:\n"
        for user_id, dates in self.all_attendance.items():
            report += f"User {user_id}:\n"
            for date, status in dates.items():
                report += f"  - {date}: {status}\n"
        return report

    def export_to_csv(self, filename):
        import csv
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Date", "Status"])
            for user_id, dates in self.all_attendance.items():
                for date, status in dates.items():
                    writer.writerow([user_id, date, status])
        print(f"Attendance data exported to file {filename}.")

import datetime

today_date = datetime.date.today().isoformat()

attendance_manager = AttendanceManager()

attendance_manager.add(date=today_date, user_id=1, was=False)

attendance_manager.edit(date=today_date, user_id=1, was=True)

attendance_manager.add(date=today_date, user_id=2, was=False)

attendance_manager.delete(date=today_date, user_id=2)

print(attendance_manager.generate_report())


attendance_manager.export_to_csv("attendance_report.csv")


