import requests
import json
from bs4 import BeautifulSoup

# html.parser or lxml -> lxml needs pip3 lxml module
html_parser = 'html.parser'
# default image when no image is available
default_image_url = 'https://www.stoefelz.com/no_image.svg'

# returns the string, if not None
# lstrip -> removes spaces and \n on left side of string
# \u200b fucks up the interpretation of the strings
def string_return_value(string):
    if string is not None:
        return string.text.lstrip().replace('\u200b', '')
    else:
        return ''

# returns array of search items
def get_search_entries(search_term, **search_arguments):
    try:
        city = search_arguments.get('city')
        zip_code = search_arguments.get('zip_code')
        zip_radius = search_arguments.get('zip_radius')
        site_number = search_arguments.get('site_number')
        sorting = search_arguments.get('sorting')
        seller = search_arguments.get('seller')
        typ = search_arguments.get('typ')
        min_price = search_arguments.get('min_price')
        max_price = search_arguments.get('max_price')
  
        # example url: 
        # https://www.kleinanzeigen.de/s-/handy-telekom/sonstige/hessen/direktkaufen:aktiv/paketdienst:dhl/preis:10:800/oneplus/k0c173l4279r200+handy_telekom.art_s:sonstige+handy_telekom.condition_s:condition_new+handy_telekom.device_equipment_s:only_device
        
        # url compositor
        url = 'https://www.kleinanzeigen.de/s-'
        # TODO categories
        category = 'k0'

        if zip_code and city:
            url += '/'+ city
        if sorting:
            url += '/sortierung:' + sorting
        if seller:
            url += '/anbieter:' + seller
        if typ:
            url += '/anzeige:' + typ 
        if min_price and max_price:
            url += '/preis:' + min_price + ':' + max_price 
        elif min_price:
            url += '/preis:' + min_price + ':' 
        elif max_price:
             url += '/preis:' + ':' + max_price 
        if site_number:
            url += '/seite:' + site_number
        url += '/' + search_term
        if category:
            url += '/' + category
        if zip_code and city:
            url += 'l' + zip_code
            if zip_radius:
                url += zip_radius

        # without headers kleinanzeigen blocks request
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        html_site = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_site.text, html_parser)

        # only for testing, code above must be commented
        # with open('../Downloads/fleisch.html') as fp:
          # soup = BeautifulSoup(fp, html_parser)

        # list for return
        list_with_items = []
        # in every article tag is one item
        articles = soup.find_all('article')

        for one_article in articles:
            # get id from attribute
            if one_article['data-adid'] is not None:
                item_id = one_article['data-adid']
            else:
                continue
    
            # heading
            heading = one_article.find('a', class_='ellipsis')
            heading = string_return_value(heading)
            
            # info
            info_text = one_article.find('p', class_='aditem-main--middle--description')
            info_text = string_return_value(info_text)
            
            # price
            price = one_article.find('p', class_='aditem-main--middle--price-shipping--price')
            price = string_return_value(price)

            # zip code
            zip_code = one_article.find('div', class_='aditem-main--top--left')
            zip_code = string_return_value(zip_code)

            # date
            date = one_article.find('div', class_='aditem-main--top--right')
            date = string_return_value(date)
            
            # picture (can be empty)
            picture_div = one_article.find('div', class_='imagebox')
            try:
                image_url = picture_div['data-imgsrc']
            except:
                image_url = default_image_url
            
            item =  {
                'id': item_id,
                'heading': heading,
                'description': info_text,
                'price': price,
                'date': date,
                'image-url': image_url
            }
            
            # append item to the returned list
            list_with_items.append(item)
            
        #for debugging
        print(url)
        # return list in json format
        return json.dumps(list_with_items)

    except:
        return json.dumps([])

