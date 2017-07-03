from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


"""
populate the result set with coarse-grain filtered result
for further evaluation
"""
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
    print("Coarse-grain filter: " + str(len(result_set)) + " candidates survived from coarse-grain filter")


"""
fine-grain filter that evaluates accuracy score of all candidate profile links
"""
def fine_filter(driver, result_set):
    """
    need to compare school, major, grad year, each worth 1 points
    """
    print("Fine-grain filter: checking " + str(len(result_set)) + " potential profile links...\n")
    for link in result_set:
        print("Clicked: " + link)
        driver.get(link)
        score = 0

        # find education data
        education_info = None
        try:
            education_info = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located( (By.XPATH,
            """//*[@data-control-name="background_details_school"]""") )
            )
        except TimeoutException:
            print("No education data found!!\n----------------------------------------------")
            continue

        print(str(len(education_info)) + " education data found")
        for education in education_info:
            # find school name
            school = education.find_element(By.TAG_NAME, "h3")
            school_name = school.text
            print(school_name.lower().replace(" ", ""))

            # find major info
            major_info = education.find_elements(By.CLASS_NAME, "pv-entity__comma-item")
            for major in major_info:
                print(major.text)

            # find graduation year
            grad_year = education.find_element(By.XPATH, "//time[2]")
            print("graduation year " + grad_year.text +
                  "\n----------------------------------------------")


def simulate_login(driver, email, password):
    # automated login process
    login_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "login-email"))
    )
    login_password = driver.find_element_by_class_name("login-password")
    sign_in_btn = driver.find_element_by_id("login-submit")

    # input credentials then log in
    print("Inputting credentials...\n")
    login_email.clear()
    login_email.send_keys(email)
    login_password.clear()
    login_password.send_keys(password)
    sign_in_btn.click()


def star_search(driver, first_name, last_name, region="buffalo"):
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, """//*[@class="ember-text-field ember-view"]"""))
    )

    search_bar.clear()
    search_bar.send_keys(first_name + " " + last_name + " " + region)
    search_bar.send_keys(Keys.RETURN)


def wait_result(driver):
    try:
        potential_divs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located( (By.XPATH, """//div[@class="search-result__info pt3 pb4 ph0"]""" ) )
        )
        return potential_divs
    except TimeoutException:
        print("No match!!")
        return []


def crawl_linkedin():

    """
    web driver set up
    """
    print("Setting up web driver...\n")
    chrome_path = r"C:\Zone\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    # phantomjs_path = r"C:\Zone\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    # driver = webdriver.PhantomJS(phantomjs_path)

    first_name = "junjie"
    last_name = "chen"

    page = "https://www.linkedin.com"
    driver.get(page)
    print("crawling: " + page + "\n")

    """
    simulate login
    """
    print("Log-in landing page...\n")
    email = "371000549@qq.com"
    password = "1313123"
    simulate_login(driver, email, password)

    # start searching
    print("Start searching...\n")
    star_search(driver, first_name, last_name)

    # wait result page to render
    print("Waiting page to render...\n")
    potential_divs = wait_result(driver)
    print(str(len(potential_divs)) + " potential candidate entering coarse-grain filter...\n")
    if len(potential_divs) == 0:
        return

    """
    coarse grain filter
    """
    result_set = set()
    coarse_filter(potential_divs, result_set, first_name + last_name)

    """
    fine grain filter
    """
    fine_filter(driver, result_set)

if __name__ == "__main__":
    crawl_linkedin()
