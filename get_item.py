import requests
import json
from bs4 import BeautifulSoup

# returns the string, if not None
# lstrip -> removes spaces and \n on left side of string
# \u200b fucks up the interpretation of the strings

def string_return_value(string):
    if string is not None:
        return string.text.lstrip().replace('\u200b', '')
    else:
        return ""
        
# return JSON array: [[username, userinfo], [big_pics, .. , big_pics], [small_pics, .., small_pics], heading, price, zip, date, views, [[detaillistright, detaillistleft], .., [detaillistright, detaillistleft]], [checktags, .. , checktags], text, link]          
# if there is some error -> empty string or array is in array
# if there is no such item -> empty JSON array

# item_id is Anzeigen-ID of Ebay-Kleinanzeigen item

def get_item(item_id):
    # list for return
    list_with_data = []
    
    # check for empty item_id -> item_id must be a string
    if str(item_id).strip() == "":
        return json.dumps("")
    
    url = "https://www.ebay-kleinanzeigen.de/s-anzeige/" + str(item_id)
	
	# TODO anzeige ohne bild finden

    # without headers ebay-kleinanzeigen blocks request TODO uncomment
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0' }
    html_site = requests.get(url, headers=headers)
    # html.parser or lxml -> lxml needs pip3 module
    soup = BeautifulSoup(html_site.text, "html.parser")
    
	
	#TODO only for offline testing -> code above must be commented
    #with open("item.html") as fp:
    #   soup = BeautifulSoup(fp, "html.parser",)
	
	
	# in every article tag is one complete search entry
    one_article = soup.find('article')
            
    # check if page exists
    if one_article is None:
        return json.dumps("")        
            
    # userinfo
    userinfo = soup.find("span", class_="iconlist-text")
    userinfo_list = []
    userinfo_list.append(string_return_value(userinfo.find("a")))
    # evtl TODO: \n mit viel leerzeichen ist drinnen, aber evtl brauch ich es auch zum anzeigen und das <br> raus
    userinfo_list.append(string_return_value(userinfo.find("span", class_="text-body-regular")))
    list_with_data.append(userinfo_list)
    
       
    # big_pictures: find_all div(class::galleryimage-large--cover) -> in every tag img with src list in div galleryimage-element
    big_pictures = one_article.find_all("img", id="viewad-image")
    big_pictures_list = []
    for one_picture in big_pictures:
        big_pictures_list.append(one_picture['src'])
    list_with_data.append(big_pictures_list)
    
    # small_pictures: find_all div (class::imagebox-thumbnail) -> in every img tag with src
    small_pictures = one_article.find_all("div", class_="imagebox-thumbnail")
    small_pictures_list = []
    for one_picture in small_pictures:
        small_pictures_list.append(one_picture.find("img")['src'])
    list_with_data.append(small_pictures_list)
    
    # header: h1 with id: viewad-title -> content from h1
    heading = one_article.find("h1", id="viewad-title")
    # in h1 are unnecessary spans
    while heading.span is not None:
        heading.span.replace_with("")
    list_with_data.append(string_return_value(heading))
    
     #price: h2 with class: boxedarticle--price: in h2 
    price = one_article.find("h2", class_="boxedarticle--price")
    list_with_data.append(string_return_value(price))
        
    # zip: span with id viewad-locality -> content of span
    zip_code = one_article.find("span", id="viewad-locality")
    list_with_data.append(string_return_value(zip_code))
    
    # date
    date = one_article.find("div", id="viewad-extra-info").find("span")
    list_with_data.append(string_return_value(date))
    
    # views 
    views = one_article.find("span", id="viewad-cntr-num")
    list_with_data.append(string_return_value(views))
    
    # -> if li found, else ""
    # detaillist: find_all li class: addetailslist--detail -> content from li and there is a span with content 
    detaillist = one_article.find_all("li", class_="addetailslist--detail")
    detaillist_list = []
    for one_detail in detaillist:
        detaillist_key_pair = []
        detaillist_key_pair.append(string_return_value(one_detail.find("span")))
        one_detail.span.replace_with("")
        detaillist_key_pair.append(string_return_value(one_detail))
        detaillist_list.append(detaillist_key_pair)
    list_with_data.append(detaillist_list)
    
    
    # checktag: li with class: checktag -> content of li
    checktag = one_article.find_all("li", class_="checktag")
    checktag_list = []
    for one_checktag in checktag:
        checktag_list.append(string_return_value(one_checktag))
    list_with_data.append(checktag_list)
    
    # text: p with id: viewad-description-text -> content of p
    text = one_article.find("p", id="viewad-description-text")
    # TODO newlines are missing -> .text from bs removes them
    list_with_data.append(string_return_value(text))

    # link
    link_to_item = url
    list_with_data.append(link_to_item)
    
 
    # return list in json format
    return json.dumps(list_with_data)

#testing line, set an actual id
print(get_item("2224438399"))
