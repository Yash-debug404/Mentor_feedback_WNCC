import math

def deno(t):
    t = t/12
    return (t)**2+1

def num(t):
    return math.pi/2

def response(interaction):
    mentor_response={}
    for m in interaction:
        time = float(m["AvgResponseTime"])
        mentor = m["MentorID"]

        R = math.sin(num(time)/deno(time))

        if mentor not in mentor_response:
            mentor_response[mentor]=[]

        mentor_response[mentor].append(R)
    
    for m in mentor_response:
        l1 = mentor_response[m]
        n = len(l1)

        if n==0:
            mentor_response[m]=0
            continue
        
        avg = sum(l1)/n
        var = sum((x - avg)**2 for x in l1)/n
        penalty=0.5
        std = var**0.5
        mentor_response[m] = max(0 , avg - penalty*std)

    return mentor_response