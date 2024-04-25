# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 23:27:14 2023

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 21:48:30 2022

@author: Administrator
"""

import numpy as np
import pandas as pd

import dynamicFJS
import time

start = time.time()

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


L = 6  # work centre size
A = 6  # job type size


for x1 in range(0, 5):
    for T in [100, 200, 500]:
        for K in [1, 2, 3, 4, 5]:  # parallel machine size
            for name in ("FIFO", "SPT", "EDD"):  # the candidate of the rules
                for limit in ([1, 100], [51, 150], [101, 200]):

                    t = 0
                    index = 0  # the index of job

                    dt = np.zeros(
                        [1, A], dtype=int
                    )  # the time interval matrix of the releasement
                    r = np.zeros([1, A], dtype=int)  # the next released date
                    SumP = dynamicFJS.Sum(Jobalpha, A)

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

                    buffer = [[] for l in range(L)]  # the work centre buffer

                    np.random.seed(x1 + 1)  # random seed for repeated test
                    Machinestatus = np.zeros(
                        [K, L], dtype=int
                    )  # machine status matrix, 0 means idle, number means the index of job processed on the machine
                    while index <= T:  # here you can change the problem size
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

                    criteria = dynamicFJS.endcriteria(
                        Job, L
                    )  # check if all the job has finished
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

                    Job.to_csv(
                        "output_"
                        + "seed"
                        + str(x1 + 1)
                        + "_length"
                        + str(T)
                        + "_K"
                        + str(K)
                        + "_limit"
                        + str(limit)
                        + "_"
                        + name
                        + ".txt",
                        sep="\t",
                        index=False,
                    )
end = time.time()
print(end - start)
