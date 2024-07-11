import os
import sys
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def generate_card(cardfile):
    cardnum = input("请输入您的考生号：")
    A1, A2, A3, A4, A5, A6, A7, A8 = [num.strip() for num in input("请输入动态口令卡上A行数字 [用,隔开]: ").split(',')]
    B1, B2, B3, B4, B5, B6, B7, B8 = [num.strip() for num in input("请输入动态口令卡上B行数字 [用,隔开]: ").split(',')]
    C1, C2, C3, C4, C5, C6, C7, C8 = [num.strip() for num in input("请输入动态口令卡上C行数字 [用,隔开]: ").split(',')]
    D1, D2, D3, D4, D5, D6, D7, D8 = [num.strip() for num in input("请输入动态口令卡上D行数字 [用,隔开]: ").split(',')]
    E1, E2, E3, E4, E5, E6, E7, E8 = [num.strip() for num in input("请输入动态口令卡上E行数字 [用,隔开]: ").split(',')]
    F1, F2, F3, F4, F5, F6, F7, F8 = [num.strip() for num in input("请输入动态口令卡上F行数字 [用,隔开]: ").split(',')]
    G1, G2, G3, G4, G5, G6, G7, G8 = [num.strip() for num in input("请输入动态口令卡上G行数字 [用,隔开]: ").split(',')]
    H1, H2, H3, H4, H5, H6, H7, H8 = [num.strip() for num in input("请输入动态口令卡上H行数字 [用,隔开]: ").split(',')]

    cardcontext = {
        "A1": A1, "A2": A2, "A3": A3, "A4": A4, "A5": A5, "A6": A6, "A7": A7, "A8": A8,
        "B1": B1, "B2": B2, "B3": B3, "B4": B4, "B5": B5, "B6": B6, "B7": B7, "B8": B8,
        "C1": C1, "C2": C2, "C3": C3, "C4": C4, "C5": C5, "C6": C6, "C7": C7, "C8": C8,
        "D1": D1, "D2": D2, "D3": D3, "D4": D4, "D5": D5, "D6": D6, "D7": D7, "D8": D8,
        "E1": E1, "E2": E2, "E3": E3, "E4": E4, "E5": E5, "E6": E6, "E7": E7, "E8": E8,
        "F1": F1, "F2": F2, "F3": F3, "F4": F4, "F5": F5, "F6": F6, "F7": F7, "F8": F8,
        "G1": G1, "G2": G2, "G3": G3, "G4": G4, "G5": G5, "G6": G6, "G7": G7, "G8": G8,
        "H1": H1, "H2": H2, "H3": H3, "H4": H4, "H5": H5, "H6": H6, "H7": H7, "H8": H8
    }

    with open(cardfile, "w", encoding="utf-8") as cardfile:
        cardfile.write(cardnum)
        cardfile.write('\n')
        cardfile.write(str(cardcontext))


url = "https://gkcx2.jseea.cn/"

driverpath = r"geckodriver.exe"
ROOTDIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOTDIR)
if getattr(sys, 'frozen', False):
    sys.path.append(sys._MEIPASS)
cardpath = os.path.join(ROOTDIR, "card")
if not os.path.exists(cardpath):
    print("未检测到动态口令卡信息，请录入卡上信息。")
    generate_card("card")
cardf = open(os.path.join(ROOTDIR, "card"), "r+")
lines = cardf.readlines()
cardid = lines[0].strip()
cardpasscode: dict = eval(lines[1])

service = Service(executable_path=driverpath)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, service=service)
driver.get(url)
examcode = driver.find_element(by=By.ID, value="ksh")
passcode = driver.find_element(by=By.ID, value="code")
passcodepic = driver.find_element(by=By.ID, value="codepic")
examcode.send_keys(cardid)
imgpath = os.path.join(ROOTDIR, "passcodepic.png")
passcodepic.screenshot(imgpath)
image = Image.open(imgpath)
image.show()
id1, id2 = [idnum.strip().upper() for idnum in input("请输入图片中的行列号 [用,分隔，例如A3,H5]: ").split(',')]
passcode.send_keys(cardpasscode.get(id1) + cardpasscode.get(id2))
button = driver.find_element(by=By.CLASS_NAME, value="sub")
button.click()
time.sleep(5)
result_page = driver.page_source
parser = BeautifulSoup(result_page, features="lxml")
div = parser.body.find('div', attrs={'class': 'mod_null_tit fon'})
result = div.span.text.strip()
print(result)
cardf.close()
driver.quit()

input("\nPress Enter to exit.")
