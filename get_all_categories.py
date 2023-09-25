import requests
import json
import re
from bs4 import BeautifulSoup

basic_url = 'https://www.kleinanzeigen.de/'
#html.parser or lxml -> lxml needs pip3 lxml module
html_parser = 'html.parser'

def get_category_number(string):
    if string is not None:
        # get string beginning with /c and two or three chars (should be numbers)
        ce_number = re.search(r"(/c...?)", string).group()
        # return only the numbers without /c
        return ce_number[2:]
    else:
        return ''

def get_all_categories():
    try:
        url = basic_url + 's-kategorien.html'
        # without headers request is bocked
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        html_site = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_site.text, html_parser)
        
        category_return_item = {}
        
        #there are three <ul> for all categories
        category_columns = soup.find_all('ul', class_='a-span-8 l-col a-horizontal-padded l-container treelist')
        if category_columns is None:
            raise Exception('There are no categories to find')

        for column in category_columns:
            # it builds a category
            categories = column.find_all('li', class_='l-container-row')
            
            # find the main category 
            for category in categories:
                main_category_number = get_category_number(category.find('h2').find('a')['href'])
                main_category_name = category.find('h2').find('a').string
                
                main_category_item = {
                    'name': main_category_name,
                    'number': main_category_number,
                    'subs': [],
                }
                
                # and its sub categories
                subs = category.find_all('li')
                for sub in subs:
                    sub_category_number = get_category_number(sub.find('a')['href'])
                    sub_category_name = sub.find('a').string

                    sub_category_item = {
                        'sub_name': sub_category_name,
                        'sub_number': sub_category_number,
                    }
                    
                    # index for easier finding the category again later
                    main_category_item['subs'].append(sub_category_item)
                
                category_return_item[main_category_number] = main_category_item

        # return object in json format, ensure_ascii=False for Umlaute
        return json.dumps(category_return_item, ensure_ascii=False)
        
    except:
        return json.dumps({})

