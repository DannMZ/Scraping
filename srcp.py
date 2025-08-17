
from dotenv import load_dotenv as start
from selenium import webdriver as dr
from selenium.webdriver.firefox.service import Service as srvs
from webdriver_manager.firefox import GeckoDriverManager as gdm

import os

start()
myUrl=os.getenv('Base_Url')
if not myUrl: raise ValueError("There'sn't url")
else:print("Url exists")

test_dr=  dr.Firefox(service=srvs(gdm().install()))

test_dr.get(myUrl)

