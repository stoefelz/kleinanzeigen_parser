import requests
import json
from bs4 import BeautifulSoup

# returns the value of the first index in list, if not empty
def check_if_empty_return(string_list):
    if len(string_list) != 0:
        return string_list[0].text.lstrip()
    else:
        return ""
        
            
def get_search_entries(search_term, sorting = "neu", site = 1):
    # list for return
    list_with_data = []
    
    category = "/k0"
    
    url = "https://www.ebay-kleinanzeigen.de/s/sortierung:" + sorting + "/seite:" + str(site) + "/" + search_term + category
	
	#TODO
    default_image_url = "https://www.stoefelz.com/frontend/media/profile.jpg"
	
	#without headers ebay-kleinanzeigen blocks request TODO uncomment
    #headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0' }
    #html_site = requests.get(url, headers=headers)
    #soup = BeautifulSoup(html_site.text, "lxml")

	
	#TODO only for testing
    with open("suche.html") as fp:
       soup = BeautifulSoup(fp, "lxml",)
	

	
	# in every article tag is one complete search entry
    articles = soup.find_all('article')
    
    for one_article in articles:
        # for one search result
        article_list = []
        
        # get id from attribute
        element_id = one_article['data-adid']
        article_list.append(element_id)
        
        #get values from parsing correct class
        heading = one_article.find_all("a", class_="ellipsis")
        article_list.append(check_if_empty_return(heading))
        
        text = one_article.find_all("p", class_="aditem-main--middle--description")
        article_list.append(check_if_empty_return(text))
        
        price = one_article.find_all("p", class_="aditem-main--middle--price")
        article_list.append(check_if_empty_return(price))
        
        zip_code = one_article.find_all("div", class_="aditem-main--top--left")
        article_list.append(check_if_empty_return(zip_code))
        
        create_date = one_article.find_all("div", class_="aditem-main--top--right")
        article_list.append(check_if_empty_return(create_date))
          
        #get picture url from class, but must check if there is a picture or not
        picture = one_article.find_all("div", class_="imagebox")
        if len(picture) != 0:
  
            classes = picture[0]['class']
            #classes returns string list of the class names
            #searching for "is-nopic" then there is no image
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
        
        #append it to the list for return
        list_with_data.append(article_list)
        
    #return list in json format
    return json.dumps(list_with_data)

print(get_search_entries("oneplus"))
