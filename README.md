# Kleinanzeigen Simple Parser
Simple Parser for kleinanzeigen.de 

Website data get extracted with BeautifulSoup to an JSON array. Kleinanzeigen may block temporarly your ip because of too many requests in short time  

needed Python3 libraries: requests, json, bs4  
**Thanks to <a href="https://github.com/wention/BeautifulSoup4">BeautifulSoup</a> for making this project possible **

there are two functions: 
- 	get_item: data for one specific item
-	get_search_entries: search results from one page

## Function: *get_item(item_id)*

item_id: id from ebay-kleinanzeigen object is needed  
returns JSON Objects with following structure:  

{  
&emsp;'heading': string,  
&emsp;'price': string,  
&emsp;'zip-code': string,  
&emsp;'date': string,  
&emsp;'views': string,  
&emsp;'user-info': string,  
&emsp;'link': string,  
&emsp;'text': text,  
&emsp;'details': {  
&emsp;&emsp;key: string,  
&emsp;&emsp;value: string  
&emsp;}[],  
&emsp;'checktags': string[],  
&emsp;'small-pictures': string[],  
&emsp;'large-pictures': string[]  
} 

*heading:* heading of item  
*price:* price of item  
*zip-code:* zip code with city  
*date:* creation date  
*views:* view counter may be empty  
*user-info:* zip code as string  
*link:* link to item  
*text:* info text to item  
*details:* detail objects in array, detail object consists of key and value  
*checktags:* check tags in array  
*small-pictures:* preview picture urls (low resolution) in array  
*large-pictures:* main picture urls (high resolution) in array  

some elements could be empty  
if error: returns empty json object  

**Example**
> get_item(200045700)

returns
```
{  
    "heading": "BMW Gran Turismo", 
    "price": "18.800 \u20ac", 
    "zip-code": "75053 Baden-W\u00fcrttemberg - Gondelsheim", 
    "date": "01.01.2023", 
    "views": "", 
    "user-info": "Gewerblicher Nutzer\nAktiv seit 01.01.2023", 
    "link": "https://www.url.de/IDNUMBER", 
    "text": "Gebrauchter BMW Gran Turismo", 
    "details": [
        {"key": "Marke", "value": "BMW"}, 
        {"key": "Modell", "value": "3er"}, 
        {"key": "Kilometerstand", "value": "153.000 km"}, 
    ], 
    "checktags": ["Anh\u00e4ngerkupplung", "Einparkhilfe", "Leichtmetallfelgen", "Xenon-/LED-Scheinwerfer"], 
    "small_pictures": ["https://img.url.de/1_.JPG", "https://img.url.de/2_.JPG"],
    "large_pictures": ["img.url.de/1.JPG", "img.url.de/1.JPG"]
}
```

## Function: _get_search_entries(search_term, **search_arguments)_

search_term: your keywords (mandatory)  
**search_arguments: optional named parameter (order does not matter), they are not checked for plausibility; when parameters are not given, default values are used  

&emsp;city = string  
&emsp;zip_code = string  
>for filtering search results by city there is the city name AND the internal code for the zip code needed -> code for zip code begins with '_' but this function wants only the following numbers (you can find the codes and cities here: https://www.ebay-kleinanzeigen.de/s-ort-empfehlungen.json?query=berlin); default value is whole germany    

&emsp;zip_radius = string  
>possible values: 'r5', 'r10', 'r20', 'r30', 'r50', 'r100', 'r150', 'r200'; default value is no radius

&emsp;site_number = string  
>site number of results, if max limit is reached, the last page is returned again (TODO); default value is first page

&emsp;sorting = string  
>possible values: 'preis', 'entfernung'; default value is newest item

&emsp;seller = string  
>possible values: 'privat', 'gewerblich'; default is both

&emsp;typ = string  
>possible values: 'angebote', 'gewerblich'; default is both

&emsp;min_price = string  
&emsp;max_price = string  
>price values should be positive numbers


returns Array of JSON Objects with following structure:  

{  
&emsp;'id': string,  
&emsp;'heading': string,  
&emsp;'description': string,  
&emsp;'price': string,  
&emsp;'date': string,  
&emsp;'image-url': string,  
}  

*id:* id of item  
*heading:* heading of item  
*description:* description of item
*price:* price of item  
*date:* creation date  
*image-url:* url for preview image  

some elements could be empty  
if error: returns empty json object  

**Example**
> get_search_entries("smartphone", city = "Berlin", zip_code = "3331", site_number = "2", sorting = "preis", typ = "angebote", min_price = "100")

returns
```
[
  {
    "id": "1234", 
    "heading": "Tausche Sony Xperia 1", 
    "description": "Tausche ein gebrauchtes Sony Xperia 1 gegen ein anderes Smartphone", 
    "price": "500 \u20ac VB", 
    "date": "Heute, 06:24", 
    "image_url": "https://img.url.de/1_.JPG"
  }, 
  {
    "id": "4123", 
    "heading": "Apple iPhone 13 Smartphone 128gb mit Rechnung",
    "description": "Hiermit verkaufe ich meine neues Apple iPhone 13 Smartphone neu und unbenuzt mit Rechnung als...",
    "price": "800 \u20ac", 
    "date": "Gestern, 23:38", 
    "image_url": "https://img.url.de/2_.JPG"
  }, 
  {
    "id": "3214", 
    "heading": "Verkaufe ein Apple iPhone 13 Smartphone",
    "description": "Verkaufe ein Apple iPhone 13 Smartphone (15,4 cm/6,1 Zoll, 128 GB Speicherplatz, 12 MP...", 
    "price": "650 \u20ac", 
    "date": "Gestern, 22:41", 
    "image_url": "https://img.url.de/3_.JPG"
  }
]
```


