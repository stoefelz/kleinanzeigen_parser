
import requests
import json
import re
from bs4 import BeautifulSoup

# html.parser or lxml -> lxml needs pip3 lxml module
HTML_PARSER = 'lxml'
# default image when no image is available
DEFAULT_IMAGE_URL = 'https://www.stoefelz.com/no_image.svg'
BASE_URL = 'https://www.kleinanzeigen.de'
# without headers kleinanzeigen blocks request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0'
}


#for new Site by Chatgpt -------------------------------#

def unwrap(obj):

    # remove wrapper like [0, value] or [1, value].
    if isinstance(obj, dict):
        return {k: unwrap(v) for k, v in obj.items()}

    if (
        isinstance(obj, list)
        and len(obj) == 2
        and isinstance(obj[0], int)
    ):
        return unwrap(obj[1])

    if isinstance(obj, list):
        return [unwrap(v) for v in obj]

    return obj


def find_result_ads(soup):

    # get search result object
    for island in soup.find_all("astro-island"):

        props = island.get("props")
        if not props:
            continue

        try:
            data = unwrap(json.loads(props))
        except Exception:
            continue

        result_ads = data.get("resultAds")

        if isinstance(result_ads, list):
            return result_ads

    return []


def get_image(ad):

    # robust picture search
    images = ad.get("imageList") or []

    if images:
        for key in (
            "adTableThumbnailPrioUrl",
            "adTableThumbnailUrl",
            "xLargeUrl",
        ):
            url = images[0].get(key)
            if url:
                return url

    if ad.get("seoContent"):
        try:
            seo = json.loads(ad["seoContent"])
            return seo.get("contentUrl", DEFAULT_IMAGE_URL)
        except Exception:
            pass

    return DEFAULT_IMAGE_URL

def new_site(items, result_ads):

    for result in result_ads:
        ad = result.get("organicAdPreview")

        # ignore ads
        if not isinstance(ad, dict):
            continue

        if ad.get("distanceInKilometers"):
            zip_code = ad.get("locationName", "") + " " + ad.get("parentLocationName", "") + " (" + str(ad.get("distanceInKilometers")) + " km)"
        else:
            zip_code = ad.get("locationName", "") + " " + ad.get("parentLocationName", "")

        items.append({
            "id": ad.get("id"),
            "heading": ad.get("title", ""),
            "description": ad.get("description", ""),
            "price": ad.get("price", ""),
            "zip-code":  zip_code,
            "date": ad.get("sortingDate", ""),
            "image-url": get_image(ad),
        })

# -------------------------------------------------- #


# returns the string, if not None
# lstrip -> removes spaces and \n on left side of string
# \u200b fucks up the interpretation of the strings
def clean_text(text: str) -> str:
    if text is not None:
        return text.get_text(separator=' ', strip=True).replace('\u200b', '')
    else:
        return ''

def old_site(items, all_articles):
    for article in all_articles:
        # get id from attribute
        item_id = article.get('data-adid')
        if not item_id:
            continue
    
        image_url = DEFAULT_IMAGE_URL
        # new json info type
        infos_json = article.find('script', {'type': 'application/ld+json'})
        
        heading = ''
        #heading and image url
        if infos_json and infos_json.string:
            try:
                json_data = json.loads(infos_json.string)
                heading = json_data.get('title').replace('\u200b', '')
                image_url = json_data.get('contentUrl') or DEFAULT_IMAGE_URL
            except json.JSONDecodeError:
                pass
        if not heading:
            heading= (
                clean_text(article.find('a', class_='ellipsis'))
                or clean_text(article.find('span', class_='ellipsis'))
                )
       
        # info
        info_text = article.find('p', class_='aditem-main--middle--description')
        info_text = clean_text(info_text)
        
        # price
        price = article.find('p', class_='aditem-main--middle--price-shipping--price')
        if hasattr(price, 'contents') and len(price.contents) >= 1:
            price = clean_text(price.contents[0])
        else:
            price = clean_text(price)

        # zip code
        zip_code_with_space = article.find('div', class_='aditem-main--top--left')
        #removes line break in text
        zip_code = re.sub(r'\s{2,}', ' ', clean_text(zip_code_with_space).replace('\n', ' '))
        
        # date
        date = article.find('div', class_='aditem-main--top--right')
        date = clean_text(date)
        
        items.append({
            'id': item_id,
            'heading': heading,
            'description': info_text,
            'price': price,
            'zip-code': zip_code,
            'date': date,
            'image-url': image_url
        })

# returns array of search items
def get_search_entries(search_term: str, search_arguments: dict) -> str:

    def argument(key: str, default: str = '') -> str:
        return search_arguments.get(key) or default

    url = (
        f"{BASE_URL}/s-suchanfrage.html"
        f"?keywords={search_term}"
        f"&categoryId={argument('category')}"
        f"&locationId={argument('zip_code_id')}"
        f"&radius={argument('zip_radius')}"
        f"&sortingField={argument('sorting')}"
        f"&adType={argument('typ')}"
        f"&posterType={argument('seller')}"
        f"&pageNum={argument('site_number')}"
        f"&maxPrice={argument('max_price')}"
        f"&minPrice={argument('min_price')}"
        f"&buyNowEnabled={argument('buynow', 'false')}"
        f"&shipping={argument('shipping')}"
        f"&shippingCarrier="
    )

    response = requests.get(url, headers=HEADERS) 
    # utf-8 important for showing right characters
    response.encoding = "utf-8"
    html_text = response.text

    # only for testing, code above must be commented
    #with open("quellcode.html", encoding="utf-8") as fp:
    #    html_text = fp.read()

    soup = BeautifulSoup(html_text, HTML_PARSER)

    # list for return
    items = []

    #check for new or old website
    result_ads = find_result_ads(soup)
    if(result_ads):
        print("NEW Site\n")
        new_site(items, result_ads)
    else:
        print("OLD Site\n")
        all_articles = soup.find_all('article')
        old_site(items, all_articles)
        
    #for debugging
    #print(url)
    # return list in json format, ensure_ascii=False for Umlaute
    return json.dumps(items, ensure_ascii=False)

