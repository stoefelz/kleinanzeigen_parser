# ek_simple_parser
Ebay Kleinanzeigen Simple Parser  

Website data get extracted with BeautifulSoup to an JSON array. Ebay Kleinanzeigen may block temporarly your ip because of too many requests in short time  

needed Python3 libraries: requests, json, bs4  

there are two files: get_item (info for one specific item) and get_search_entries (search results 1 page from Ebay Kleinanzeigen)

__Function: *get_item(item_id)*__

item_id: id from ebay-kleinanzeigen object is needed  
returns array with strings or arrays in following order:  

[[username, userinfo], [big_pics, .. , big_pics], [small_pics, .., small_pics], heading, price, zip, date, views, [[detaillistright, detaillistleft], .., [detaillistright, detaillistleft]], [checktags, .. , checktags], text, link]  

*0* userinfo in string  
*1* urls of pictures with better resolution in an array  
*2* urls of pictures with less resolution in an array  
*3* heading in string  
*4* price in string  
*5* zip code as string  
*6* date of creation in string  
*7* number of views in string (it seems it doesnt work, is only empty string sometimes)  
*8* details in array, where key pair is stored [value_of_info: info]  
*9* check tags in array  
*10* product description in string  
*11* Link to Ebay Kleinanzeigen item website  

there could be only one empty string in in every array index -> error/not available in html source code  

if error: returns empty json array  

__Function: *get_search_entries(search_term, sorting = "neu", site = 1)*__

search_term: your keywords, sorting: *neu* or *preis* possible  
if *site* max limit is reached -> last max site is returned // TODO  
returns array with arrays of strings:  

[[item_id, heading, text, price, zip, date, image.jpg], ... ,[item_id, heading, text, price, zip, date, image.jpg]]  

every item array has following order:  

*0* item_id  
*1* heading  
*2* product description  
*3* price  
*4* zip code  
*5* date of creation  
*6* image of item  

there could be only one empty string in in every array index -> error/not available in html source code  

if error: returns empty json array

# TODO
getCategories()  

bugs: 

bei suche: zuerst checken, ob übergebener json string inhalt hat, wenn leer -> keine suchergebnisse
bei artikel seite: zuerst checken, ob übergebener json string inhalt hat, wenn leer -> keine objekt mit dieser id

TODO
mal schauen, was bei einer anzeige passiert, wo kein bild
wenn irgendein absatz nicht vorhanden -> ausblenden

BUGS: anscheinend in der plz zeile oder so in der suche html code zu sehen <!-- Libertywrapper .... -->

description nich ganz sichtbar
keine views sichtbar: anscheinend ohne javascript net möglich -> raushauen, scheinbar manchmal undefinied vies meldung
user info, da müssen leerzeilen raus
macnhe anzeigen kann man net öffnen
in objektanzeige: zeilenumbrüche fehlen einfach
nicht anzeigbar: evtl wenn  "Detalis" leer
details und features: wenn zeilenumbruch weil überlänge, schaut auch scheiße aus


idee:
für bild weiter swipen irgendwie sichtbar machen
bei suche bei langem drücken link zu browser item
bei löschen klick in suchleiste: keyboard zeigen
ladebildschirm auf jeder seite
