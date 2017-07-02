import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# def cralw_linkedin():
"""
basic housekeeping
"""
print("Setting up driver...\n")
chrome_path = r"C:\Zone\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
first_name = ""
last_name = ""
region = ""

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
# automated login process
login_email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "login-email"))
)
login_password = driver.find_element_by_class_name("login-password")
sign_in_btn = driver.find_element_by_id("login-submit")

# input data then log in
print("Inputting credentials...\n")
login_email.clear()
login_email.send_keys(email)
login_password.clear()
login_password.send_keys(password)
sign_in_btn.click()

# start searching
print("Start searching...\n")

search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, """//*[@class="ember-text-field ember-view"]""" ))
)
search_bar.clear()
search_bar.send_keys(first_name + " " + last_name + " " + region)
search_bar.send_keys(Keys.RETURN)

# wait anchor page to render
print("Waiting page to render...\n")
result_divs = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located( (By.XPATH, """//div[@class="search-result__info pt3 pb4 ph0"]""" ) )
)
print("result list size: " + str(len(result_divs)))

for div in result_divs:
    inner_anchor = div.find_element(By.TAG_NAME, "a")


    inner_h3 = inner_anchor.find_element(By.TAG_NAME, "h3")
    inner_h3_id = inner_h3.get_attribute("id")

    inner_span = inner_anchor.find_element(By.XPATH, "//*[@id=\"" + inner_h3_id + "\"]/span[1]/span" )
    inner_span_text = inner_span.text
    if first_name+last_name in inner_span_text.lower().replace(" ", ""):
        print(inner_span_text + ":")
        print(inner_anchor.get_attribute("href") + "\n")


# if __name__ == "__main__":
#     cralw_linkedin()
