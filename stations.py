#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from init_objects import clean_stations

# missing some stations
# stations have to be in order: first stop -> last stop
bus_stations = {
    '27 (NS Rudnik)': ['Letališka', 'Rog', 'GZL', 'Leskovškova', 'Yulon', 'BTC - Emporium', 'BTC - Kolosej', 'Tržnica',
                       'BTC - Uprava', 'Jarše', 'Šola Jarše', 'Flajšmanova', 'Središka', 'Viadukt', 'Friškovec',
                       'Kolodvor', 'Bavarski dvor', 'Pošta', 'Drama', 'Križanke', 'Gornji trg', 'Privoz', 'Strelišče',
                       'Ižanska', 'Galjevica', 'Mihov štradon', 'Jurčkova', 'Bobrova', 'NS Rudnik'],
    '20 (Fužine)': ['Nove Stožice P+R', 'Maroltova', 'Puhova', 'Kardeljeva ploščad', 'Gasilska brigada', 'Bežigrad',
                    'Razstavišče', 'Bavarski dvor', 'Dalmatinova', 'Turist', 'Zmajski most', 'Poljanska',
                    'Ambrožev trg', 'Roška', 'Klinični center', 'Bolnica', 'Tržnica Moste', 'Zaloška', 'Brodarjev trg',
                    'Preglov trg', 'Rusjanov trg ', 'Fužine P+R'],
    '27 (Letališka)': ['NS Rudnik', 'Bobrova', 'Jurčkova', 'Mihov štadron', 'Galjevica', 'Ižanska', 'Stelišče',
                       'Privoz', 'Gornji trg', 'Križanke', 'Drama', 'Pošta', 'Bavarski dvor', 'Kolodvor', 'Friškovec',
                       'Viadukt', 'Središka', 'Flajšmanova', 'Šola Jarše', 'Jarše', 'BTC - Uprava', 'Tržnica',
                       'BTC - Kolosej', 'BTC - Emporium', 'Yulon', 'Leskovškova', 'GZL', 'Rog', 'Letališka'],
    '20 (Nove Stožice)': ['Fužine P+R', 'Rusjanov trg', 'Preglov trg', 'Brodarjev trg', 'Pot na Fužine', 'Zaloška',
                          'Tržnica Moste', 'Bolnica', 'Klinični center', 'Ambrožev trg', 'Poljanska', 'Zmajski most',
                          'Tavčarjeva', 'Bavarski dvor', 'Razstavišče', 'Bežigrad', 'Kržičeva', 'Gasilska Brigada',
                          'Puhova', 'Nove Stožice'],
    '6 (Črnuče)': ['Dolgi most P+R', 'Bonifacija', 'Vič', 'Glince', 'Stan in dom', 'Hajdrihova', 'Tobačna', 'Aškerčeva',
                   'Drama', 'Konzorcij', 'Ajdovščina', 'Bavarski dvor', 'Razstavišče', 'Astra', 'Stadion', 'Mercator',
                   'AMZS', 'Smelt', 'Stožice', 'Ruski car', 'Ježica', 'Sava', 'Kolodvor Črnuče', 'Rogovilc', 'Črnuče'],
    '6 (Dolgi most P+R)': ['Črnuče', 'Rogovilc', 'Kolodvro Črnuče', 'Sava', 'Ježica', 'Ruski car', 'Stožice', 'Smelt',
                           'AMZS', 'Mercator', 'Stadion', 'Astra', 'Razstavišče', 'Bavarski dvor', 'Pošta', 'Drama',
                           'Aškerčeva', 'Tobačna', 'Hajdrihova', 'Staon in dom', 'Glince', 'Vič', 'Bonifacija',
                           'Dolgi most P+R'],
    '7L (Pržan)': ['Letališka', 'Rog', 'GZL', 'Leskoškova', 'Yulon', 'Bratislavska', 'Nove Jarše', 'Žito', 'Kodrova',
                   'Jarše', 'Šola Jarše', 'Pokopališka', 'Žale', 'Savske Stolpnice', 'Prekmurska', 'Bežigrad',
                   'Razstavišče', 'Bavarski Dvor', 'Hotel Lev', 'Tivoli', 'Stara cerkev', 'Na jami', 'Bolnica P Držaja',
                   'Zgornja Šiška', 'Tržnica Koseze', 'Čebelarska', 'Plešičeva', 'Andreja Bitenca', 'Pržan'],
    '7L (Letališka)': ['Pržan', 'Andreja Bitenca', 'Plešičeva', 'Čebelarska', 'Tržnica Koseze', 'Zgornja Šiška',
                       'Bolnica P Držaja', 'Na Jami', 'Stara cerkev', 'Tivoli', 'Bavarski Dvor',
                       'Razstavišče', 'Bežigrad', 'Prekmurksa', 'Savske stolpnice', 'Žale', 'Pokopališka', 'Šola Jarše',
                       'Jarše', 'Kodrova', 'Žito', 'Nove Jarše', 'Bratislavksa', 'Yulon', 'Leskovškova', 'GZL', 'Rog',
                       'Letališka'],
    '14 (Vrhovci)': ['Savlje', 'Kališnikov trg', 'Čerinova', '7. septembra', 'Gorjančeva', 'Pohorskega bataljona',
                     'Brinje', 'Vodovodna', 'Podmilščakova', 'Bratov Židan', 'Parmova', 'Hranilniška', 'Razstavišče',
                     'Bavarski dvor', 'Ajdovščina', 'Konzorcij', 'Cankarjev dom', 'Pod Rožnikom',
                     'Študentsko naselje', 'Rožna dolina', 'Cesta XV', 'Jamnikarjeva', 'Viško polje', 'Podmornica',
                     'Preval', 'Brdo', 'Vrhovci'],
    '14 (Savlje)': ['Vrhovci', 'Brdo', 'Preval', 'Podmornica', 'Viško polje', 'Jamnikarjeva', 'Cesta XV',
                    'Rožna dolina', 'Študentsko naselje', 'Pod Rožnikom', 'Cankarjev dom', 'Pošta', 'Bavarski Dvor',
                    'Razstavišče', 'Hranilniška', 'Parmova', 'Bratov Židan', 'Podmilščakova', 'Vodovodna', 'Brinje',
                    'Pohorskega bataljona', 'Gorjančeva', '7. septembra', 'Čerinova', 'Kališnikov trg', 'Savlje']
}
train_stations = {
    'Ljubljana - Grosuplje': ['Ljubljana', 'Ljubljana - Vodmat', 'Ljubljana - Rakovnik','Škofljica', 'Šmarje-Sap',
                              'Grosuplje'],
    'Grosuplje - Ljubljana': ['Grosuplje', 'Šmarje-Sap', 'Škofljica', 'Ljubljana - Rakovnik', 'Ljubljana - Vodmat',
                              'Ljubljana'],
    'Ljubljana - Borovnica': ['Ljubljana', 'Ljubljana Tivoli', 'Brezovica', 'Notranje Gorice', 'Preserje', 'Borovnica'],
    'Brezovica - Ljubljana': ['Brezovica', 'Preserje', 'Notranje Gorice', 'Brezovica', 'Ljubljana Tivoli', 'Ljubljana'],
    'Kranj - Ljubljana': ['Kranj', 'Škofja Loka', 'Reteče', 'Medvode', 'Medno', 'Ljubljana Vižmarje',
                          'Ljubljana Stegne', 'Litostroj', 'Ljubljana'],
    'Ljubljana - Kranj': ['Ljubljana', 'Litostroj', 'Ljubljana Stegne', 'Ljubljana Vižmarje', 'Medno', 'Medvode',
                          'Reteče', 'Škofja Loka', 'Kranj'],
    'Ljubljana - Litija': ['Ljubljana', 'Ljubljana Polje', 'Ljubljana Zalog', 'Laze', 'Jevnica', 'Kresnice', 'Litija'],
    'Litija - Ljubljana': ['Litija', 'Kresnice', 'Jevnica', 'Laze', 'Ljubljana Zalog', 'Ljubljana Polje', 'Ljubljana'],
    'Ljubljana - Kamnik': ['Ljubljana', 'Ljubljana Brinje', 'Ljubljana Ježica', 'Ljubljana Črnuče', 'Trzin ind. cona',
                           'Trzin Mlake', 'Trzin', 'Domžale', 'Rodica', 'Jarše-Mengeš', 'Homec pri Kamniku',
                           'Šmarca', 'Duplica-Bakovnik', 'Kamnik'],
    'Kamnik - Ljubljana': ['Kamnik', 'Duplica-Bakovnik', 'Šmarca', 'Homec pri Kamniku', 'Rodica', 'Domžale', 'Trzin',
                           'Trzin Mlake', 'Trzin ind. cona', 'Ljubljana Črnuče', 'Ljubljana Ježica', 'Ljubljana Brinje'
                           'Ljubljana']
}
# bus_stations = {'27 (NS Rudnik)': ['Letališka', 'Rog', 'GZL'],
#             '20 (Fuzine)': ['Križanke', 'Drama']}


bus_stations = clean_stations(bus_stations)
train_stations = clean_stations(train_stations)
