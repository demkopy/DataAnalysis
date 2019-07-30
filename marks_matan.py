import pandas as pd
import collections as cols
import matplotlib.pyplot as plt
import numpy as np


def convert_mark(mark):
    try:
        return int(mark)
    except ValueError:
        return -1


k_21 = pd.read_csv("K-21.csv", index_col=0)
k_22 = pd.read_csv("K-22.csv", index_col=0)
k_23 = pd.read_csv("K-23.csv", index_col=0)

marks_k21 = list(k_21["mark"])
marks_k22 = list(k_22["mark"])
marks_k23 = list(k_23["mark"])

for i in range(len(marks_k21)):
    marks_k21[i] = convert_mark(marks_k21[i])

for i in range(len(marks_k22)):
    marks_k22[i] = convert_mark(marks_k22[i])

for i in range(len(marks_k23)):
    marks_k23[i] = convert_mark(marks_k23[i])

marks_by_groups = {"21": marks_k21, "22": marks_k22, "23": marks_k23}

common_marks_by_group = cols.defaultdict(cols.Counter)
for group, marks in marks_by_groups.items():
    common_marks_by_group[group] = cols.Counter(marks)

all_marks = list()
for marks in marks_by_groups.values():
    for mark in marks:
        all_marks.append(mark)

common_marks = cols.Counter(all_marks)

label_values = sorted(common_marks.keys())

labels = list(str(mark) for mark in label_values)
labels[0] = "absent"

values = np.array([float(common_marks[mark]) / sum(common_marks.values()) for mark in label_values])

explode = label_values.copy()
for i in range(len(explode)):
    explode[i] = 0 if explode[i] != 0 else 0.1


plt.pie(values,
        labels=labels,
        startangle=90,
        shadow=True,
        explode=explode,
        autopct=lambda val: str(int(round(val))) + "%",
        radius=1.4,
        pctdistance=0.8)


def marks_bucket(mark):
    if mark == -1:
        return "absent"
    elif mark == 0:
        return "zero"
    elif mark < 5:
        return "less than five"
    elif mark < 10:
        return "between five and ten"
    elif mark < 15:
        return "between ten and fifteen"
    elif mark < 20:
        return "between fifteen and twenty"
    else:
        return "between twenty and twenty-five"


marks_buckets = cols.defaultdict(int)

for mark, amount in common_marks.items():
    marks_buckets[marks_bucket(mark)] += amount

for bucket, amount in marks_buckets.items():
    print(bucket + ": " + str(amount))
print("Total: " + str(sum(common_marks.values())))
plt.show()

