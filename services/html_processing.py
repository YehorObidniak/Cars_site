import bs4
import json
import requests
from fake_useragent import UserAgent
import concurrent.futures


class DubicarsConcurrentProcessor:
    def __init__(self):
        self.ua = UserAgent()
        self.html_processor = DubicarsHTMLProcessor()

    def get_html_from_urls(self, urls):
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            result_gen = executor.map(self.__get_html_from_link, urls)
        final_result = [i for i in result_gen]
        return final_result

    def __get_html_from_link(self, url):
        response = requests.get(url)
        res_dict = self.html_processor.process_html(response.text)
        return res_dict


class HTMLProcessor:
    def __init__(self):
        pass

    def process_html(self):
        pass


# class YallaHTMLProcessor(HTMLProcessor):
#     def process_html(html):
#         soup = bs4.BeautifulSoup(html.text)


class DubicarsHTMLProcessor(HTMLProcessor):
    def get_cars_dict(self, urls):
        return DubicarsConcurrentProcessor().get_html_from_urls(urls)

    def process_html(self, html):
        soup = bs4.BeautifulSoup(html, "lxml")
        if soup.find("h3", {"class": "text-default"}, string="Sold") is None:
            try:
                links = soup.find_all("script", {"type": "application/ld+json"})[2]
                data = json.loads(links.text)
                items = {}
                items["url"] = data["offers"]["url"]
                items["brand"] = data["brand"]
                items["model"] = data["model"]
                items["color"] = data["color"]
                items["photo"] = data["image"]
                items["photo"] = soup.find("source", {"media": "(max-width:600px)"})[
                    "srcset"
                ]
                items["price"] = data["offers"]["price"]
                items["phone"] = (
                    soup.find("section", {"id": "call-dealer"})
                    .find("div", class_="content")
                    .find("a")["href"]
                )
                temp_ul = soup.find("ul", class_="dc-highlight-list")
                items["kms"] = temp_ul.find_all("li")[1].find_all("span")[1].text
                items["location"] = temp_ul.find_all("span")[7].text
                items["regSpecs"] = temp_ul.find_all("span")[9].text.strip()
                items["modelDate"] = data["vehicleModelDate"]
                return items
            except IndexError:
                items = {}
                items["url"] = soup.find(
                    "link", {"hreflang": "en", "rel": "alternate"}
                )["href"]
                temp = soup.find("ul", class_="faq__data").find_all("li")
                items["brand"] = temp[0].find_all("span")[1].text
                items["model"] = temp[1].find_all("span")[1].text
                items["color"] = temp[2].find_all("span")[1].text
                items["photo"] = soup.find(
                    "meta", {"property": "og:image", "itemprop": "image"}
                )["content"]
                items["photo"] = soup.find("source", {"media": "(max-width:600px)"})[
                    "srcset"
                ]
                items["price"] = soup.find("strong", class_="price text-primary").text
                temp_ul = soup.find("ul", class_="dc-highlight-list")
                items["kms"] = temp_ul.find_all("li")[1].find_all("span")[1].text
                items["location"] = temp_ul.find_all("span")[7].text
                items["modelDate"] = temp_ul.find_all("span")[1].text
                items["phone"] = (
                    soup.find("section", {"id": "call-dealer"})
                    .find("div", class_="content")
                    .find("a")["href"]
                )
                try:
                    items["regSpecs"] = temp_ul.find_all("span")[9].text.strip()
                except:
                    items["regSpecs"] = (
                        soup.find("li", {"class": "icon-cog"})
                        .find_all("span")[1]
                        .text.strip()
                    )
                return items
            except Exception as e:
                print(e)
        else:
            print(soup.find("link", {"hreflang": "en", "rel": "alternate"})["href"])
