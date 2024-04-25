#!/bin/bash

# 循环从 1 到 40
for num in {1..40}
do
    echo $num
    # 调用 Python 脚本 Main.py 并传递参数 num
    python Main.py $num
done