#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   make_zip_file.py
@Time    :   2025/06/12 14:16:51
@Author  :   yangqinglin
@Version :   v1.0
@Email   :   yangql1@wedoctor.com
@Desc    :   None
"""
import os
import json
import shutil
import subprocess
from scrapy_medbench import SelenuimWrapper


class MakeZipFile:
    def __init__(self, origin_file_dir, zip_file_path: str):
        self.origin_file_dir = origin_file_dir
        self.zip_file_path = zip_file_path
        self.file_paths = []
        os.remove(zip_file_path) if os.path.exists(zip_file_path) else None
        shutil.rmtree("tmp") if os.path.exists("tmp") else None
        os.mkdir("tmp")
        for root, _, files in os.walk(self.origin_file_dir):
            for file in files:
                src_file = os.path.join(self.origin_file_dir, file)
                shutil.copy(src_file, "tmp")
                self.file_paths.append(file)

    def modeify_file(self, filename, id):
        file = filename + ".jsonl"
        file_path = os.path.join("tmp", file)
        file_list = []
        with open(file_path, "r", encoding="utf-8") as f:
            for i in f:
                file_list.append(json.loads(i))
        file_list = [item for item in file_list if item["other"]["id"] == id]
        with open(file_path, "w", encoding="utf-8") as out_file:
            for item in file_list:
                out_file.write(json.dumps(item, ensure_ascii=False) + "\n")

    def make_zip(self):
        command = [
            "zip",
            "-r",
            "MedBench.zip",
            "tmp/",
            "-x",
            "*.DS_Store",
            "-x",
            "__MACOSX*",
        ]
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 输出命令的标准输出和标准错误
        print("标准输出:\n", result.stdout)
        print(f"Created zip file: {self.zip_file_path}")
