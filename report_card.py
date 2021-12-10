import csv
import sys
from pprint import pprint
import json

data = {
    "courses": [],
   "students": [],
    "tests": [],
    "marks": []
    }

output = {
    "students":[]
    }

file_list = [sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]]

def build_list(file):
  name = file.split(".")[0]
  with open(file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(spamreader)
    for row in spamreader:
      data[name].append(', '.join(row).split(","))

for file in file_list:
    build_list(file)

#populate students 
for student in data["students"]:
    output["students"].append({"id":student[0],"name":student[1],"totalAverages":[],"courses":[]})

#clean up courses
for course in data["courses"]:
  course[2:] = ["".join(course[2:])]

#loop over courses to populate students.courses
for course in data["courses"]:
    obj = {
      "id": course[0],
      "name": course[1],
      "teacher":course[2],
      "courseAverages":[]
        }
    
    for entry in output["students"]:
        entry["courses"].append(obj)

# {student: {course: weightedAverage}}
student = {}
weight = {}

#make weight lookup
for test in data["tests"]:
    weight[int(test[0])] = [int(test[2]),test[1]]

#attach weight to marks
for mark in data["marks"]:
    mark.append((weight.get(int(mark[0]))))

#data['marks'] = [test_id, student_id, mark, [weight, course_id]

#course_id, student_id, grade*weight
for mark in data["marks"]:
    mark[2] = int(mark[2]) * int(mark[3][0])
    mark[0] = mark[3][1]
    del mark[3]      

for mark in data["marks"]:
    if mark[1] not in student.keys():
        #if student not in data yet
        student[mark[1]] = {mark[0] : [mark[2]]}
    else:
        #if course not in for student yet
        if mark[0] not in student[mark[1]].keys():
            student[mark[1]].update({mark[0]:[mark[2]]})
        else:
            student[mark[1]][mark[0]].append(mark[2]) 

for key, val in student.items():
    for course, grades in val.items():
        student[key][course] = (sum(grades) / 100)

#insert courseAverages
for stud in output["students"]:
    for course in stud["courses"]:
        course["courseAverages"] = student.get(stud["id"], {}).get(course["id"])

#insert totalAVerages
for student in output["students"]:
    avg = []
    for course in student["courses"]:
        avg.append(course["courseAverages"])

    student["totalAverages"] = sum(avg) / len(avg)
    
jsondump = json.dumps(output)

with open(sys.argv[5], "w") as outfile:
    outfile.write(jsondump)
