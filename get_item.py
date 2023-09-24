import requests
import json
import re
from bs4 import BeautifulSoup

basic_url = 'https://www.kleinanzeigen.de/'
#html.parser or lxml -> lxml needs pip3 lxml module
html_parser = 'html.parser'

# returns the string, if not None
# lstrip -> removes spaces and \n on left side of string
# \u200b fucks up the interpretation of the strings
def string_return_value(string):
    if string is not None:
        return string.text.lstrip().replace('\u200b', '')
    else:
        return ''

# item_id is unique ID of Kleinanzeigen item
def get_item(item_id):
    try:
        url = basic_url + 's-anzeige/' + str(item_id)
        # without headers request is bocked
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        html_site = requests.get(url, headers=headers)
        # comment follwing line for offline testing
        soup = BeautifulSoup(html_site.text, html_parser)
        
        # only for offline testing, remove following comments
        # with open('test.html') as fp:
        #    soup = BeautifulSoup(fp, html_parser)
        
        # in every article tag is one complete search entry
        one_article = soup.find('article')
        
        # check if page exists
        if one_article is None:
            raise Exception('Item does not exist')
            
        #userinfo and username
        userinfo_with_space = soup.find('span', class_='iconlist-text').find('span', class_='text-body-regular')
        #removes line break in text
        userinfo = re.sub('  .*  ', '', string_return_value(userinfo_with_space))
        
        username = userinfo_with_space = soup.find('span', class_='iconlist-text').find('span', class_='text-body-regular-strong').a
        username = string_return_value(username)
        
        
        # large_pictures: find_all div(class::galleryimage-large--cover) -> in every tag img with src list in div galleryimage-element
        large_pictures_list = []
        large_pictures = one_article.find_all('img', id='viewad-image')
        for one_picture in large_pictures:
            large_pictures_list.append(one_picture['src'])
        
         # small_pictures: find_all div (class::imagebox-thumbnail) -> in every img tag with src
        small_pictures_list = []
        small_pictures = one_article.find_all('div', class_='imagebox-thumbnail')
        for one_picture in small_pictures:
            small_pictures_list.append(one_picture.find('img')['src'])
        
        # heading: h1 with id: viewad-title -> content from h1
        heading = one_article.find('h1', id='viewad-title')
        # in h1 are unnecessary spans
        while heading.span is not None:
            heading.span.replace_with('')
        heading = string_return_value(heading)
        
        # price: h2 with class: boxedarticle--price: in h2 
        price = one_article.find('h2', class_='boxedarticle--price')
        price = string_return_value(price)
            
        # zip: span with id viewad-locality -> content of span
        zip_code = one_article.find('span', id='viewad-locality')
        zip_code = string_return_value(zip_code)
        
        # date
        date = one_article.find('div', id='viewad-extra-info').find('span')
        date = string_return_value(date)
        
        # views 
        views = one_article.find('span', id='viewad-cntr-num')
        views = string_return_value(views)
        
        # detaillist: find_all li class: addetailslist--detail -> content from li and there is a span with content 
        detaillist_list = []
        detaillist = one_article.find_all('li', class_='addetailslist--detail')
        for one_detail in detaillist:
            value = string_return_value(one_detail.find('span'))
            one_detail.span.replace_with('')
            # delete trailing \n
            key = string_return_value(one_detail).rstrip()
            key_value_pair = {'key': key, 'value': value}
            detaillist_list.append(key_value_pair) 
           
        # checktag: li with class: checktag -> content of li
        checktag = one_article.find_all('li', class_='checktag')
        checktag_list = []
        for one_checktag in checktag:
            checktag_list.append(string_return_value(one_checktag))
        
        # text: p with id: viewad-description-text -> content of p
        text = one_article.find('p', id='viewad-description-text')
        # convert br to \n
        # text consists of not contiguous br tags
        text = re.sub('<.?br.?>', '\n', str(text))
        # text is now string and msut be converted to html again
        text = BeautifulSoup(text, html_parser)
        text = string_return_value(text)
     
        item_object = {
            'heading': heading,
            'price': price,
            'zip-code': zip_code,
            'date': date,
            'views': views,
            'username': username,
            'userinfo': userinfo,
            'link': url,
            'text': text,
            'details': detaillist_list,
            'checktags': checktag_list,
            'small-pictures': small_pictures_list,
            'large-pictures': large_pictures_list
        }
        
        # return object in json format
        return json.dumps(item_object)
        
    except:
        return json.dumps({})

