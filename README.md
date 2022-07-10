# ek_simple_parser
Ebay Kleinanzeigen Simple Parser

# TODO
getCategories()  
getSearchEntries("search_term")  
getItem(ID)  


pip beautifulsoup 4 + requests ???

was ist in sfos zu tun: 

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

idee:
für bild weiter swipen irgendwie sichtbar machen
bei suche bei langem drücken link zu browser item
bei löschen klick in suchleiste: keyboard zeigen
ladebildschirm auf jeder seite
