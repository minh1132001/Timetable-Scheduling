import numpy as np
import time
starting_time = time.time()

n_class = 0
n_teacher = 0
n_subject = 0

a_class_subject = None
a_teacher_subject = None
subject_info = None


# Read data from file data.txt
def read_data():
    global a_teacher_subject, a_class_subject, n_teacher, n_class, n_subject, subject_info
    with open('data3.txt') as f:

        # Read info
        curr_line = f.readline()
        n_teacher, n_class, n_subject = int(curr_line.split(" ")[0]), \
                                        int(curr_line.split(" ")[1]), \
                                        int(curr_line.split(" ")[2])
        # Make class_subject_matrix
        a_class_subject = np.zeros((n_class, n_subject))
        for i in range(n_class):
            current_class_subject = f.readline().split(" ")[:-1]  # Bỏ đi số 0 ở cuối
            for subject in current_class_subject:
                a_class_subject[i, int(subject) - 1] = 1  # Matrix = 1 nếu lớp i học môn j (subject)

        # Make teacher_subject matrix
        a_teacher_subject = np.zeros((n_teacher, n_subject))
        for i in range(n_teacher):
            current_teacher_subject = f.readline().split(" ")[:-1]  # Bỏ đi số 0 ở cuối
            for subject in current_teacher_subject:
                a_teacher_subject[i, int(subject) - 1] = 1  # Matrix = 1 nếu gv i dạy môn j (subject)

        # Make subject_info matrix
        subject_info = [int(si) for si in f.readline().split(" ")]

        # Fill subject info in a_class_subject
        for i in range(n_class):
            for j in range(n_subject):
                a_class_subject[i, j] = a_class_subject[i, j] * subject_info[j]
read_data()


timeable = []
def Check(timeable, period, _class, _teacher):
    if len(timeable) == 0:
        return False
    for i in range(len(timeable)):
        if timeable[i][0] == period:
            if timeable[i][1] == _class or timeable[i][3] == _teacher:
                return True
    return False


def solution(timeable):
    total_periods_per_day = 5
    day = 1
    total_periods = timeable[-1][0]
    total_days = 5
    for day in range(total_days):
        print("Thu", day + 2, end="")
        print(":")
        for period in range(total_periods_per_day):
            if (day * total_periods_per_day) + (period + 1) <= total_periods :
                print("------ Tiet", period + 1)
                for _timeable in timeable:
                    if _timeable[0] == (day * total_periods_per_day) + (period + 1):
                        print(".......Lop ", _timeable[1] + 1, " hoc mon ", _timeable[2] + 1, " Giao vien ", _timeable[3] + 1)


def scheduling(period, timeable, a_class_subject):
    global done
    global can_arrange
    can_arrange = False
    for _class in range(n_class):
        for _subject in range(n_subject):
            if a_class_subject[_class, _subject] > 0:  # Còn tiết cần xếp
                for _teacher in range(n_teacher):
                    if a_teacher_subject[_teacher, _subject] > 0:
                        # Nếu không trùng lớp và thầy
                        if not Check(timeable, period, _class, _teacher):
                            # Trừ đi số tiết
                            a_class_subject[_class, _subject] = a_class_subject[_class, _subject] - 1
                            dict = [period, _class, _subject, _teacher]
                            timeable.append(dict)
                            scheduling(period, timeable, a_class_subject)
                            if done:
                                return
                            scheduling(period, timeable, a_class_subject + 1)
                            can_arrange = True


        if np.count_nonzero(a_class_subject) == 0:  # Đã xếp xong
            done = True
            return solution(timeable)

    if np.count_nonzero(a_class_subject) > 0 and not can_arrange:
        scheduling(period + 1, timeable, a_class_subject)


scheduling(0, timeable, a_class_subject)
print(timeable)
print("Execution time =", time.time() - starting_time)
