# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 21:48:30 2022

@author: Administrator
"""

import numpy as np
import pandas as pd
import sys

import dynamicFJS

# Jobalpha is the benchmark of static JSP
Jobalpha = pd.DataFrame(
    np.array(
        [
            [3, 1, 2, 4, 6, 5],
            [1, 3, 6, 7, 3, 6],
            [2, 3, 5, 6, 1, 4],
            [8, 5, 10, 10, 10, 4],
            [3, 4, 6, 1, 2, 5],
            [5, 4, 8, 9, 1, 7],
            [2, 1, 3, 4, 5, 6],
            [5, 5, 5, 3, 8, 9],
            [3, 2, 5, 6, 1, 4],
            [9, 3, 5, 4, 3, 1],
            [2, 4, 6, 1, 5, 3],
            [3, 3, 9, 10, 4, 1],
        ]
    ),
    index=pd.MultiIndex.from_product(
        [["J1", "J2", "J3", "J4", "J5", "J6"], ["sequence", "machine"]]
    ),
    columns=[0, 1, 2, 3, 4, 5],
)
Jobalpha.index.names = ["Jobtype", "information"]

K = 3  # parallel machine size
L = 6  # work centre size
A = 6  # job type size
t = 0
index = 0  # the index of job

dt = np.zeros([1, A], dtype=int)  # the time interval matrix of the releasement
r = np.zeros([1, A], dtype=int)  # the next released date
SumP = dynamicFJS.Sum(Jobalpha, A)
limit = np.array([5, 10])

# Job is the information storage of the jobs
# o1 means the machine index used for the first operation
# r1 means the release date to first work centre
# s1 means the start time of the first operation
# c1 means the completion date of the first operation
Job = pd.DataFrame(
    {
        "index": np.zeros(1),
        "type": np.zeros(1),
        "status": np.zeros(1),
        "due": np.zeros(1),
        "o1": np.zeros(1),
        "o2": np.zeros(1),
        "o3": np.zeros(1),
        "o4": np.zeros(1),
        "o5": np.zeros(1),
        "o6": np.zeros(1),
        "r1": np.zeros(1),
        "r2": np.zeros(1),
        "r3": np.zeros(1),
        "r4": np.zeros(1),
        "r5": np.zeros(1),
        "r6": np.zeros(1),
        "s1": np.zeros(1),
        "s2": np.zeros(1),
        "s3": np.zeros(1),
        "s4": np.zeros(1),
        "s5": np.zeros(1),
        "s6": np.zeros(1),
        "c1": np.zeros(1),
        "c2": np.zeros(1),
        "c3": np.zeros(1),
        "c4": np.zeros(1),
        "c5": np.zeros(1),
        "c6": np.zeros(1),
    }
)

Machinestatus = np.zeros(
    [K, L], dtype=int
)  # machine status matrix, 0 means idle, number means the index of job processed on the machine
buffer = [[] for l in range(L)]  # the work centre buffer
name = "FIFO"


seed_argv = int(sys.argv[1])
np.random.seed(seed_argv)  # random seed for repeated test

# import pdb; pdb.set_trace()

while index <= 299:  # here you can change the problem size
    # while t<=10:
    # job releasement
    Job, r, dt, index, buffer = dynamicFJS.newjob(
        r, t, dt, Job, Jobalpha, A, index, buffer, SumP, limit
    )
    # processed the job
    Machinestatus, Job = dynamicFJS.machine(
        Machinestatus, buffer, Jobalpha, Job, t, L, K
    )
    # print("t="+str(t))
    # print(buffer)
    # print(Machinestatus)
    Machinestatus, Job, buffer = dynamicFJS.dispatching(
        Machinestatus, Job, buffer, t, L, K, Jobalpha, name
    )
    t = t + 1
    # print(Machinestatus)


criteria = dynamicFJS.endcriteria(Job, L)  # check if all the job has finished
while criteria:
    Machinestatus, Job = dynamicFJS.machine(
        Machinestatus, buffer, Jobalpha, Job, t, L, K
    )
    Machinestatus, Job, buffer = dynamicFJS.dispatching(
        Machinestatus, Job, buffer, t, L, K, Jobalpha, name
    )
    t = t + 1
    criteria = dynamicFJS.endcriteria(Job, L)

# how to evaluate the result
# print(Job)
# Job.to_csv('output'+str(1)+'.txt',sep = '\t',index = False)


# 目标（4）是最小化每个作业的平均流动时间。
def obj4(Job):
    flow_times = []
    for _, jj in Job.iterrows():
        if not any([jj["c%d" % ii] for ii in range(1, A + 1)]):
            continue
        min_rr = min([jj["r%d" % ii] for ii in range(1, A + 1)])
        max_cc = max([jj["c%d" % ii] for ii in range(1, A + 1)])
        flow_times.append(max_cc - min_rr)
    return sum(flow_times) / len(flow_times)


# 目标（5）是最小化每个作业的平均迟延时间。
def obj5(Job):
    tardiness_times = []
    for _, jj in Job.iterrows():
        if not any([jj["c%d" % ii] for ii in range(1, A + 1)]):
            continue
        max_cc = max([jj["c%d" % ii] for ii in range(1, A + 1)])
        dd = jj["due"]
        tardiness_times.append(max_cc - dd)
    return sum(tardiness_times) / len(tardiness_times)


# 目标（6）是最小化每个作业的平均等待时间。
def obj6(Job):
    waiting_times = []
    for _, jj in Job.iterrows():
        if not any([jj["c%d" % ii] for ii in range(1, A + 1)]):
            continue
        __t = 0
        for ii in range(1, A + 1):
            __t += jj["s%d" % ii] - jj["r%d" % ii]

            try:
                assert jj["s%d" % ii] - jj["r%d" % ii] >= 0
            except:
                import pdb

                pdb.set_trace()
        waiting_times.append(__t)
    return sum(waiting_times) / len(waiting_times)


# 目标（7）是最小化每个作业的平均等待时间百分比。
def obj7(Job):
    waiting_times_percentage = []
    for _, jj in Job.iterrows():
        if not any([jj["c%d" % ii] for ii in range(1, A + 1)]):
            continue
        __t = 0
        for ii in range(1, A + 1):
            __t += jj["s%d" % ii] - jj["r%d" % ii]

            assert jj["s%d" % ii] - jj["r%d" % ii] >= 0

        min_rr = min([jj["r%d" % ii] for ii in range(1, A + 1)])
        max_cc = max([jj["c%d" % ii] for ii in range(1, A + 1)])
        waiting_times_percentage.append(__t / (max_cc - min_rr))

    return sum(waiting_times_percentage) / len(waiting_times_percentage)


with open("outputs/%03d.txt" % seed_argv, "w") as f:
    print(obj4(Job), file=f)
    print(obj5(Job), file=f)
    print(obj6(Job), file=f)
    print(obj7(Job), file=f)
