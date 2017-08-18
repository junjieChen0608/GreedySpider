"""
Please read me if you are a developer

You need to:
1, No doubt that you need to install Chrome Webdriver and Selenium in order to get the whole program running
2, change the Chrome Webdriver path to your own path in the setup_driver()
3, fill in dummy Linkedin account before the call of simulate_login()

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import random


class LinkedinCrawler:
    def __init__(self, info_dict, file_path):
        # TODO change constructor signature to a dictionary and a file path string
        self.first_name = ""
        self.last_name = ""
        if file_path == "":
            self.first_name = info_dict["firstName"].lower()
            self.last_name = info_dict["lastName"].lower()
        self.driver = None

    """
    randomly pause for few seconds, make it slow and steady
    """
    def random_pause(self):
        random.seed()
        to_pause = random.randint(1, 5)
        self.driver.implicitly_wait(to_pause)

    """
    web driver set up
    """
    def setup_driver(self, page):
        print("\nSetting up web driver...\n")
        # TODO change your own chrome webdriver path
        chrome_path = r"C:\Zone\ChromeDriver\chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_path)
        self.driver.get(page)

    """
    simulate login
    """
    def simulate_login(self, email, password):
        if email == "" or password == "":
            print("email and password cannot be empty.")
            raise RuntimeError

        # automated login process
        login_email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-email"))
        )
        login_password = self.driver.find_element_by_class_name("login-password")
        sign_in_btn = self.driver.find_element_by_id("login-submit")

        # input credentials then log in
        print("Inputting credentials...\n")
        login_email.clear()
        login_email.send_keys(email)
        login_password.clear()
        login_password.send_keys(password)
        sign_in_btn.click()


    """
    start searching
    """
    def start_search(self, region="buffalo"):

        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//*[@class="ember-text-field ember-view"]"""))
        )

        search_bar.clear()
        search_bar.send_keys(self.first_name + " " + self.last_name + " " + region)
        search_bar.send_keys(Keys.RETURN)

    """
    wait result page to render
    """
    def wait_result(self):

        try:
            potential_divs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, """//div[@class="search-result__info pt3 pb4 ph0"]"""))
            )
            return potential_divs
        except TimeoutException:
            print("No match!!")
            return []

    """
    populate the result set with coarse-grain filtered result
    for further evaluation, Linkedin occasionally returns irrelevant search results for unknown reason
    """
    def coarse_filter(self, potential_divs, result_set):

        for div in potential_divs:
            inner_anchor = div.find_element(By.TAG_NAME, "a")
            profile_link = inner_anchor.get_attribute("href")

            inner_h3 = inner_anchor.find_element(By.TAG_NAME, "h3")
            inner_h3_id = inner_h3.get_attribute("id")

            inner_span = inner_anchor.find_element(By.XPATH, "//*[@id=\"" + inner_h3_id + "\"]/span[1]/span")
            inner_span_text = inner_span.text.lower().replace(" ", "")
            if self.first_name in inner_span_text and self.last_name in inner_span_text:
                result_set.add(profile_link)
        print(str(len(result_set)) + " candidates survived from coarse-grain filter")

    """
    fine-grain filter that evaluates accuracy score of all candidate profile links
    """
    def fine_filter(self, result_set):
        # TODO design scoring mechanism

        print("Checking " + str(len(result_set)) + " potential profile links...\n")
        print("--------------------------------------------------------------------------------------------")
        for link in result_set:
            print("Clicked: " + link)
            self.driver.get(link)
            score = 0

            # find education data
            education_info = None
            try:
                education_info = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH,
                                                         """//*[@data-control-name="background_details_school"]"""))
                )
            except TimeoutException:
                print("No education data found!!\n--------------------------------------------------------------------------------------------")
                continue

            print(str(len(education_info)) + " education data found\n")
            for education in education_info:
                # find school name
                school = education.find_element(By.TAG_NAME, "h3")
                school_name = school.text
                print(school_name)

                # find major info
                major_info = education.find_elements(By.CLASS_NAME, "pv-entity__comma-item")
                for major in major_info:
                    print(major.text)

                # find graduation year
                grad_years = education.find_elements(By.TAG_NAME, "time")
                grad_year = ""
                if len(grad_years) == 2:
                    grad_year = grad_years[1].text
                    print("graduation year: " + grad_year + "\n")
            print("--------------------------------------------------------------------------------------------")

    def crawl_utl(self):
        print("Start searching...\n")
        self.start_search()

        print("Waiting page to render...\n")
        potential_divs = self.wait_result()
        print(str(len(potential_divs)) + " potential candidate entering coarse-grain filter")
        if len(potential_divs) == 0:
            return

        """
        coarse grain filter
        """
        result_set = set()
        self.coarse_filter(potential_divs, result_set)

        """
        fine grain filter
        """
        self.fine_filter(result_set)

    def crawl_linkedin(self):

        page = "https://www.linkedin.com"
        print("crawling: " + page)
        self.setup_driver(page)

        print("Log-in landing page...\n")
        email = "371000549@qq.com"
        # TODO put password here
        password = ""
        self.simulate_login(email, password)

        # TODO loop this function if need to do multiple search
        self.crawl_utl()

        # finally, close the web browser
        self.driver.close()
        print("Crawling complete")
