import requests
import json
from bs4 import BeautifulSoup

# returns the value of the first index in list, if not empty
def check_if_empty_return(string_list):
    if len(string_list) != 0:
        return string_list[0].text.lstrip()
    else:
        return ""

def check_if_empty_return_string(string_list):
    if len(string_list) != 0:
        return string_list.text.lstrip()
    else:
        return ""
            
def get_item(item_id):
    # list for return
    list_with_data = []
    
    if item_id.strip() == "":
        return json.dumps(list_with_data)
    
    url = "https://www.ebay-kleinanzeigen.de/s-anzeige/" + item_id
	
	#TODO anzeige ohne bild finden
    default_image_url = "https://www.stoefelz.com/frontend/media/profile.jpg"
    
	
	#without headers ebay-kleinanzeigen blocks request TODO uncomment
    #headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0' }
    #html_site = requests.get(url, headers=headers)
    #soup = BeautifulSoup(html_site.text, "lxml")

	
	#TODO only for testing
    with open("item.html") as fp:
       soup = BeautifulSoup(fp, "lxml",)
	

	#TODO unten alles find_all because obere funktoin liste will
	# in every article tag is one complete search entry
    one_article = soup.find('article')
            
    # get id from attribute
    #big_pictures: find_all div(class::galleryimage-large--cover) -> in jedem eine img mit src array in div galleryimage-element
    big_pictures = one_article.find_all("img", id="viewad-image")
    big_pictures_array = []
    for one_picture in big_pictures:
        big_pictures_array.append(one_picture['src'])
    list_with_data.append(big_pictures_array)
    
    #small_pictures: find_all div (class::imagebox-thumbnail) -> in jedem img mit src
    small_pictures = one_article.find_all("div", class_="imagebox-thumbnail")
    small_pictures_array = []
    for one_picture in small_pictures:
        small_pictures_array.append(one_picture.find("img")['src'])
    list_with_data.append(small_pictures_array)
    
    #header: h1 with id: viewad-title -> content from h1
    heading = one_article.find("h1", id="viewad-title")
    #in h1 are unnecessary spans
    while heading.span != None:
        heading.span.replace_with("")
    list_with_data.append(check_if_empty_return_string(heading))
    
    #price: h2 with class: boxedarticle--price: in h2 
    price = one_article.find("h2", class_="boxedarticle--price")
    list_with_data.append(check_if_empty_return_string(price))
        
    #zip: span with id viewad-locality -> content of span
    zip_code = one_article.find("span", id="viewad-locality")
    list_with_data.append(check_if_empty_return_string(zip_code))
      
    #date
    date = one_article.find("div", id="viewad-extra-info").find("span")
    list_with_data.append(check_if_empty_return_string(date))
    
    #-> if li found, else ""
    #detaillist: find_all li class: addetailslist--detail -> inhalt: von li und darin auch ein span mit inhalt 
    detaillist = one_article.find_all("li", class_="addetailslist--detail")
    detaillist_array = []
    for one_detail in detaillist:
        detaillist_key_pair = []
        detaillist_key_pair.append(check_if_empty_return_string(one_detail.find("span")))
        one_detail.span.replace_with("")
        detaillist_key_pair.append(check_if_empty_return_string(one_detail))
        detaillist_array.append(detaillist_key_pair)
    list_with_data.append(detaillist_array)
    
    
    #checktag: li with class: checktag -> content of li
    checktag = one_article.find_all("li", class_="checktag")
    checktag_array = []
    for one_checktag in checktag:
        checktag_array.append(check_if_empty_return_string(one_checktag))
    list_with_data.append(checktag_array)
    
    #text: p with id: viewad-description-text -> content of p
    text = one_article.find("p", id="viewad-description-text")
    list_with_data.append(check_if_empty_return_string(text))
    
    #link
    link_to_item = url
    list_with_data.append(link_to_item)
    
 
    #return list in json format
    return json.dumps(list_with_data)

print(get_item("s"))
