from Engagement import engagement
from feedback import feed
from Responsiveness import response
from student_progress import student_prog
import csv

interactions = []
student = []
feedback = []
mentors = []

with open("data/feedbacks.csv","r") as csvtemp:
    csvdic = csv.DictReader(csvtemp)
    for line in csvdic:
        feedback.append(line)

with open("data/interactions.csv", "r") as csvtemp:
    csvdic = csv.DictReader(csvtemp)
    for line in csvdic:
        interactions.append(line)

with open("data/students.csv", "r") as csvtemp:
    csvdic = csv.DictReader(csvtemp)
    for line in csvdic:
        student.append(line)

with open("data/mentors.csv", "r") as csvtemp:
    csvdic = csv.DictReader(csvtemp)
    for line in csvdic:
        mentors.append(line)

student_mentor_map = {}
for interaction in interactions:
    sid = interaction["StudentID"]
    mid = interaction["MentorID"]
    if sid not in student_mentor_map:
        student_mentor_map[sid] = []
    if mid not in student_mentor_map[sid]:  
        student_mentor_map[sid].append(mid)


for s in student:
    sid = s["StudentID"]
    s["MentorIDs"] = student_mentor_map.get(sid, []) 

prog = student_prog(student)
W1 = 0.3
respon = response(interactions)
W2 = 0.275
eng = engagement(interactions)
W3 = 0.275
feedb = feed(feedback)
W4 = 0.15

score = []

for m in mentors:
    scores={}
    mentor = m["MentorID"]
    P = float(prog.get(mentor,0))
    R = float(respon.get(mentor,0))
    E = float(eng.get(mentor,0))
    F = float(feedb.get(mentor,0))
    Mm = W1*P + W2*R + W3*E + W4*F 
    name = m["Name"]
    scores["Final Mentor Score"] = Mm
    scores["Name"] = name
    scores["MentorID"] = mentor
    score.append(scores)

score.sort(key=lambda x: x["Final Mentor Score"],reverse=True)


for i in range(len(score)):
    score[i]["Rank"] = i+1

field = ["MentorID","Name","Final Mentor Score","Rank"]
filename = "mentor_scores.csv"
with open(filename , "w") as csvtemp:
    csvdic = csv.DictWriter(csvtemp , fieldnames=field)
    csvdic.writeheader()
    csvdic.writerows(score)
