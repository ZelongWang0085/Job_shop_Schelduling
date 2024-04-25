# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 22:37:29 2022

@author: Administrator
"""
import numpy as np
import pandas as pd
import dispatchingrules
import Machinedispatching


def releasement(limit):
    lowlimit = limit[0]
    uplimit = limit[1]
    dt = np.random.randint(
        lowlimit, uplimit
    )  # here you can change the releasement pattern
    return dt


def Sum(Jobalpha, A):
    SumP = np.zeros([1, A], dtype=int)
    for x1 in range(0, A):
        SumP[0, x1] = np.sum(Jobalpha.loc["J" + str(x1 + 1), "machine"])
    return SumP


def tardinessFactor():
    pool = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    Factor = np.random.choice(pool, 1)
    return Factor


def newjob(r, t, dt, Job, Jobalpha, A, index, buffer, SumP, limit):
    for x1 in range(0, A):
        if t == r[0, x1] and r[0, x1] != 0:
            index = index + 1
            tempJ = Job.loc[0]
            tempJ.at["type"] = x1 + 1
            tempJ.at["r1"] = t
            tempJ.at["status"] = 1
            tempJ.at["index"] = index
            Factor = tardinessFactor()
            tempJ.at["due"] = np.around(t + Factor * SumP[0, x1], 2)
            tempJ = pd.DataFrame(tempJ).T
            Job = pd.concat([Job, tempJ], ignore_index=True)
            dt[0, x1] = 0

            nextU = Jobalpha.loc["J" + str(x1 + 1), "sequence"].at[0]
            buffer[nextU - 1].append(index)

        if dt[0, x1] == 0:
            dt[0, x1] = releasement(limit)
            r[0, x1] = r[0, x1] + dt[0, x1]
    return Job, r, dt, index, buffer


def machine(Machinestatus, buffer, Jobalpha, Job, t, L, K):
    for x1 in range(0, L):
        for x2 in range(0, K):
            ID = Machinestatus[x2][x1]
            if ID != 0:
                status = Job.at[ID, "status"]
                status = int(status)
                c = Job.at[ID, "c" + str(status)]
                if c == t:
                    Job.at[ID, "status"] = status + 1
                    Machinestatus[x2][x1] = 0
                    if status != L:
                        a = int(Job.at[ID, "type"])
                        nextU = Jobalpha.loc["J" + str(a), "sequence"].at[status]
                        buffer[nextU - 1].append(ID)

    return Machinestatus, Job


def dispatching(Machinestatus, Job, buffer, t, L, K, Jobalpha, name):
    for x1 in range(0, L):
        sizeM = 0

        for x2 in range(0, K):
            if Machinestatus[x2][x1] == 0:
                sizeM = sizeM + 1
        while len(buffer[x1]) != 0 and sizeM != 0:

            ID = dispatchingrules.rule(name, Job, buffer, x1, Jobalpha, L, t)
            # print(t,buffer[x1],ID)
            Opt_M = Machinedispatching.machineselection(Machinestatus, x1, K)
            P = Machinedispatching.P(Job, x1, ID, Jobalpha)

            buffer[x1].remove(ID)
            Machinestatus[Opt_M][x1] = ID
            status = Job.at[ID, "status"]
            status = int(status)
            Job.at[ID, "s" + str(status)] = t
            Job.at[ID, "c" + str(status)] = t + P
            Job.at[ID, "o" + str(status)] = Opt_M + 1
            if status != L:
                Job.at[ID, "r" + str(status + 1)] = t + P
            sizeM = sizeM - 1

    return Machinestatus, Job, buffer


def endcriteria(Job, L):
    Un = len(Job[Job["status"] != L + 1])
    criteria = Un != 1
    return criteria
