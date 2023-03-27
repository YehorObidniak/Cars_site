import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_project.settings")
django.setup()

from django.db import transaction
from cars_project.main.models import Car_any, Brands, regSpecs
from django.db.models import Q

import sqlite3 as sql
from custom_classes import Car
import os


class DbManager:
    def __init__(self):
        self.base = sql.connect(os.path.dirname(__file__) + "/../db.sqlite3")
        self.cur = self.base.cursor()
        if self.base:
            print("Database connected succesfully")

    def reset_active_field(self, domain):
        Car_any.objects.filter(site=domain).update(active=False)
        self.cur.execute(
            "UPDATE main_car_any SET active =(?2) WHERE site = (?1) ",
            (
                domain,
                0,
            ),
        )
        self.base.commit()

    def get_db_listings(self, site):
        self.cur.execute(
            "SELECT url, price FROM main_car_any WHERE site=(?)", (site,)
        ).fetchall()

        return Car_any.objects.filter(site=site).values()

    def remove_listings(self, url):
        Car_any.objects.filter(active=False).delete()
        self.cur.execute("DELETE FROM main_car_any WHERE active=(?)", (False,))
        self.base.commit()

    # TODO
    def get_sellers_ids(self):
        return self.cur.execute("SELECT id FROM main_car_any").fetchall()

    def upsert_listing(self, car: Car):
        #  old_price+' '+(?6)
        defaults = {}
        try:
            car_ = Car_any.objects.get(unique_field=car.url)
            defaults = {
                'price':car.price, 
                'old_price':car_.price + ' ' + car_.old_price,
                'where':Q('price' != car.price)
            }
        except:
            defaults = {
                # 'url':car.url,
                'brand':car.brand,
                'model':car.model, 
                'color':car.color, 
                'photo':car.photo, 
                'price':car.price, 
                'kms':car.kms, 
                'year':car.year, 
                'location':car.location, 
                'regSpecs':car.reg_specs,
                'activeListings':car.active_listings,
                'posted':car.posted,
                'site':car.domain,
                'contact':car.contact,
                'old_price':car.old_price,
                'active':True,
            }
            
        Car_any.objects.update_or_create(unique_field=car.url, defaults=defaults)
        self.cur.execute(
            "INSERT INTO main_car_any (url, brand, model, color, photo, price, kms, year, location, regSpecs, activeListings, posted, site, contact, old_price, active) values (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16) ON CONFLICT(url)"
            "DO UPDATE set old_price = price ||' '|| old_price, price = (?6) WHERE price != (?6)",
            (
                # "https://www.dubicars.com/2002-mercedes-benz-cls-500-552122.html",
                # "Mercedes-Benz",
                # "CLS 500",
                # "Grey/Silver",
                # "//www.dubicars.com/images/794e44/w_650x380/private-sellers/1ed487ab-f2cc-4938-891e-b3e964a19f24.jpg",
                # 21000,
                # 130000,
                # 2002,
                # "Al Ain",
                # "GCC",
                # 1,
                # "1678394193.8799658",
                # "Dubicars",
                # "tel:+971507730011",
                # "",
                # "True",
                car.url,
                car.brand,
                car.model,
                car.color,
                car.photo,
                car.price,
                car.kms,
                car.year,
                car.location,
                car.reg_specs,
                car.active_listings,
                car.posted,
                car.domain,
                car.contact,
                car.old_price,
                1,
                # " " + str(car.price),
            ),
        )
        Car_any.objects.filter(url=car.url).update(active=True)
        self.cur.execute(
            "UPDATE main_car_any SET active = (?1) WHERE url =(?2)", (1, car.url)
        ),
        self.base.commit()

    # def test(self):
    # sql_query = "DELETE FROM main_car_any url NOT IN (SELECT MIN(url) FROM lipo GROUP BY messdatum)"
    # self.cur.execute(sql_query)
    # self.base.commit()
    # sql_query = "SELECT url FROM main_car_any WHERE url IN (SELECT url FROM main_car_any GROUP BY url HAVING COUNT(*) > 1)"
    # sql_query = "SELECT url FROM main_car_any WHERE url ='https://uae.yallamotor.com/used-cars/mitsubishi/lancer/2016/used-mitsubishi-lancer-2016-sharjah-1391781'"
    # return self.cur.execute(sql_query).fetchall()
    # sql_query = "DELETE FROM main_car_any WHERE id IN (SELECT id FROM main_car_any GROUP BY url HAVING COUNT(*) > 1)"
    # self.cur.execute(sql_query)
    # self.base.commit()
    # return self.cur.execute(
    #     "SELECT url FROM main_car_any WHERE id IN (SELECT id FROM main_car_any GROUP BY url HAVING COUNT(*) > 1)"
    # ).fetchall()

    def get(self):
        # self.cur.execute("ALTER TABLE main_car_any ADD COLUMN old_price TEXT")
        # self.base.commit()
        # return self.cur.execute(
        #     "SELECT url FROM main_car_any WHERE site='Dubizzle' AND active IS NULL OR active = ''"
        # ).fetchall()
        self.cur.execute(
            "SELECT url FROM main_car_any WHERE site='Dubizzle' AND active = 0"
        ).fetchall()
        return Car_any.objects.filter(site='Dubizzle').filter(active=False)

    # return self.cur.execute("ALTER TABLE main_car_any DROP COLUMN id")

    # def add_column(self):
    #     sql_query = "ALTER TABLE main_car_any ADD old_price INTEGER"
    #     self.cur.execute(sql_query)
    #     sql_query = "ALTER TABLE main_car_any ADD active BOOLEAN"
    #     self.cur.execute(sql_query)
    #     sql_query = "ALTER TABLE main_car_any RENAME COLUMN price to current_price"
    #     self.cur.execute(sql_query)

    # upsert_listing()


# with open("not_active_links.txt", "w+") as file:
#     res = DbManager().get()
#     for i in res:
#         file.write(i[0] + "\n")
# print(DbManager().reset_active_field("Dubizzle"))
