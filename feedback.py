def feed(feedback):
    mentor_feedback={}
    for m in feedback:
        rating = int(m["Rating"])
        mentor = m["MentorID"]
        if mentor not in mentor_feedback:

            mentor_feedback[mentor] = []

        mentor_feedback[mentor].append(rating)
    for m in mentor_feedback:
        l1 = mentor_feedback[m]
        n = len(l1)
        if n==0:
            mentor_feedback[m]=0
            continue
        avg = sum(l1)/n
        var = sum((x-avg)**2 for x in l1)/n
        std = var**0.5
        totwe = 0
        numwe = 0
        for r in l1:
            z = (r-avg)/(std+0.01)
            w = 1/(1+max(0,(abs(z)-2)))
            totwe += w
            numwe += w*r
        Fraw = ((numwe/totwe)-1)/4
        k = 5
        R0 = 0.5
        p = n/(n+k)
        q = k/(n+k)
        F = p*Fraw + q*R0
        mentor_feedback[m]=F
    return mentor_feedback