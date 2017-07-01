import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def compose_url(first_name, last_name):
    return "https://www.linkedin.com/search/results/index/?keywords=" + first_name + "%20" + last_name + "%20buffalo&origin=GLOBAL_SEARCH_HEADER"

"""
basic housekeeping
"""
print("Setting up driver...\n")
chrome_path = r"C:\Zone\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
first_name = "ziyi"
last_name = "liu"
region = "buffalo"

# page = compose_url(first_name, last_name)
page = "https://www.linkedin.com"
driver.get(page)
print("crawling: " + page + "...\n")

"""
simulate login
"""
print("Log-in landing page...\n")
email = ""
password = ""
# click sign in button
driver.implicitly_wait(5)
login_email = driver.find_element_by_class_name("login-email")
login_password = driver.find_element_by_class_name("login-password")
sign_in_btn = driver.find_element_by_id("login-submit")

# input data then log in
print("Inputting credentials...\n")
login_email.clear()
login_email.send_keys(email)
login_password.clear()
login_password.send_keys(password)
sign_in_btn.click()

driver.implicitly_wait(5)

# start searching
print("start searching...\n")
search_bar = driver.find_element_by_css_selector(".ember-text-field.ember-view")
search_bar.clear()
search_bar.send_keys(first_name + " " + last_name + " " + region)
# driver.find_element_by_class_name("nav-search-button").click()
search_bar.send_keys(Keys.RETURN)

# wait result page to render
print("waiting page to render...\n")
driver.implicitly_wait(10)

# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, '.result__result-link.ember-view'))
# )

soup = bs.BeautifulSoup(driver.page_source, "lxml")
# print(soup)
print("soup is ready to serve!!\n")

scripts = soup.find_all("script")
for script in scripts:
    print(script)
# # wait result page to render
# print("Waiting result page to render")
# posts = WebDriverWait(driver, 5).until(lambda driver: driver.find_elements_by_css_selector(".search-result__result-link.ember-view"))
#
# print("Output all results with out filtering")
# for post in posts:
#     print(first_name + " " + last_name + " -> " + post.get_attribute("href"))
#
# print("Crawling complete")
