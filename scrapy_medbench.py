#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   scrapy_medbench.py
@Time    :   2025/06/04 16:04:50
@Author  :   yangqinglin
@Version :   v1.0
@Email   :   yangql1@wedoctor.com
@Desc    :   None
"""
from datetime import datetime, timezone, timedelta
import time
import json
import random
from seleniumwire import webdriver

# from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class SelenuimWrapper:
    def __init__(self, driver_path, proxy=None):
        self.service = ChromeService(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        if proxy:
            self.options.add_argument(f"--proxy-server={proxy}")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def get(self, url):
        self.driver.get(url)
        print(self.driver.title)

    def login(self):
        # 进入登陆页面
        login_element = self.driver.find_element(
            By.XPATH, "//button[contains(., '登录')]"
        )
        login_element.click()

    def login_with_password(self, username, password):
        # 通过账号密码登录
        user_password_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), '密码登录')]")
            )
        )
        user_password_login.click()

        user_box = self.driver.find_element(By.ID, "normal_login_account")
        user_box.send_keys(username)
        pass_box = self.driver.find_element(By.ID, "normal_login_password")
        pass_box.send_keys(password)

        login_button = self.driver.find_element(By.CLASS_NAME, "login-form-button")
        login_button.click()

    def login_with_phone(self, phone_number):
        # 通过手机号登录
        phone_input = self.driver.find_element(By.ID, "normal_login_phone")
        phone_input.send_keys(phone_number)

        get_auth_code_button = self.driver.find_element(By.CLASS_NAME, "getCaptcha")
        get_auth_code_button.click()

    def authenticate(self):
        # # 等待验证码输入框出现
        send_auth_code_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rect-bottom"))
        )
        send_auth_code_button.click()
        try:
            slider = (
                By.XPATH,
                '//span[@aria-label="滑块"]',
            )
            actions = ActionChains(self.driver)
            actions.click_and_hold(slider).perform()
            actions.move_by_offset(0, 260).perform()
            actions.release().perform()
        except:
            print("无滑块验证")

    def go_to_evaluate(self):
        go_to_evaluate_button = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(., '加入评测')]")
            )
        )
        go_to_evaluate_button.click()

    def upload_answer_file(
        self,
        model_name=None,
        param_number=32,
        context_length=2048,
        date=None,
        model_description=None,
        email=None,
        upload_file_path=None,
    ):
        upload_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "_default-circle-area_n8qjy_108")
            )
        )
        upload_button.click()
        model_name_box = self.driver.find_element(
            By.XPATH, "//div[@id='modelName']/input"
        )
        # model_name
        model_name_box.send_keys(model_name)
        developer_type = self.driver.find_element(
            By.XPATH,
            "//input[@placeholder='请输入模型名称']",
        )
        self.driver.execute_script("arguments[0].click();", developer_type)
        # developer_type
        developer_type = self.driver.find_element(
            By.XPATH,
            "//input[@class='ant-radio-input' and @type='radio' and @value='personal']",
        )
        self.driver.execute_script("arguments[0].click();", developer_type)
        # param_number
        param_number_box = self.driver.find_element(
            By.XPATH, "//div[@id='param']/input"
        )
        param_number_box.send_keys(param_number)
        # is open source
        is_open_source = self.driver.find_element(
            By.XPATH,
            "//input[@class='ant-radio-input' and @type='radio' and @value='no']",
        )
        self.driver.execute_script("arguments[0].click();", is_open_source)
        # context_length
        context_len = self.driver.find_element(By.ID, "contextLen")
        context_len.send_keys(context_length)
        # date
        date_box = self.driver.find_element(
            By.XPATH, "//div[@class='ant-picker-input']/input"
        )
        date_box.send_keys(date)
        # model_description
        model_description_box = self.driver.find_element(By.ID, "modelDesc")
        model_description_box.send_keys(model_description)
        # email
        email_box = self.driver.find_element(By.ID, "email")
        email_box.send_keys(email)
        # is public
        is_public = self.driver.find_element(
            By.XPATH,
            "//input[@class='ant-radio-input' and @type='radio' and @value='private']",
        )
        self.driver.execute_script("arguments[0].click();", is_public)
        # upload file
        upload_file = self.driver.find_element(
            By.XPATH, "//input[@type='file' and @name='file']"
        )
        print("Upload file path:", upload_file_path)
        upload_file.send_keys(upload_file_path)

        result = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_evaluate-result_n8qjy_435"))
        )

        return result.text.strip()

    def get_score(self, **kwds):
        url = kwds.get("url", None)
        user = kwds.get("user", None)
        password = kwds.get("password", None)
        self.get(url=url)
        self.login()
        self.login_with_password(user, password)
        self.authenticate()
        time.sleep(3)
        self.driver.execute_script(
            "window.location.href = 'https://medbench.opencompass.org.cn/record'"
        )
        upload_result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_tab-item_1jfqe_43"))
        )
        self.driver.execute_script("arguments[0].click();", upload_result)
        time.sleep(15)
        result = {}
        for request in self.driver.requests:
            if request.response:
                if (
                    request.response.headers.get("Content-Type") == "application/json"
                    and request.method == "GET"
                    and request.url.endswith("v3_dev")
                ):
                    print("Request URL:", request.url)
                    # print("Response Status:", request.response.status_code)
                    body = request.response.body.decode("utf-8")
                    data = json.loads(body)[-1]
                    result.update(data)
        upload_time = datetime.fromtimestamp(result.get("upload_time")) + timedelta(
            hours=8
        )
        release_time = datetime.fromtimestamp(result.get("release_time")) + timedelta(
            hours=8
        )
        result["upload_time"] = upload_time.strftime("%Y-%m-%d %H:%M:%S")
        result["release_time"] = release_time.strftime("%Y-%m-%d %H:%M:%S")
        return result

    def close(self):
        time.sleep(random.randint(3, 5))
        self.driver.quit()

    def upload_file(self, **kwds):
        url = kwds.get("url", None)
        user = kwds.get("user", None)
        password = kwds.get("password", None)
        model_name = kwds.get("model_name", None)
        param_number = kwds.get("param_number", 32)
        context_length = kwds.get("context_length", 2048)
        date = kwds.get("date", None)
        model_description = kwds.get("model_description", None)
        email = kwds.get("email", None)
        upload_file_path = kwds.get("upload_file_path", None)
        self.get(url=url)
        self.login()
        self.login_with_password(user, password)
        self.authenticate()
        self.go_to_evaluate()
        result = self.upload_answer_file(
            model_name=model_name,
            param_number=param_number,
            context_length=context_length,
            date=date,
            model_description=model_description,
            email=email,
            upload_file_path=upload_file_path,
        )
        self.close()
        return result
