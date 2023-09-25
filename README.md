# Kleinanzeigen Parser
Simple Parser for kleinanzeigen.de 

Website data get extracted with BeautifulSoup to an JSON array. Kleinanzeigen may block temporarly your ip because of too many requests in short time  

needed Python3 libraries: requests, json, bs4  
**Thanks to <a href="https://github.com/wention/BeautifulSoup4">BeautifulSoup</a> for making this project possible **

there are three functions: 
- 	get_item: data for one specific item
-	get_search_entries: search results from one page
-   get_all_categories: get all search categories with their ids

## Function: *get_item(item_id)*

item_id: id from ebay-kleinanzeigen object is needed  
returns JSON Objects with following structure:  
```
{  
	'heading': string, 
	'price': string, 
	'zip-code': string, 
	'date': string, 
	'views': string, 
	'username': string,
	'userinfo': string,
	'link': string,
	'text': text, 
	'details': { 
		key: string, 
		value: string,
	}[], 
	'checktags': string[], 
	'small-pictures': string[],
	'large-pictures': string[,
} 
```
*heading:* heading of item  
*price:* price of item  
*zip-code:* zip code with city  
*date:* creation date  
*views:* view counter may be empty  
*username*: username from seller  
*userinfo:* user type and creation date from user  
*link:* link to item  
*text:* info text from item  
*details:* detail objects in array, detail object consists of key and value  
*checktags:* check tags in array  
*small-pictures:* preview picture urls (low resolution) in array  
*large-pictures:* main picture urls (high resolution) in array  

some elements could be empty  
if error occurs while fetching data: returns empty json object  

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
    "username": "Thomas",
    "userinfo": "Gewerblicher Nutzer\nAktiv seit 01.01.2023", 
    "link": "https://www.url.de/IDNUMBER", 
    "text": "Gebrauchter BMW Gran Turismo", 
    "details": [
        {"key": "Marke", "value": "BMW"}, 
        {"key": "Modell", "value": "3er"}, 
        {"key": "Kilometerstand", "value": "153.000 km"}, 
    ], 
    "checktags": ["Anh\u00e4ngerkupplung", "Einparkhilfe", "Leichtmetallfelgen", "Xenon-/LED-Scheinwerfer"], 
    "small-pictures": ["https://img.url.de/1_.JPG", "https://img.url.de/2_.JPG"],
    "large-pictures": ["img.url.de/1.JPG", "img.url.de/1.JPG"]
}
```

## Function: _get_search_entries(search_term, search_arguments)_

search_term: your keywords (mandatory)  
search_arguments: Dictionary with optional, named parameter (order does not matter), they are not checked for plausibility; when parameters are not given, default values are used. When you want a default search, add an empty dictionary ('{}') as search_arguments

### Possible search_argument parameter 

zip_code_id  
>every zip code has its own id (you can find the codes here: https://www.kleinanzeigen.de/s-ort-empfehlungen.json?query=berlin) -> this website returns the ids with a previous '\_'. This argument needs only the number without the '\_'; default value is whole germany    

zip_radius  
>possible values: '5', '10', '20', '30', '50', '100', '150', '200'; default value is no radius

site_number  
>site number of results, if max limit is reached, the last page is returned again (TODO); default value is first page

sorting  
>possible values: 'SORTING_DATE', 'PRICE_AMOUNT'; default value is sorting with date

seller  
>possible values: 'PRIVATE', 'COMMERCIAL'; default is both

typ  
>possible values: 'OFFER', 'WANTED'; default is both

min_price  
max_price  
>price values should be positive numbers

category  
>every category has a specific number


returns Array of JSON Objects with following structure:  

```
{  
	'id': string,  
	'heading': string,  
	'description': string,  
	'price': string,  
	'zip-code': string,  
	'date': string,  
	'image-url': string,  
}  
```

*id:* id of item  
*heading:* heading of item  
*description:* description of item
*price:* price of item  
*zip-code*: zip code from location of item  
*date:* creation date  
*image-url:* url for preview image  

some elements could be empty when error occurs while fetching object  
if error: returns empty json object  

**Example**
> get_search_entries("smartphone", {"zip_code_id" :"3331", "site_number": "2", "sorting": "PRICE_AMOUNT", "typ": "OFFER", "min_price": "100"})

returns
```
[
  {
    "id": "1234", 
    "heading": "Tausche Sony Xperia 1", 
    "description": "Tausche ein gebrauchtes Sony Xperia 1 gegen ein anderes Smartphone", 
    "price": "500 \u20ac VB", 
    "zip-code": "13351 Wedding",
    "date": "Heute, 06:24", 
    "image-url": "https://img.url.de/1_.JPG"
  }, 
  {
    "id": "4123", 
    "heading": "Apple iPhone 13 Smartphone 128gb mit Rechnung",
    "description": "Hiermit verkaufe ich meine neues Apple iPhone 13 Smartphone neu und unbenuzt mit Rechnung als...",
    "price": "800 \u20ac", 
    "zip-code": "13351 Wedding",
    "date": "Gestern, 23:38", 
    "image-url": "https://img.url.de/2_.JPG"
  }, 
  {
    "id": "3214", 
    "heading": "Verkaufe ein Apple iPhone 13 Smartphone",
    "description": "Verkaufe ein Apple iPhone 13 Smartphone (15,4 cm/6,1 Zoll, 128 GB Speicherplatz, 12 MP...", 
    "price": "650 \u20ac", 
    "zip-code": "13351 Wedding",
    "date": "Gestern, 22:41", 
    "image-url": "https://img.url.de/3_.JPG"
  }
]
```

## Function: *get_all_categories()*


returns JSON Objects with following structure:  

```
{  
  'category_id': {
	'name': string,
	'number': string,
	'subs': {
	  'sub_name': string,
	  'sub_number': string
	}[]
  }
} 
```

_category_id_: category id as dictionary index  
_name_: name of category  
_number_: id of category  
_subs_: all subcategories as list  
_sub_name_: name of subcategory  
_sub_number_: id of subcategory  

this dictionary entry is repeated until all categories are captured

**Example**

```
{
  "210": {
	"name": "Auto, Rad & Boot", 
	"number": "210", 
	"subs": [
	  {"sub_name": "Autos", "sub_number": "216"}, 
		{"sub_name": "Autoteile & Reifen", "sub_number": "223"}, 
	  {"sub_name": "Boote & Bootszubehör", "sub_number": "211"}, 
	  {"sub_name": "Fahrräder & Zubehör", "sub_number": "217"}, 
	  {"sub_name": "Motorräder & Motorroller", "sub_number": "305"}, 
	  {"sub_name": "Motorradteile & Zubehör", "sub_number": "306"}, 
	  {"sub_name": "Nutzfahrzeuge & Anhänger", "sub_number": "276"}, 
	  {"sub_name": "Reparaturen & Dienstleistungen", "sub_number": "280"}, 
	  {"sub_name": "Wohnwagen & -mobile", "sub_number": "220"}, 
	  {"sub_name": "Weiteres Auto, Rad & Boot", "sub_number": "241"}
	]
  }
}
```