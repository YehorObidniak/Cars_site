import requests
from bs4 import BeautifulSoup
import json
from requestParams import getParametersForRequest
from datetime import datetime as dt
from dbManager import DbManager
import time
import html_processing


def testing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        print(time.time() - start_time)
        return res

    return wrapper


class Car:
    def __init__(
        self,
        url="",
        brand="",
        model="",
        color="",
        photo="",
        name="",
        price="",
        year="",
        location="",
        reg_specs="",
        kms="",
        active_listings="",
        contact="",
        posted="",
    ):
        self.url = url
        self.name = name
        self.brand = brand
        self.model = model
        self.color = color
        self.photo = photo
        self.price = price
        self.year = year
        self.kms = kms
        self.location = location
        self.reg_specs = kms
        self.active_listings = active_listings
        self.contact = contact
        self.posted = posted


class Site:
    def __init__(self, domain):
        self.domain = domain
        self.activeListingsCount = 0

    def get_new_links(self):
        pass

    def scan_price(self):
        pass

    def update(self):
        pass


class Dubizzle(Site):
    def __init__(self, domain):
        self.lastTimeChecked = 0
        self.db_manager = DbManager()
        super().__init__(domain)

    def update(self):
        current_web_listings = self.__parse_website()
        print(current_web_listings)
        # current_db_listings = self.db_manager.get_db_listings("Dubizzle")
        self.__process_listings(current_web_listings)

        # self.__remove_deleted_listings(current_web_listings, current_db_listings)
        # self.__check_prices(current_web_listings, current_db_listings)
        # self.__get_new_listings(current_web_listings, current_db_listings)

    def __process_listings(self, current_web_listings):
        # self.db_manager.reset_active_field()
        for web_listing in current_web_listings:
            self.db_manager.upsert_listing(
                Car(
                    url=web_listing["url"],
                    brand=web_listing["make"],
                    model=web_listing["model"],
                    color=web_listing["color"],
                    photo=web_listing["photo"],
                    price=web_listing["price"],
                    kms=web_listing["kilometers"],
                    posted=web_listing["posted"],
                    reg_specs=web_listing["reg_specs"],
                    location=web_listing["location"],
                    year=web_listing["year"],
                )
            )
            # print(web_listing)

    def __parse_website(self):
        # starting from first page
        data_list = []
        i = 1
        while i <= self.activeListingsCount / 200 + 1:
            self.headers, self.link, self.data = getParametersForRequest(
                i=i, domain="Dubizzle"
            )
            response = requests.post(
                url=self.link,
                headers=self.headers,
                data=self.data,
            )
            json_obj = json.loads(response.text)
            self.activeListingsCount = json_obj["results"][0]["nbHits"]
            for j in json_obj["results"][0]["hits"]:
                data_list.append(self.__format_json(j))
            i += 1
        return data_list
        # {'url': 'https://abudhabi.dubizzle.com/motors/used-cars/hyundai/sonata/2023/3/15/hyundai-sonata-2019-full-options24-l-2400--3-896---7df80d33d11a457f8c826619442448f3/', 'make': 'Hyundai', 'model': 'Sonata', 'color': 'Silver', 'photo': 'https://dbz-images.dubizzle.com/images/2023/03/15/c67fc35fa3c2419baa9b8d80bc293d3d-.jpeg?impolicy=legacy&imwidth=480', 'price': 78000, 'kilometers': 50000, 'posted': '03/15/2023, 02:30:34', 'reg_specs': 'GCC Specs', 'location': 'Abu Dhabi', 'listing_id': '7df80d33d11a457f8c826619442448f3', 'category': 140, 'year': 2019}, {'url': 'https://dubai.dubizzle.com/motors/used-cars/mercedes-benz/slk-class/2023/3/13/mercedes-benz-slk-200-perfect-condition-2-222---af679cbe0adb4efea67ad6343b26b607/', 'make': 'Mercedes-Benz', 'model': 'SLK-Class', 'color': 'Red', 'photo': 'https://dbz-images.dubizzle.com/images/2023/03/13/0c99f5f477e243419931ef985f54e3e5-.jpeg?impolicy=legacy&imwidth=480', 'price': 20000, 'kilometers': 135236, 'posted': '03/15/2023, 01:32:16', 'reg_specs': 'GCC Specs', 'location': 'Dubai', 'listing_id': 'af679cbe0adb4efea67ad6343b26b607', 'category': 140, 'year': 2009}

    def __get_new_listings(self, current_web_listings, current_db_listings):
        pass

    def __check_prices(self, current_web_listings, current_db_listings):
        for web_listing in current_web_listings:
            # TODO sql query as dict with urls as
            if web_listing["price"] != current_db_listings["url"]["price"]:
                self.db_manager.change_price(
                    url=web_listing["url"],
                    old_price=current_db_listings["url"]["price"],
                    new_price=web_listing["price"],
                )
            else:
                pass

    def __get_listers_phone(self, web_listing):
        listers_ids = self.db_manager.get_sellers_ids()
        if web_listing["lister_id"] in listers_ids:
            web_listing["phone"] = self.db_manager.get_lister_id
        # else:
        #     make phone request

    def __format_json(self, data):
        items = {}
        def_dict = {"en": {"value": ""}}
        default_value = "Not mentioned"
        items["url"] = data["absolute_url"]["en"]
        items["make"] = data["details"]["Make"]["en"]["value"]
        items["model"] = data["details"]["Model"]["en"]["value"]
        items["color"] = data["details"].get("Exterior Color", def_dict)["en"]["value"]
        photo_thumbnails = data["photo_thumbnails"]
        items["photo"] = photo_thumbnails[0] if photo_thumbnails else default_value
        items["price"] = data["price"]
        items["kilometers"] = data["details"]["Kilometers"]["en"]["value"]
        items["posted"] = dt.fromtimestamp(data["added"]).strftime("%m/%d/%Y, %H:%M:%S")
        items["reg_specs"] = data["details"]["Regional Specs"]["en"]["value"]
        items["location"] = data["site"]["en"]
        items["listing_id"] = data["uuid"]
        items["category"] = data["category_v2"]["ids"][0]
        items["year"] = data["details"]["Year"]["en"]["value"]
        return items

    # def
    # cars_link = []
    # headers, link, data = getParametersForRequest()
    # for j in temp_json_data["results"]["hits"]:
    #     cars_link.append(j["absolute_url"]["en"])
    # for i in range(self.activeListingsCount + 1 / 333 + 1):
    #     if i == 0:


# class Yallamotor(Site):


class Dubicars(Site):
    def __init__(self, domain):
        self.lastTimeChecked = 0
        self.db_manager = DbManager()
        self.activeListingsCount = 0
        self.html_processor = html_processing.DubicarsHTMLProcessor()
        super().__init__(domain)

    def update(self):
        current_web_links = self.__get_web_links()
        cars_dicts = self.__get_data_from_web_links(current_web_links)
        return cars_dicts

    def __get_web_links(self):
        # starting from first page
        self.headers = getParametersForRequest()
        i = 1
        urls = []
        while i <= self.activeListingsCount / 30 + 1:
            response = requests.get(
                f"https://www.dubicars.com/search?view=&ms=yes&o=&ul=AE&ma=&mo=0&b=&set=bu&pf=&pt=100000&emif=&emit=&c=used&yf=&yt=&kf=&kt=160000&eo=not-for-export&stsd=&cr=AED&cy=&co=&s=&gi=&f=&g=&l=&st=private&page={i}",
                headers=self.headers,
            )
            self.__update_active_listings(response.text)
            soup = BeautifulSoup(response.text, "lxml")
            links = soup.find_all("a", class_="image-container d-block")
            for link in links:
                urls.append(link["href"])
            i += 1
        return urls

    def __get_data_from_web_links(self, current_web_links):
        res = self.html_processor.get_cars_dict(current_web_links)
        return res

    def __update_active_listings(self, html):
        soup = BeautifulSoup(html, "lxml")
        self.activeListingsCount = int(
            soup.find("span", {"class": "count"}).text.replace(" Results found", "")
        )


# start_time=time.time()
# d = Dubizzle("123")
# print(d.update())
# obj = d.update()
# print(Dubicars("Dubicars").update())
print(Dubizzle("Dubizzle").update())
# with open("example_dubizzle_response.json", "w+", encoding="utf-8") as file:
#     json.dump(obj, file, ensure_ascii=False)
