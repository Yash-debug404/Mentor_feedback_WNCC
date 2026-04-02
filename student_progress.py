def student_prog(student):
    mentor_progress = {}
    mentor_count = {}

    for s in student:
        mentor_ids = s.get("MentorIDs", [])
        milestonecompleted = int(s["MilestonesCompleted"])
        total = int(s["TotalMilestones"])
        p = milestonecompleted / total if total != 0 else 0

        for mentor in mentor_ids:  
            if mentor not in mentor_progress:
                mentor_progress[mentor] = 0
                mentor_count[mentor] = 0
            mentor_progress[mentor] += p
            mentor_count[mentor] += 1

    for m in mentor_progress:
        mentor_progress[m] /= mentor_count[m]  

    return mentor_progress