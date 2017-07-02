import bs4 as bs
from selenium import webdriver

def evaluate_score(head_text, top_section, short_story, major):
    print("Evaluating " + head_text + " ...")
    suny = "stateuniversityofnewyorkatbuffalo"
    ub = "universityatbuffalo"
    region = "buffalo"
    score = 0
    if suny in top_section or ub in top_section:
        score+=2
    elif region in top_section:
        score+=1
    if major in top_section:
        score+=1

    if suny in short_story or ub in short_story:
        score+=2
    elif region in short_story:
        score+=1
    if major in short_story:
        score+=1

    print("Final score " + str(score) +
          "\n---------------------------------------------------------")
    return score

def compose_url(first_name, last_name):
    return "https://www.google.com/search?q=site%3Awww.linkedin.com%2Fin+" + first_name + "+" + last_name + "+buffalo"

# set up driver
print("setting up driver...")
first_name = ""
last_name = ""
major = ""
chrome_path = r"C:\Zone\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get(compose_url(first_name, last_name))

# feed the source page to soup
print("making soup...")
soup = bs.BeautifulSoup(driver.page_source, "html.parser")

#grab all g class
file = open("result.txt", 'a')
file.write("Possible match for [ " + first_name[0].upper() + first_name[1:]
           + " " + last_name[0].upper() + last_name[1:]
           + " ]\n---------------------------------------------------------\n\n")
print("printing all \"g\" class in searching " + first_name + " " + last_name + "\n" +
      "---------------------------------------------------------")
all_g = soup.find_all("div", class_="g")
for g in all_g:
    inner_anchor = g.find("h3", class_="r").find("a")
    """
    check head text
    """
    head_text = inner_anchor.text.lower()
    if first_name + " " + last_name not in head_text:
        continue

    """
    check profile link, filter languages other than EN
    """
    profile_link = inner_anchor["href"]
    sub_link = profile_link[profile_link.find("/in/")+4:]

    if "/" in sub_link:
        continue

    """
    format top section and short story for evaluation
    """
    top_section = g.find("div", class_="slp f").text.lower().replace(" ", "")
    short_story = g.find("span", class_="st").text.lower().replace(" ", "")
    score = evaluate_score(head_text, top_section, short_story, major)
    file.write("Accuracy Score: " + str(score) + "\n" + profile_link + "\n\n")


