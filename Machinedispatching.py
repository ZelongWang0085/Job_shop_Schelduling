def machineselection(Machinestatus, x1, K):
    for x2 in range(0, K):
        if Machinestatus[x2][x1] == 0:
            Opt_M = x2
            break
    return Opt_M


def P(Job, x1, min_ID, Jobalpha):
    a = Job.at[min_ID, "type"]
    a = int(a)
    status = Job.at[min_ID, "status"]
    P = Jobalpha.loc["J" + str(a), "machine"].at[status - 1]
    return P
