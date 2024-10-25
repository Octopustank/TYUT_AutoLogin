#!/usr/bin/python3
def _message(msg:str, end='\n'):
    print(f"[MESSAGE] {msg}", end=end)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import time as tm
import json as js
import os
import subprocess
import sys
_message("import over.")

DEBUG = False
URL = "http://drcom.tyut.edu.cn/"
BROWSER_BINARY_PATH = subprocess.getoutput("which firefox")

def _get_path():
    path = os.getcwd()
    data = os.path.join(path, "data.json")
    if not os.path.isfile(data):
        _message(f"No data file at {data}")
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        data = os.path.join(path, "data.json")
        
        if not os.path.isfile(data):
            _message(f"No data file at {data}")
            _error("No data file was found.")
            sys.exit(1)
    return data
    
    
def _set_browser():
    options = Options()
    options.binary_location = BROWSER_BINARY_PATH
    options.add_argument("-headless")
    service = Service(log_path=os.devnull)
    browser = webdriver.Firefox(options=options, service=service)
    return browser

def _creat_display(debug=False):
    if debug:
        display = None
    else:
        display = Display(visible=0, size=(1280, 768))
        display.start()
    return display


def _fill_in(ipts: list, usr_name:str, psw:str) -> None:
    ipts[2].clear()
    ipts[3].clear()
    ipts[2].send_keys(usr_name)
    ipts[3].send_keys(psw)
    return

def _click_login(ipts: list) -> None:
    # ipts[5].click() # Auto login
    ipts[6].click() # Save the password
    ipts[1].click() # Login
    return


def _error(msg:str):
    print(f"[ ERROR ] {msg}")


def load_data():
    data = _get_path()
    with open(data, "r", encoding='utf-8') as f:
        data = js.load(f)
    usr_name = data["username"]
    psw = data["password"]
    return (usr_name, psw)

def init():
    display = _creat_display(DEBUG)
    browser = _set_browser()
    _message("init over.")
    return (browser, display)

def open_url(browser):
    _message("open login page ", end='')
    browser.get(URL)
    print("over.")
    tm.sleep(0.5)
    return browser

def check_login(browser:webdriver.Firefox) -> bool:
    page = browser.page_source

    for i in range(20):
        if "正在登录..." in page:
            tm.sleep(0.5)

        elif "ldap auth error" in page:
            _error("account or password error")
            return False

        else:
            page = browser.page_source
            url = browser.current_url

            if "您已经成功登录。" in page or\
            "You have successfully logged into our system." in page:
                return True
                
            elif url == "https://www.tyut.edu.cn/":
                return True
            
            else:
                return False
    
    print(page)
    _error("Timeout while waiting for a response")
    return False

def login(browser, usr_name:str, psw:str) -> None:
    ipts = browser.find_elements(By.CLASS_NAME, "edit_lobo_cell")
    _fill_in(ipts, usr_name, psw)
    _click_login(ipts)
    _message("login action over.")
    tm.sleep(0.5)
    return

def destroy(browser, display=None) -> None:
    browser.quit()
    if display:
        display.stop()
    _message("bye!")
    return

if __name__ == "__main__":
    usr_name, psw = load_data()
    browser, display = init()

    open_url(browser)
    if not check_login(browser):
        login(browser, usr_name, psw)
        open_url(browser)
        if check_login(browser):
            _message(f"success(using: {usr_name}).")
        else:
            _error("error.")
    else:
        _message("already loged in.")
        
    destroy(browser, display)
