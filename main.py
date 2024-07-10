import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def generate_card(card):
    A1, A2, A3, A4, A5, A6, A7, A8 = [num.strip() for num in input("请输入动态口令卡上A行数字 [用,隔开]: ").split(',')]
    B1, B2, B3, B4, B5, B6, B7, B8 = [num.strip() for num in input("请输入动态口令卡上B行数字 [用,隔开]: ").split(',')]
    C1, C2, C3, C4, C5, C6, C7, C8 = [num.strip() for num in input("请输入动态口令卡上C行数字 [用,隔开]: ").split(',')]
    D1, D2, D3, D4, D5, D6, D7, D8 = [num.strip() for num in input("请输入动态口令卡上D行数字 [用,隔开]: ").split(',')]
    E1, E2, E3, E4, E5, E6, E7, E8 = [num.strip() for num in input("请输入动态口令卡上E行数字 [用,隔开]: ").split(',')]
    F1, F2, F3, F4, F5, F6, F7, F8 = [num.strip() for num in input("请输入动态口令卡上F行数字 [用,隔开]: ").split(',')]
    G1, G2, G3, G4, G5, G6, G7, G8 = [num.strip() for num in input("请输入动态口令卡上G行数字 [用,隔开]: ").split(',')]
    H1, H2, H3, H4, H5, H6, H7, H8 = [num.strip() for num in input("请输入动态口令卡上H行数字 [用,隔开]: ").split(',')]

    with open(card, "w", encoding="utf-8") as cardfile:
        cardfile.write()

ROOTDIR = os.getcwd()

url = "https://gkcx2.jseea.cn/"
card = open("card.txt", "r")

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(url)
examcode = driver.find_element(by=By.ID, value="ksh")
passcode = driver.find_element(by=By.ID, value="code")
passcodepic = driver.find_element(by=By.ID, value="codepic")
examcode.send_keys("24320322830282")
imgpath = os.path.join(ROOTDIR, "passcodepic.png")
passcodepic.screenshot(imgpath)
image = Image.open(imgpath)
image.show()
passcode.send_keys(input("Please input your code: "))
button = driver.find_element(by=By.CLASS_NAME, value="sub")
button.click()
time.sleep(5)
result_page = driver.page_source
parser = BeautifulSoup(result_page, features="lxml")
div = parser.body.find('div', attrs={'class': 'mod_null_tit fon'})
result = div.span.text.strip()
print(result)
driver.quit()
