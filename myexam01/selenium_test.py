#install
#
#pip install selenium
#pip install beautifulsoup4
#pip install lxml

from selenium import webdriver

driver = webdriver.Chrome('./driver/chromedriver.exe')
driver.get("https://nid.naver.com/nidlogin.login")

driver.save_screenshot('./data/001.png')
elem_login = driver.find_element_by_id("id")
elem_login.clear()
elem_login.send_keys("bisrun")

elem_pwd = driver.find_element_by_id("pw")
elem_pwd.clear()
elem_pwd.send_keys("nr74popo00")

xpath = """//*[@id="frmNIDLogin"]/fieldset/input"""
driver.find_element_by_xpath(xpath).click()

driver.get("http://mail.naver.com")

from bs4 import BeautifulSoup
html = driver.page_source
#soup = BeautifulSoup(html, features="xml")
soup= BeautifulSoup(html,'html.parser')
soup = BeautifulSoup(html, 'lxml')
raw_list = soup.find_all('div', 'name _ccr(lst.from)') #space 딱 맞춰야 함.
send_list = [each.a.string for each in soup.find_all('div', 'name _ccr(lst.from)')]
driver.close()