# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 18:45:44 2022

@author: Administrator
"""


def rule(name, Job, buffer, x1, Jobalpha, L, t):
    if name == "FIFO":
        ID = FIFO(Job, buffer, x1, Jobalpha)
    if name == "LIFO":
        ID = LIFO(Job, buffer, x1)
    if name == "SPT":
        ID = SPT(Job, buffer, x1, Jobalpha)
    if name == "LPT":
        ID = LPT(Job, buffer, x1, Jobalpha)
    if name == "LOR":
        ID = LOR(Job, buffer, x1)
    if name == "MOR":
        ID = MOR(Job, buffer, x1)
    if name == "SRTPT":
        ID = SRTPT(Job, buffer, x1, Jobalpha, L)
    if name == "LRTPT":
        ID = LRTPT(Job, buffer, x1, Jobalpha, L)
    if name == "EDD":
        ID = EDD(Job, buffer, x1)
    if name == "LDD":
        ID = LDD(Job, buffer, x1)
    if name == "CR":
        ID = CR(Job, buffer, Jobalpha, t, x1)
    if name == "SLACK":
        ID = SLACK(Job, buffer, Jobalpha, t, x1, L)
    return ID


def FIFO(*args, **kwargs):
    # return FIFO_min_release(*args, **kwargs)
    # return FIFO_max_release(*args, **kwargs)
    # return FIFO_min_due(*args, **kwargs)
    # return FIFO_max_due(*args, **kwargs)
    # return FIFO_min_unfinished(*args, **kwargs)
    # return FIFO_max_unfinished(*args, **kwargs)
    # return FIFO_min_cur_o_time(*args, **kwargs)
    # return FIFO_max_cur_o_time(*args, **kwargs)
    # return FIFO_min_complete(*args, **kwargs)
    # return FIFO_max_complete(*args, **kwargs)
    # return FIFO_max_wait(*args, **kwargs)
    # return FIFO_min_wait(*args, **kwargs)
    # return FIFO_min_unfinished_o(*args, **kwargs)
    # return FIFO_max_unfinished_o(*args, **kwargs)
    # return FIFO_min_avg_unfinished(*args, **kwargs)
    # return FIFO_max_avg_unfinished(*args, **kwargs)

    # return FIFO_min_complete_PLUS_unfinished(*args, **kwargs)
    return FIFO_min_unfinished_PLUS_cur_o_time(*args, **kwargs)


def FIFO_min_complete_PLUS_unfinished(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(0, len(Jobalpha.loc["J" + str(a), "machine"])):
            if next_status >= status - 1:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * 2
            else:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_min_complete_PLUS_cur_o_time(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(0, len(Jobalpha.loc["J" + str(a), "machine"])):
            if next_status == status - 1:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * 2
            else:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_min_complete_PLUS_unfinished_PLUS_cur_o_time(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            if next_status > status - 1:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * 2
            elif next_status == status - 1:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * 3
            else:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_min_unfinished_PLUS_cur_o_time(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    W, V = 1, 9
    # W, V = 2, 8
    # W, V = 3, 7
    # W, V = 4, 6
    # W, V = 6, 4
    # W, V = 7, 3
    # W, V = 8, 2
    # W, V = 9, 1
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            if next_status == status - 1:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * V
                P = P + Jobalpha.loc["J" + str(a), "machine"].at[next_status] * W
            else:
                P = Jobalpha.loc["J" + str(a), "machine"].at[next_status] * W
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_min_avg_unfinished(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        num = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
            num += 1
        P_c = P_c / num
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_avg_unfinished(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        num = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
            num += 1
        P_c = P_c / num
        d.append(P_c)
    max_r = max(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_max_wait(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        if status == 1:
            wt = Job.at[ID, "r1"]
        else:
            wt = Job.at[ID, "c%d" % (status - 1)]
        d.append(wt)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_min_wait(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        if status == 1:
            wt = Job.at[ID, "r1"]
        else:
            wt = Job.at[ID, "c%d" % (status - 1)]
        d.append(wt)
    max_r = min(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_complete(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        P_c = 0
        for next_status in range(0, len(Jobalpha.loc["J" + str(a), "machine"])):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_complete(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        P_c = 0
        for next_status in range(0, len(Jobalpha.loc["J" + str(a), "machine"])):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    max_r = max(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_cur_o_time(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P = Jobalpha.loc["J" + str(a), "machine"].at[status - 1]
        d.append(P)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_cur_o_time(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P = Jobalpha.loc["J" + str(a), "machine"].at[status - 1]
        d.append(P)
    max_r = max(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_unfinished(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_unfinished(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        a = Job.at[ID, "type"]
        a = int(a)
        status = Job.at[ID, "status"]
        status = int(status)
        P_c = 0
        for next_status in range(
            status - 1, len(Jobalpha.loc["J" + str(a), "machine"])
        ):
            P = Jobalpha.loc["J" + str(a), "machine"].at[next_status]
            P_c += P
        d.append(P_c)
    max_r = max(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_due(Job, buffer, x1, Jobalpha):
    min_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        d.append(Job.at[ID, "due"])
    min_r = min(d)
    min_index = d.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_due(Job, buffer, x1, Jobalpha):
    max_ID = 0
    d = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        d.append(Job.at[ID, "due"])
    max_r = max(d)
    max_index = d.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_release(Job, buffer, x1, Jobalpha):
    min_ID = 0
    r = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        r.append(Job.at[ID, "r" + str(status)])
    min_r = min(r)
    min_index = r.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_release(Job, buffer, x1, Jobalpha):
    max_ID = 0
    r = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        r.append(Job.at[ID, "r" + str(status)])
    max_r = max(r)
    max_index = r.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def FIFO_min_unfinished_o(Job, buffer, x1, Jobalpha):
    min_ID = 0
    r = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        r.append(-status)
    min_r = min(r)
    min_index = r.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def FIFO_max_unfinished_o(Job, buffer, x1, Jobalpha):
    min_ID = 0
    r = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        r.append(status)
    min_r = min(r)
    min_index = r.index(min_r)
    min_ID = buffer[x1][min_index]
    return min_ID


def LIFO(Job, buffer, x1):
    max_ID = 0
    r = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        r.append(Job.at[ID, "r" + str(status)])
    max_r = max(r)
    max_index = r.index(max_r)
    max_ID = buffer[x1][max_index]
    return max_ID


def SPT(Job, buffer, x1, Jobalpha):
    min_ID = 0
    P = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        P.append(Jobalpha.loc["J" + str(a), "machine"].at[status - 1])
    min_P = min(P)
    min_index = P.index(min_P)
    min_ID = buffer[x1][min_index]
    return min_ID


def LPT(Job, buffer, x1, Jobalpha):
    max_ID = 0
    P = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        P.append(Jobalpha.loc["J" + str(a), "machine"].at[status - 1])
    max_P = max(P)
    max_index = P.index(max_P)
    max_ID = buffer[x1][max_index]
    return max_ID


def LOR(Job, buffer, x1):
    min_ID = 0
    OR = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        OR.append(7 - status)
    min_OR = min(OR)
    min_index = OR.index(min_OR)
    min_ID = buffer[x1][min_index]
    return min_ID


def MOR(Job, buffer, x1):
    max_ID = 0
    OR = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        OR.append(7 - status)
    max_OR = max(OR)
    max_index = OR.index(max_OR)
    max_ID = buffer[x1][max_index]
    return max_ID


def SRTPT(Job, buffer, x1, Jobalpha, L):
    min_ID = 0
    RTPT = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        RP = 0
        for x3 in range(status, L + 1):
            RP = RP + Jobalpha.loc["J" + str(a), "machine"].at[x3 - 1]
            RTPT.append(RP)
    min_RTPT = min(RTPT)
    min_index = RTPT.index(min_RTPT)
    min_ID = buffer[x1][min_index]
    return min_ID


def LRTPT(Job, buffer, x1, Jobalpha, L):
    max_ID = 0
    RTPT = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        RP = 0
        for x3 in range(status, L + 1):
            RP = RP + Jobalpha.loc["J" + str(a), "machine"].at[x3 - 1]
            RTPT.append(RP)
    max_RTPT = max(RTPT)
    max_index = RTPT.index(max_RTPT)
    max_ID = buffer[x1][max_index]
    return max_ID


def EDD(Job, buffer, x1):
    min_ID = 0
    due = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        due.append(Job.at[ID, "due"])
    min_due = min(due)
    min_index = due.index(min_due)
    min_ID = buffer[x1][min_index]
    return min_ID


def LDD(Job, buffer, x1):
    max_ID = 0
    due = list()
    for x2 in range(0, len(buffer[x1])):

        ID = buffer[x1][x2]
        due.append(Job.at[ID, "due"])
    max_due = max(due)
    max_index = due.index(max_due)
    max_ID = buffer[x1][max_index]
    return max_ID


def CR(Job, buffer, Jobalpha, t, x1):
    min_CR = 0
    CR = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        due = Job.at[ID, "due"]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        p = Jobalpha.loc["J" + str(a), "machine"].at[status - 1]
        ratio = (due - t) / p
        CR.append(ratio)
    min_CR = min(CR)
    min_index = CR.index(min_CR)
    min_ID = buffer[x1][min_index]
    return min_ID


def SLACK(Job, buffer, Jobalpha, t, x1, L):
    min_SLACK = 0
    SLACK = list()
    for x2 in range(0, len(buffer[x1])):
        ID = buffer[x1][x2]
        due = Job.at[ID, "due"]
        status = Job.at[ID, "status"]
        status = int(status)
        a = Job.at[ID, "type"]
        a = int(a)
        RP = 0
        for x3 in range(status, L + 1):
            RP = RP + Jobalpha.loc["J" + str(a), "machine"].at[x3 - 1]
        slack = due - t - RP
        SLACK.append(slack)
    min_SLACK = min(SLACK)
    min_index = SLACK.index(min_SLACK)
    min_ID = buffer[x1][min_index]
    return min_ID
