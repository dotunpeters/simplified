
"""
Scrape data from Jumia and Konga.
Add data to file.
Add data to database.
"""

from requests_html import HTML, HTMLSession
from time import perf_counter
from multiprocessing import Process
from csv import writer
from models import *
import app
import custom_config
import os

#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

session = HTMLSession()

def jumia(categ, url):
    """ Scrapes jumia products """
    print(f"scrapping {categ} on {url}")

    #list params
    name = ""
    sku = ""
    price = ""
    stars = 0
    link = ""
    image_url = ""
    reviews = 0
    seller = "jumia"
    category = categ
    description = ""
    counter = 0
    score = 0

    #scrape
    initial = session.get(url)
    if (initial.status_code == 200):
        rawcount = initial.html.find("body > main > section.osh-content > section.pagination > ul > li:nth-child(5) > a", first=True)
        count = int(rawcount.text)

    for i in range(count):
        response = session.get(f"{url}?page={i+1}")
        if (response.status_code == 200):

            try: 
                section = response.html.find(".products", first=True)
                products = section.find(".sku")
            except Exception as e:
                continue

            for product in products:
                counter += 1
                try:
                    #get sku
                    sku = product.attrs['data-sku']

                except Exception as e:
                    continue

                linker = product.find(".link", first=True)

                try:
                    #get link
                    link = linker.attrs['href']

                except Exception as e:
                    continue

                title = linker.find(".title", first=True)
                brand = title.find(".brand", first=True).text
                prename = title.find(".name", first=True).text

                #get name
                name = f"{brand} {prename}"

                price_container = linker.find(".price-container", first=True)
                price_box = price_container.find(".price-box", first=True)
                pricer = price_box.find(".price", first=True)

                #get price
                price = pricer.text.strip("₦").strip(" ")

                try:
                    rating_stars = linker.find(".rating-stars", first=True)
                    total_ratings = rating_stars.find(".total-ratings", first=True)
                    rawreview = int(total_ratings.text.strip("(").strip(")"))
                    
                    if (rawreview < 5):
                        continue
                    else:

                        #get reviews
                        reviews = rawreview

                except Exception as e:
                    continue

                each = session.get(link)
                if (each.status_code == 200):
                    main_imgs = each.html.find(".sldr", first=True)

                    try:
                        a_imgs = main_imgs.find("a", first=True)
                        imgs = a_imgs.find("img", first=True)
                    except Exception as e:
                        continue

                    #get image_url
                    image_url = imgs.attrs['data-src']

                    features = each.html.find("#jm > main > div:nth-child(3) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(1)", first=True)

                    new = each.html.find("#jm > main > div:nth-child(3) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(2) > div", first=True)

                    try:
                        #get description
                        describe = f"{features.text}\n{new.text}"
                        description = describe.strip(" ").lstrip("Key Features").replace("\n", "\t")

                    except Exception as e:
                        continue

                    rawstar = each.html.find("#jm > main > div:nth-child(3) > div.col12 > section:nth-child(5) > div.row.-fw-nw > div.col4.-phm > div > div.-fs29.-yl5.-pvxs > span", first=True)

                    try:
                        if (float(rawstar.text) < float(2.5)):
                            continue
                        else:
                            #get stars
                            stars = float(rawstar.text)

                            score += 1
                            each = [name, sku, price, stars, link, image_url, reviews, seller, category, description]
                            
                            #write to file
                            try:
                                with open("products.csv", 'a', encoding="utf-8") as product_file:
                                    product_filewrite = writer(product_file)
                                    product_filewrite.writerow(each)
                                    print(f"-> SUCS fileWRITE-> write successfully Jumia | {categ} | {name[0:10]} to file...")
                            except Exception as e:
                                print(f"-> ERR fileWRITE-> could not add Jumia|{categ}|{name[0:10]} to file: {e}")

                            #write to database
                            try:
                                with app.app_context():
                                    item = Products(name=name, sku=sku, price=price, stars=stars, link=link, image_url=image_url, reviews=reviews, seller=seller, category=category, description=description)
                                    db.session.add(item)
                                    db.session.commit()
                                    print(f"-> SUCS dbADD-> added successfully Jumia|{categ}|{name[0:10]} to database")
                            except Exception as e:
                                print(f"-> ERR dbADD-> could not add Jumia|{categ}|{name[0:10]} to database: {e}")
                            
                    except Exception as e:
                        continue

    print(f"-> END: Jumia | {categ} | counts: {score} of {counter}")



def konga(categ, url):
    """ Scrapes konga products """
    print(f"scrapping {categ} on {url}")

    #list params
    name = ""
    sku = ""
    price = ""
    stars = 0
    link = ""
    image_url = ""
    reviews = 0
    seller = "konga"
    category = categ
    description = ""
    counter = 0
    score = 0

    #scrape
    initial = session.get(url)
    if (initial.status_code == 200):
        rawcount = initial.html.find("#mainContent > section._9cac3_2I9l4 > section > section > div > ul > li:nth-child(4) > a", first=True)
        count = int(rawcount.text)

    for i in range(count):
        response = session.get(f"{url}?page={i+1}")
        if (response.status_code == 200):
            section = response.html.find("#mainContent > section._9cac3_2I9l4 > section > section > section > section > ul", first=True)
            products = section.find("li")

            for product in products:
                each = product.find("div", first=True)
                next_each = each.find("div", first=True)
                diver = next_each.find("div", first=True)
                linker = diver.find("a", first=True)

                #get link
                link = f"https://www.konga.com{linker.attrs['href']}"

                next_down_each = next_each.find("._4941f_1HCZm", first=True)
                former = next_down_each.find("form", first=True)

                reviewer = former.find(".ccc19_2IYt0", first=True)
                next_deep = reviewer.find('.a455c_3G0na', first=True)
                deep_span = next_deep.find('.eea9b_1Ma8-', first=True)

                counter += 1
                if deep_span.text.strip("(").strip(")") == "No reviews yet":
                    continue
                else: 
                    #get reviews
                    reviews = int(deep_span.text.strip("Review").strip("Reviews").strip(" "))
                    if reviews < 5:
                        continue

                each = session.get(link)
                if (each.status_code == 200):
                    namer = each.html.find("#mainContent > div > div.d9549_IlL3h > div._8f9c3_230YI._47f1e_1dZrT > div._680e2_KPkEz > div > h4", first=True)

                    #get name
                    name = namer.text

                    skuer = each.html.find("#mainContent > div > div.d9549_IlL3h > div._8f9c3_230YI._47f1e_1dZrT > div._680e2_KPkEz > div > form > div._31c33_NSdat > div._97fc0_3W515.b50e0_1HOLM > span", first=True)

                    #get sku
                    sku = skuer.text

                    pricer = each.html.find("#mainContent > div > div.d9549_IlL3h > div._8f9c3_230YI._47f1e_1dZrT > div._680e2_KPkEz > div > form > div._3924b_1USC3._16f96_38E1t > div._3924b_1USC3 > div._678e4_e6nqh", first=True)

                    #get price
                    price = pricer.text.strip("₦")

                    imager = each.html.find("#mainContent > div > div.d9549_IlL3h > div._8f9c3_230YI._47f1e_1dZrT", first=True)
                    pictr = imager.find(".bf1a2_3kz7s", first=True).find("._3a8a4_3Bhwv", first=True).find(".fd8e9_1qWnZ", first=True)
                    pictr = pictr.find("._7f96a_3PgMp", first=True)
                    pictr = pictr.find("img", first=True)

                    #get image_url
                    image_url = pictr.attrs['src']

                    #get description
                    describe = each.html.find("#mainContent > div > div.d9549_IlL3h > div._227af_AT9tO > div._79826_3-pAs > div._3383f_1xAuk > div > div", first=True).text
                    description = describe.strip(" ").replace("\n", "\t")

                    starer = each.html.find("#mainContent > div > div.d9549_IlL3h > div._8f9c3_230YI._47f1e_1dZrT > div._680e2_KPkEz > div > form > div._31c33_NSdat > div.a455c_3G0na.af1a1_3wVPH", first=True)

                    try:
                        starcount = 0
                        svgs = starer.find("svg")
                        for svg in svgs:
                            if (svg.attrs['class'][0] == "ba6f2_18Jb4"):
                                starcount += 1

                        #get stars
                        stars = starcount

                        score += 1
                        each = [name, sku, price, stars, link, image_url, reviews, seller, category, description]
                        
                        #write to file
                        try:
                            with open("products.csv", 'a', encoding="utf-8") as product_file:
                                product_filewrite = writer(product_file)
                                product_filewrite.writerow(each)
                                print(f"-> SUCS fileWRITE-> write successfully Konga | {categ} | {name[0:10]} to file...")
                        except Exception as e:
                            print(f"-> ERR fileWRITE-> could not add Konga|{categ}|{name[0:10]} to file: {e}")

                        #write to database
                        try:
                            with app.app_context():
                                item = Products(name=name, sku=sku, price=price, stars=stars, link=link, image_url=image_url, reviews=reviews, seller=seller, category=category, description=description)
                                db.session.add(item)
                                db.session.commit()
                                print(f"-> SUCS dbADD-> added successfully Konga|{categ}|{name[0:10]} to database")
                        except Exception as e:
                            print(f"-> ERR dbADD-> could not add Konga|{categ}|{name[0:10]} to database: {e}")

                    except Exception as e:
                        continue

    print(f"-> END: konga | {categ} | counts: {score} of {counter}")


if __name__ == '__main__':

    #start timer
    start = perf_counter()


    #asynchronous
    #jumia
    jumia_computing = Process(target=jumia, args=["computing", "https://www.jumia.com.ng/computing/"])
    jumia_electronics = Process(target=jumia, args=["electronics", "https://www.jumia.com.ng/electronics/"])
    jumia_fashion = Process(target=jumia, args=["fashion", "https://www.jumia.com.ng/category-fashion-by-jumia/"])
    jumia_health_beauty = Process(target=jumia, args=["health and beauty", "https://www.jumia.com.ng/health-beauty/"])
    jumia_home_office = Process(target=jumia, args=["home and office", "https://www.jumia.com.ng/home-office/"])
    jumia_phones_tablets = Process(target=jumia, args=["phones and tablets", "https://www.jumia.com.ng/phones-tablets/"])


    #konga
    konga_computing = Process(target=konga, args=["computing", "https://www.konga.com/category/computers-accessories-5227"])
    konga_electronics = Process(target=konga, args=["electronics", "https://www.konga.com/category/electronics-5261"])
    konga_fashion = Process(target=konga, args=["fashion", "https://www.konga.com/category/konga-fashion-1259"])
    konga_health_beauty = Process(target=konga, args=["health and beauty", "https://www.konga.com/category/beauty-health-personal-care-4"])
    konga_home_office = Process(target=konga, args=["home and office", "https://www.konga.com/category/home-kitchen-602"])
    konga_phones_tablets = Process(target=konga, args=["phones and tablets", "https://www.konga.com/category/phones-tablets-5294"])


    #start processes
    jumia_computing.start()
    konga_computing.start()
    konga_electronics.start()
    jumia_electronics.start()
    jumia_fashion.start()
    konga_fashion.start()
    konga_health_beauty.start()
    jumia_health_beauty.start()
    konga_home_office.start()
    konga_phones_tablets.start()
    jumia_home_office.start()
    jumia_phones_tablets.start()

    #write to file
    each = ["name", "sku", "price", "stars", "link", "image_url", "reviews", "seller", "category", "description"]
    with open("products.csv", 'w', encoding="utf-8") as product_file:
        product_filewrite = writer(product_file)
        product_filewrite.writerow(each)

    #join processes
    jumia_computing.join()
    konga_computing.join()
    konga_electronics.join()
    jumia_electronics.join()
    jumia_fashion.join()
    konga_fashion.join()
    konga_health_beauty.join()
    jumia_health_beauty.join()
    konga_home_office.join()
    konga_phones_tablets.join()
    jumia_home_office.join()
    jumia_phones_tablets.join()


    #end timer
    end = perf_counter()

    print(f"time: {round((end - start) / 60, 2)}mins")