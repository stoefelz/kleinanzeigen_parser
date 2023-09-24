import requests
import json
import re
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
def get_search_entries(search_term, search_arguments):
    try:
        zip_code_id = search_arguments.get('zip_code_id') if search_arguments.get('zip_code_id') != None else ""
        zip_radius = search_arguments.get('zip_radius') if search_arguments.get('zip_radius') != None else ""
        site_number = search_arguments.get('site_number') if search_arguments.get('site_number') != None else ""
        sorting = search_arguments.get('sorting') if search_arguments.get('sorting') != None else ""
        seller = search_arguments.get('seller') if search_arguments.get('seller') != None else ""
        typ = search_arguments.get('typ') if search_arguments.get('typ') != None else ""
        min_price = search_arguments.get('min_price') if search_arguments.get('min_price') != None else ""
        max_price = search_arguments.get('max_price') if search_arguments.get('max_price') != None else ""
        category_id = search_arguments.get('category') if search_arguments.get('category') != None else ""
  
        # example url: 
        # https://www.kleinanzeigen.de/s-suchanfrage.html?keywords=auto&categoryId=210&locationStr=Frankfurt+am+Main+-+Hessen&locationId=4292&radius=10&sortingField=PRICE_AMOUNT&adType=WANTED&posterType=COMMERCIAL&pageNum=1&action=find&maxPrice=20&minPrice=10&buyNowEnabled=false&shippingCarrier=
      
        # url compositor
        url = 'https://www.kleinanzeigen.de/s-suchanfrage.html?keywords='+search_term+'&categoryId='+category_id+'&locationStr=&locationId='+zip_code_id+'&radius='+zip_radius+'&sortingField='+sorting+'&adType='+typ+'&posterType='+seller+'&pageNum='+site_number+'&action=find&maxPrice='+max_price+'&minPrice='+min_price+'&buyNowEnabled=false&shippingCarrier=' 

        # without headers kleinanzeigen blocks request
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0' }
        html_site = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_site.text, html_parser)

        # only for testing, code above must be commented
        # with open('../Downloads/test.html') as fp:
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
            zip_code_with_space = one_article.find('div', class_='aditem-main--top--left')
            #removes line break in text
            zip_code = re.sub('  .*  ', '', string_return_value(zip_code_with_space)).replace('\n', ' ')

            # date
            date = one_article.find('div', class_='aditem-main--top--right')
            date = string_return_value(date)
            
            # picture (can be empty)
            picture_div = one_article.find('div', class_='imagebox')
            try:
                image_url = one_article.find('img')['src']
            except:
                image_url = default_image_url
            
            item =  {
                'id': item_id,
                'heading': heading,
                'description': info_text,
                'price': price,
                'zip-code': zip_code,
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
print(get_search_entries("smartphone", {"zip_code_id" :"3331", "zip_radius": "5", "site_number": "2", "sorting": "PRICE_AMOUNT", "typ": "OFFER", "min_price": "100"}))
