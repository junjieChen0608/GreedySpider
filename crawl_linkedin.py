from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def coarse_filter(potential_divs, result_set, fullname):
    for div in potential_divs:
        inner_anchor = div.find_element(By.TAG_NAME, "a")
        profile_link = inner_anchor.get_attribute("href")
        inner_h3 = inner_anchor.find_element(By.TAG_NAME, "h3")
        inner_h3_id = inner_h3.get_attribute("id")

        inner_span = inner_anchor.find_element(By.XPATH, "//*[@id=\"" + inner_h3_id + "\"]/span[1]/span" )
        inner_span_text = inner_span.text
        if fullname in inner_span_text.lower().replace(" ", ""):
            result_set.add(profile_link)
            # print(inner_span_text + ":")
            # print(profile_link + "\n")


def fine_filter(driver, result_set):

    """
    need to compare school, major, grad year, each worth 1 points
    """
    print("Checking " + str(len(result_set)) + " potential profile links...\n")
    for link in result_set:
        print("Clicked: " + link)
        driver.get(link)
        score = 0
        # find education data
        degree_info = None
        try:
            degree_info = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located( (By.XPATH, """//div[@class="pv-entity__degree-info"]""") )
            )
        except TimeoutException:
            print("No education data found!!")
            continue
        print(str(len(degree_info)) + " education data found")
        # find school name and major
        school_name = ""
        major = ""
        for degree in degree_info:
            school_name = degree.find_element(By.TAG_NAME, "h3")
            print(school_name.text)




def crawl_linkedin():

    """
    basic housekeeping
    """
    print("Setting up driver...\n")

    chrome_path = r"C:\Zone\Chrome Webdriver\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    # phantomjs_path = r"C:\Zone\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    # driver = webdriver.PhantomJS(phantomjs_path)

    driver.maximize_window()
    first_name = ""
    last_name = ""
    region = "buffalo"

    # page = compose_url(first_name, last_name)
    page = "https://www.linkedin.com"
    driver.get(page)
    print("crawling: " + page + "\n")

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

    # wait result page to render
    print("Waiting page to render...\n")
    potential_divs = None
    try:
        potential_divs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located( (By.XPATH, """//div[@class="search-result__info pt3 pb4 ph0"]""" ) )
        )
    except TimeoutException:
        print("No match!!")
        return

    print("Coarse grain filter from " + str(len(potential_divs)) + " potential candidate...\n")
    result_set = set()

    """
    coarse grain filter
    """
    coarse_filter(potential_divs, result_set, first_name + last_name)

    """
    fine grain filter
    """
    fine_filter(driver, result_set)

if __name__ == "__main__":
    crawl_linkedin()
