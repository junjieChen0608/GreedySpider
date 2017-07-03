from crawl_linkedin import LinkedinCrawler

first_name = input("Please enter first name:")
last_name = input("Please enter last name:")
myCrawler = LinkedinCrawler(first_name, last_name)
myCrawler.crawl_linkedin()