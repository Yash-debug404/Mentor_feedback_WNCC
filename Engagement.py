import math

K_FOR_CODER = 3

K_FOR_MEETING = 5

K_FOR_MESSAGES = 32

def n(x):
   return (math.log(1+x))

def saturate_C(x):
    k=n(K_FOR_CODER)
    return n(x)/(n(x)+k)

def saturate_M(x):
    k = n(K_FOR_MEETING)
    return n(x)/(n(x)+k)

def saturate_Msg(x):
    k=n(K_FOR_MESSAGES)
    return n(x)/(n(x)+k)

def Iraw(C,M,Msg):
    Wc = 0.45
    Ic = saturate_C(C)
    Wm = 0.35
    Im = saturate_M(M)
    Wmsg = 0.2
    Imsg = saturate_Msg(Msg)
    return Wc*Ic + Wm*Im + Wmsg*Imsg

def engagement(interaction):
    mentor_interaction={}
    for m in interaction:
        mentor = m["MentorID"]
        Meeting = int(m["Meetings"])
        Code = int(m["CodeReviews"])
        Message = int(m["Messages"])
        I = Iraw(Code,Meeting,Message)

        if mentor not in mentor_interaction:

            mentor_interaction[mentor]=[]

        mentor_interaction[mentor].append(I)

    for m in mentor_interaction:
        l1 = mentor_interaction[m]
        n = len(l1)
        avg = sum(l1)/n
        var = sum((x-avg)**2 for x in l1)/n
        std = var**0.5
        penalty=0.5
        mentor_interaction[m] = max(0,avg - penalty*std)
    return mentor_interaction