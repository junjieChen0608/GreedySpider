from crawler import LinkedinCrawler

info_dict = {
    "firstName" : "",
    "lastName" : "",
    "schoolName" : "",
    "degree" : "",
    "major" : "",
    "gradYear" : ""
}
info_dict["firstName"] = input("Please enter first name:")
info_dict["lastName"] = input("Please enter last name:")
myCrawler = LinkedinCrawler(info_dict, "")
myCrawler.crawl_linkedin()