import requests
import json
from bs4 import BeautifulSoup

global error

# returns the value of the first index in list, if not empty; should only have 1 index, but it doesnt matter

def check_if_empty_return(string_list):
    if len(string_list) != 0:
        #\u200b fucks up the interpretation of the strings
        if len(string_list) > 1000:
            error = True
        return string_list[0].text.lstrip().replace('\u200b', '')
    else:
        return ""

    # TODO für filter sollte sorting einfach in einen string umgewandelt werden, wo alle filter rein kommen, bsp: "/s/k0/reinland/kleidung"
    # obwohl dann z.b. bei sorting zu beachten ist, dass "sortierung: blablabal" des is
def get_search_entries(search_term, site = 1, sorting = "", seller = "", typ="", min_price = 0, max_price = -1):
    try:
        # filter
        category = "/k0"
        if sorting != "preis":
            sorting = ""
        if seller != "privat" and seller != "gewerblich":
            seller = ""
        if typ != "angebote" and typ != "gesuche":
            typ = ""
        try:
            if int(min_price) <= 0 or int(min_price) > 100000:
                min_price = 0
        except:
            min_price = 0
        try:
            if int(max_price) < 0 or int(max_price) > 100000:
                max_price = ""
        except:
            max_price = ""

      # example for link: https://www.ebay-kleinanzeigen.de/s-sortierung:preis/anbieter:privat/anzeige:angebote/preis:1:10/k0
        url = "https://www.ebay-kleinanzeigen.de/s/sortierung:" + sorting + "/anbieter:" + seller + "/anzeige:" + typ + "/preis:" + str(min_price) + ":" + str(max_price) + "/seite:" + str(site) + "/" + search_term + category
        print(url)

            # TODO
        default_image_url = "https://www.stoefelz.com/frontend/media/profile.jpg"

            # without headers ebay-kleinanzeigen blocks request
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0' }
        html_site = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_site.text, "html.parser")

            # only for testing, code above must be commented
        # with open("suche2.html") as fp:
         #  soup = BeautifulSoup(fp, "lxml",)

        # list for return
        list_with_data = []

            # in every article tag is one complete search item
        articles = soup.find_all('article')

        for one_article in articles:
            error = False
            # for one search result
            article_list = []

            # get id from attribute
            if one_article['data-adid'] is not None:
                article_list.append(one_article['data-adid'])
            else:
                print("no id found")
                article_list.append("")

            # get values from parsing correct class
            heading = one_article.find_all("a", class_="ellipsis")
            article_list.append(check_if_empty_return(heading))


            text = one_article.find_all("p", class_="aditem-main--middle--description")
            article_list.append(check_if_empty_return(text))

            price = one_article.find_all("p", class_="aditem-main--middle--price-shipping--price")
            article_list.append(check_if_empty_return(price))

            zip_code = one_article.find_all("div", class_="aditem-main--top--left")
            article_list.append(check_if_empty_return(zip_code))

            create_date = one_article.find_all("div", class_="aditem-main--top--right")
            article_list.append(check_if_empty_return(create_date))

            # get picture url from class, but must check if there is a picture or not
            picture = one_article.find_all("div", class_="imagebox")
            if len(picture) != 0:

                classes = picture[0]['class']
                # classes returns string list of the class names
                # searching for "is-nopic" then there is no image
                checker = True

                for one_class_name in classes:
                    if one_class_name == "is-nopic":
                        article_list.append(default_image_url)
                        checker = False
                        break

                if checker == True:
                    article_list.append(picture[0]['data-imgsrc'])

            else:
                article_list.append(default_image_url)

            if error == True:
                print("too long string")
                continue
            else:
            # append it to the list for return
                list_with_data.append(article_list)

        # return list in json format
        print(list_with_data)
        return json.dumps(list_with_data)

    except:
        return json.dumps([])

    
#search term for testing
get_search_entries("smartphone", "preis", 2, "privat", "gesuche", "", "")

