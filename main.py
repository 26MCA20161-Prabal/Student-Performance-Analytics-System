import numpy as np
import matplotlib.pyplot as plt

SUBJECTS = ["Maths", "Science", "English", "Computer", "History"]
MAX_MARKS = 100
GRADES = ["A+", "A", "B", "C", "D", "F"]

# Student class

class Student:
    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = np.array(marks)   # marks stored as a NumPy array

    def show_marks(self):
        for i in range(len(SUBJECTS)):
            print(f"  {SUBJECTS[i]:<10}: {self.marks[i]}")


def calculate_total(marks):
    return np.sum(marks)


def calculate_average(marks):
    return np.mean(marks)


def find_highest(marks):
    return np.max(marks)


def find_lowest(marks):
    return np.min(marks)


def find_highest_subject(marks):

    return SUBJECTS[np.argmax(marks)]


def find_lowest_subject(marks):
    return SUBJECTS[np.argmin(marks)]


def assign_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------------
# Functions for the whole class
# ---------------------------------------------------------------
def get_marks_matrix(students):
    # Builds a 2D array: one row per student, one column per subject
    all_marks = []
    for student in students:
        all_marks.append(student.marks)
    return np.array(all_marks)


def calculate_subject_averages(students):
    matrix = get_marks_matrix(students)
    return np.mean(matrix, axis=0)   


def calculate_class_average(students):
    matrix = get_marks_matrix(students)
    return np.mean(matrix)


def find_top_student(students):
    averages = []
    for student in students:
        averages.append(calculate_average(student.marks))
    top_index = np.argmax(averages)   
    return students[top_index]


def count_grades(students):
    
    labels = []
    counts = []
    for grade in GRADES:
        count = 0
        for student in students:
            if assign_grade(calculate_average(student.marks)) == grade:
                count += 1
        if count > 0:
            labels.append(grade)
            counts.append(count)
    return labels, counts


def find_student_by_roll(students, roll_number):
    for student in students:
        if student.roll_number == roll_number:
            return student
    return None 



# Input helpers

def read_number(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please enter a value between {minimum} and {maximum}.")


def read_name(prompt):
    while True:
        name = input(prompt).strip()
        if name != "":
            return name
        print("Name cannot be empty.")



# Menu actions

def add_student(students):
    print("\n--- Add Student ---")
    name = read_name("Enter student name: ")

    while True:
        roll_number = int(read_number("Enter roll number: ", 1, 100000))
        if find_student_by_roll(students, roll_number) is None:
            break
        print("This roll number already exists. Try another.")

    marks = []
    for subject in SUBJECTS:
        mark = read_number(f"Enter marks in {subject} (0-{MAX_MARKS}): ", 0, MAX_MARKS)
        marks.append(mark)

    students.append(Student(name, roll_number, marks))
    print(f"Student '{name}' added successfully.")


def display_students(students):
    if len(students) == 0:
        print("\nNo students added yet.")
        return

    print("\n--- All Students ---")
    print(f"{'Roll No':<10}{'Name':<20}{'Total':>8}{'Average':>10}{'Grade':>8}")
    print("-" * 56)
    for student in students:
        total = calculate_total(student.marks)
        average = calculate_average(student.marks)
        grade = assign_grade(average)
        print(f"{student.roll_number:<10}{student.name:<20}{total:>8.1f}{average:>10.2f}{grade:>8}")


def display_student_performance(students):
    if len(students) == 0:
        print("\nNo students added yet.")
        return

    roll_number = int(read_number("Enter roll number: ", 1, 100000))
    student = find_student_by_roll(students, roll_number)
    if student is None:
        print("No student found with that roll number.")
        return

    marks = student.marks
    average = calculate_average(marks)

    print(f"\n--- Performance of {student.name} (Roll No: {student.roll_number}) ---")
    student.show_marks()
    print(f"Total marks   : {calculate_total(marks):.1f} / {len(SUBJECTS) * MAX_MARKS}")
    print(f"Average marks : {average:.2f}")
    print(f"Highest mark  : {find_highest(marks)} ({find_highest_subject(marks)})")
    print(f"Lowest mark   : {find_lowest(marks)} ({find_lowest_subject(marks)})")
    print(f"Grade         : {assign_grade(average)}")


def show_top_student(students):
    if len(students) == 0:
        print("\nNo students added yet.")
        return

    top = find_top_student(students)
    average = calculate_average(top.marks)
    print("\n--- Top Student ---")
    print(f"Name    : {top.name}")
    print(f"Roll No : {top.roll_number}")
    print(f"Average : {average:.2f}")
    print(f"Grade   : {assign_grade(average)}")


def show_class_average(students):
    if len(students) == 0:
        print("\nNo students added yet.")
        return

    print("\n--- Class Statistics ---")
    print(f"Class average: {calculate_class_average(students):.2f}")
    print("Subject-wise averages:")
    subject_averages = calculate_subject_averages(students)
    for i in range(len(SUBJECTS)):
        print(f"  {SUBJECTS[i]:<10}: {subject_averages[i]:.2f}")


def generate_graphs(students):
    if len(students) == 0:
        print("\nNo students added yet. Add students first.")
        return

    # Graph 1: average marks of each student
    names = []
    averages = []
    for student in students:
        names.append(student.name)
        averages.append(calculate_average(student.marks))

    plt.figure(figsize=(8, 5))
    plt.bar(names, averages, color="skyblue")
    plt.title("Average Marks of Each Student")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Graph 2: subject-wise class average
    subject_averages = calculate_subject_averages(students)

    plt.figure(figsize=(8, 5))
    plt.bar(SUBJECTS, subject_averages, color="orange")
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.tight_layout()

    # Graph 3: grade distribution
    labels, counts = count_grades(students)

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct="%1.1f%%")
    plt.title("Grade Distribution")

    plt.show()   # shows all three windows



# Main program

def show_menu():
    print("\n===== STUDENT PERFORMANCE ANALYTICS SYSTEM =====")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Display Student Performance")
    print("4. Find Top Student")
    print("5. Calculate Class Average")
    print("6. Generate Graphs")
    print("7. Exit")


def main():
    students = []   # list that holds all Student objects

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_student_performance(students)
        elif choice == "4":
            show_top_student(students)
        elif choice == "5":
            show_class_average(students)
        elif choice == "6":
            generate_graphs(students)
        elif choice == "7":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()