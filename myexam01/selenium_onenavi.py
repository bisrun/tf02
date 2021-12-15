#install
#
#pip install selenium
#pip install beautifulsoup4
#pip install lxml

from selenium import webdriver

driver = webdriver.Chrome('./driver/chromedriver.exe')

driver.get("https://map.gis.kt.com/indexPC.html?v=1555571177015")

myCenter = driver.execute_script("_map.getCenter")
