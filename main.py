#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2025/06/12 16:56:18
@Author  :   yangqinglin
@Version :   v1.0
@Email   :   yangql1@wedoctor.com
@Desc    :   None
"""
import string
import random
import json
import time
from datetime import datetime, timedelta
from scrapy_medbench import SelenuimWrapper
from make_zip_file import MakeZipFile

DRIVER_PATH = "/Users/admin/wedoctor/medbench/chromedriver-mac-x64/chromedriver"
# 原始medbench目录
ORIGIN_FILE_DIR = "/Users/admin/wedoctor/medbench/MedBench"
# 上传的zip文件路径
UPLOAD_ZIP = "/Users/admin/wedoctor/medbench/MedBench.zip"
# 账号文件路径
ACCOUNT_FILE = "/Users/admin/wedoctor/medbench/scrapy/zhanghao.jsonl"
PROXY = "socks5://172.27.24.28:7897"
MEDBENCH_URL = "https://medbench.opencompass.org.cn/home"


def main(category, user, password, id=None):
    # 原始medbench目录
    origin_file_dir = ORIGIN_FILE_DIR
    zip_file_path = "MedBench.zip"

    maker = MakeZipFile(origin_file_dir, zip_file_path)
    if id:
        maker.modeify_file(category, id)
        model_name = f"{category}_{id}_model"
        model_description = f"{category}_{id}_model_description"
    else:
        model_name = f"{category}_model"
        model_description = f"{category}_model_description"
    maker.make_zip()

    param_number = random.choice([7, 14, 32, 48, 72])
    context_length = random.choice([1024, 4098])
    # random choice date
    start = datetime.strptime("2025-05-02", "%Y-%m-%d")
    end = datetime.strptime("2025-06-16", "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_date = start + timedelta(days=random_days)
    date = random_date.strftime("%Y-%m-%d")

    email = f"{random.randint(1,50)}@{''.join(random.choices(string.ascii_letters + string.digits, k=3))}.com"
    selenuim_wrapper = SelenuimWrapper(DRIVER_PATH, PROXY)
    result = selenuim_wrapper.upload_file(
        url=MEDBENCH_URL,
        user=user,
        password=password,
        model_name=model_name,
        param_number=param_number,
        context_length=context_length,
        date=date,
        model_description=model_description,
        email=email,
        upload_file_path=UPLOAD_ZIP,
    )
    return result


def get_answer():
    user = "rhknfu6z@bccto.cc"
    password = "j12u589B2,6mVh4hubpT"
    selenuim_wrapper = SelenuimWrapper(DRIVER_PATH, PROXY)
    score = selenuim_wrapper.get_score(
        url=MEDBENCH_URL,
        user=user,
        password=password,
    )
    return score


def get_user_passwrd():
    with open(ACCOUNT_FILE, "r") as f:
        for i, up in enumerate(f):
            up = json.loads(up)
            user = up.get("email")
            password = up.get("pw")
            yield i, (user, password)


def batch_submit(category, start_id, end_id, step):
    start_id = start_id + step
    end_id = end_id + step
    for i, (user, password) in get_user_passwrd():
        if start_id - 1 <= i <= end_id - 1:
            print(i + 1, user, password)
            id = i + 1 - step
            result = main(category=category, id=id, user=user, password=password)
            print(result)
            if result != "查看结果":
                print(f"User: {user}, Password: {password}, id: {id}, Result: {result}")
                break
        elif i >= end_id:
            break


def batch_get_answer(start_id, end_id, score_file, step):
    start_id = start_id + step
    end_id = end_id + step
    with open(score_file, "w", encoding="utf-8") as f:
        for i, (user, password) in get_user_passwrd():
            if start_id - 1 <= i <= end_id - 1:
                print(i + 1, user, password)
                selenuim_wrapper = SelenuimWrapper(DRIVER_PATH, PROXY)
                score = selenuim_wrapper.get_score(
                    url=MEDBENCH_URL,
                    user=user,
                    password=password,
                )
                f.write(json.dumps(score, ensure_ascii=False) + "\n")


def get_single_answer(category, id, step=800):
    id = id + step
    for i, (user, password) in get_user_passwrd():
        if i == id - 1:
            print(i + 1, user, password)
            id = i + 1 - step
            result = main(category=category, id=id, user=user, password=password)
            print(result)
            time.sleep(5)
            selenuim_wrapper = SelenuimWrapper(DRIVER_PATH, PROXY)
            score = selenuim_wrapper.get_score(
                url=MEDBENCH_URL,
                user=user,
                password=password,
            )
            print(score)
            break


def all_score(user, password):
    all_res = main(category="all_test", user=user, password=password)
    print(all_res)
    time.sleep(5)
    selenuim_wrapper = SelenuimWrapper(DRIVER_PATH, PROXY)
    score = selenuim_wrapper.get_score(
        url=MEDBENCH_URL,
        user=user,
        password=password,
    )
    print(score)


if __name__ == "__main__":
    # batch_submit("DBMHG_test", 49, 49, step=250)
    # time.sleep(5)
    batch_get_answer(1, 50, "DBMHG_score.jsonl", step=250)
    # print("<A, C, D, E, F, G, H, I, J, K, L, M, N, O, P>")
    # get_single_answer("MedDG_test", 1, step=106)
    # all_score(user="dzvpeqlw@bccto.cc", password="j12u589B2,6mVh4hubpT")
    # 第三次提交，通过本地修改，解决和git的冲突
    # 第二次提交，直接通过github修改
    # 第四次提交，没有任何操作
    # 第五次提交，没有任何操作
    # 第六次提交，没有任何操作
    # 第七次提交，没有任何操作
