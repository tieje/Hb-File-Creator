from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
from sys import argv
import json

# Edit this path to where to where you cloned the repo
user_path = '/Users/thomasfrancis/Documents/hb-file-creator/'

# Get personal information
file = open(os.path.join(user_path,'login-info.json'), mode='r')
info = json.load(file)
file.close()

# Check if login information is missing
missing = False
if info['email'] == '':
    print('Email is missing in login-info.json file.')
    missing = True
if info['password'] == '':
    print('Password is missing in login-info.json file.')
    missing = True
if missing:
    exit

# Begin web scraping
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(
    executable_path=os.path.join(user_path, "chromedriver"),
    options=chrome_options,
)
wait = WebDriverWait(driver, 1)
# Get to intranet homepage argument
driver.get('https://intranet.hbtn.io/')
# Put in Credentials and Login
login_box = driver.find_element_by_xpath(
    '//*[@id="user_login"]'
)
password_box = driver.find_element_by_xpath(
    '//*[@id="user_password"]'
)
login_button = driver.find_element_by_xpath(
    '//*[@id="new_user"]/div[4]/input'
)
login_box.send_keys(info['email'])
password_box.send_keys(info['password'])
login_button.click()

# Go to accept argument during authenticated session
print(argv)
driver.get(argv[2])
print('login successful')
all_file_names = driver.find_elements_by_xpath('//html/body/main/article/div/div/div/div/div[3]/div/ul/li[3]/code')
os.chdir(argv[1])
for elm in all_file_names:
    path = os.path.join(argv[1], elm.text)
    if os.path.exists(path):
        print(elm.text + ' already exists.')
    else:
        f = open(path, 'w')
        f.close()
