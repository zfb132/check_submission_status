import os
import random
import smtplib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from email.mime.text import MIMEText
from email.header import Header
from log import initLog
from config import *

logging = initLog('submission.log', __name__)

def send_email(msg):
    message = MIMEText(f'New status for {URL} \n\n{msg}', 'plain', 'utf-8')
    message['From'] = f"NewStatus <{SENDER_EMAIL}>"
    message['To'] =  ", ".join(RECEIVERS)
    subject = URL.split('/')[-1].upper()
    message['Subject'] = f'{subject} Manuscript Status: {msg}'
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(SENDER_SERVER, SMTP_PORT)
        smtpObj.login(SENDER_EMAIL, SENDER_PWD)  
        smtpObj.sendmail(SENDER_EMAIL, RECEIVERS, message.as_string())
        print("Sent email successfully")
        logging.info("Sent email successfully")
    except smtplib.SMTPException as e:
        print("Error: unable to send email")
        print(repr(e))
        logging.error("Error: unable to send email")


def get_random_interval():
    '''
    获取随机时间间隔
    '''
    return random.randint(1, 5)


def update_status(status):
    '''
    更新投稿状态
    '''
    name = "status.txt"
    if not os.path.exists(name):
        with open(name, 'w') as f:
            f.write(status)
            logging.info(f'Crate {name} file: current status is "{status}"')
    else:
        with open(name, 'r') as f:
            previous_status = f.read()
            if previous_status != status:
                with open(name, 'w') as f:
                    f.write(status)
                    logging.info(f'Update {name} file: current status is "{status}"')
                    send_email(status)
            else:
                logging.info(f'Current status is "{status}", no update')


def run():
    '''
    登录投稿网站，获取投稿状态
    '''
    # 指定chromedriver路径
    my_service = Service(executable_path=DRIVER_PATH)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    b = Browser(driver_name='chrome', service=my_service, options=chrome_options)
    time.sleep(get_random_interval())
    b.visit(URL)
    time.sleep(get_random_interval())
    b.fill('USERID', USER)
    time.sleep(get_random_interval())
    b.fill('PASSWORD', PWD)
    time.sleep(get_random_interval())
    # 点击登录按钮
    wait = WebDriverWait(b.driver, 30)
    e = wait.until(EC.element_to_be_clickable((By.ID, 'logInButton')))
    b.driver.execute_script("arguments[0].click();", e)
    time.sleep(get_random_interval())
    # 切换到作者页面
    html_obj = b.html
    soup = BeautifulSoup(html_obj,"lxml")
    li = soup.find_all("li", attrs={"class": "nav-link"})
    for a in li:
        author_tag = a.find("a")
        if author_tag and author_tag.text.strip() == "Author":
            b.driver.execute_script(author_tag["href"].split("javascript:")[-1])
            break
    time.sleep(get_random_interval())
    html_obj = b.html
    soup = BeautifulSoup(html_obj,"lxml")
    table = soup.find("span", attrs={"class": "pagecontents"})
    print(table.string)
    current_manuscript_status = table.string
    time.sleep(get_random_interval())
    b.quit()
    update_status(current_manuscript_status)


if __name__=="__main__":
    run()