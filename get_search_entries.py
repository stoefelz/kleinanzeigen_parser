import requests
import json
from bs4 import BeautifulSoup

# returns the value of the first index in list, if not empty; should only have 1 index, but it doesnt matter
def check_if_empty_return(string_list):
    if len(string_list) != 0:
        #\u200b fucks up the interpretation of the strings
        return string_list[0].text.lstrip().replace('\u200b', '')
    else:
        return ""
        
            #TODO wenn 10stellige nummer -> dann sollte anzeige anngezeigt werden
            #sollte wie ein onclick event auf liste sein
            
    #TODO für fliter sollte sorting einfach in einen string umgewandelt werden, wo alle filter rein kommen, bsp: "/s/k0/reinland/kleidung"
    #obwohl dann z.b. bei sorting zu beachten ist, dass "sortierung: blablabal" des is
def get_search_entries(search_term, sorting = "neu", site = 1):

    
    #TODO mehrere filter implementieren
    category = "/k0"
    
    url = "https://www.ebay-kleinanzeigen.de/s/sortierung:" + sorting + "/seite:" + str(site) + "/" + search_term + category
	
	#TODO
    default_image_url = "https://www.stoefelz.com/frontend/media/profile.jpg"
	
	#without headers ebay-kleinanzeigen blocks request TODO uncomment
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0' }
    html_site = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_site.text, "lxml")

	
	#TODO only for testing
    #with open("suche2.html") as fp:
     #  soup = BeautifulSoup(fp, "lxml",)
	
    # list for return
    list_with_data = []
	
	# in every article tag is one complete search entry
    articles = soup.find_all('article')
    
    for one_article in articles:
        # for one search result
        article_list = []
        
        # get id from attribute
        if one_article['data-adid'] is not None:
            article_list.append(one_article['data-adid'])
        else:
            article_list.append("")
        
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

print(get_search_entries("bernd das bureck"))
