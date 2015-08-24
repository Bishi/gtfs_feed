#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from init_objects import clean_stations

# missing some stations
# stations have to be in order: first stop -> last stop
bus_stations = {
    '27 (NS Rudnik)': ['Letali�ka', 'Rog', 'GZL', 'Leskov�kova', 'Yulon', 'BTC - Emporium', 'BTC - Kolosej', 'Tr�nica',
                       'BTC - Uprava', 'Jar�e', '�ola Jar�e', 'Flaj�manova', 'Sredi�ka', 'Viadukt', 'Fri�kovec',
                       'Kolodvor', 'Bavarski dvor', 'Po�ta', 'Drama', 'Kri�anke', 'Gornji trg', 'Privoz', 'Streli��e',
                       'I�anska', 'Galjevica', 'Mihov �tradon', 'Jur�kova', 'Bobrova', 'NS Rudnik'],
    '20 (Fu�ine)': ['Nove Sto�ice P+R', 'Maroltova', 'Puhova', 'Kardeljeva plo��ad', 'Gasilska brigada', 'Be�igrad',
                    'Razstavi��e', 'Bavarski dvor', 'Dalmatinova', 'Turist', 'Zmajski most', 'Poljanska',
                    'Ambro�ev trg', 'Ro�ka', 'Klini�ni center', 'Bolnica', 'Tr�nica Moste', 'Zalo�ka', 'Brodarjev trg',
                    'Preglov trg', 'Rusjanov trg ', 'Fu�ine P+R'],
    '27 (Letali�ka)': ['NS Rudnik', 'Bobrova', 'Jur�kova', 'Mihov �tadron', 'Galjevica', 'I�anska', 'Steli��e',
                       'Privoz', 'Gornji trg', 'Kri�anke', 'Drama', 'Po�ta', 'Bavarski dvor', 'Kolodvor', 'Fri�kovec',
                       'Viadukt', 'Sredi�ka', 'Flaj�manova', '�ola Jar�e', 'Jar�e', 'BTC - Uprava', 'Tr�nica',
                       'BTC - Kolosej', 'BTC - Emporium', 'Yulon', 'Leskov�kova', 'GZL', 'Rog', 'Letali�ka'],
    '20 (Nove Sto�ice)': ['Fu�ine P+R', 'Rusjanov trg', 'Preglov trg', 'Brodarjev trg', 'Pot na Fu�ine', 'Zalo�ka',
                          'Tr�nica Moste', 'Bolnica', 'Klini�ni center', 'Ambro�ev trg', 'Poljanska', 'Zmajski most',
                          'Tav�arjeva', 'Bavarski dvor', 'Razstavi��e', 'Be�igrad', 'Kr�i�eva', 'Gasilska Brigada',
                          'Puhova', 'Nove Sto�ice'],
    '6 (�rnu�e)': ['Dolgi most P+R', 'Bonifacija', 'Vi�', 'Glince', 'Stan in dom', 'Hajdrihova', 'Toba�na', 'A�ker�eva',
                   'Drama', 'Konzorcij', 'Ajdov��ina', 'Bavarski dvor', 'Razstavi��e', 'Astra', 'Stadion', 'Mercator',
                   'AMZS', 'Smelt', 'Sto�ice', 'Ruski car', 'Je�ica', 'Sava', 'Kolodvor �rnu�e', 'Rogovilc', '�rnu�e'],
    '6 (Dolgi most P+R)': ['�rnu�e', 'Rogovilc', 'Kolodvro �rnu�e', 'Sava', 'Je�ica', 'Ruski car', 'Sto�ice', 'Smelt',
                           'AMZS', 'Mercator', 'Stadion', 'Astra', 'Razstavi��e', 'Bavarski dvor', 'Po�ta', 'Drama',
                           'A�ker�eva', 'Toba�na', 'Hajdrihova', 'Staon in dom', 'Glince', 'Vi�', 'Bonifacija',
                           'Dolgi most P+R'],
    '7L (Pr�an)': ['Letali�ka', 'Rog', 'GZL', 'Lesko�kova', 'Yulon', 'Bratislavska', 'Nove Jar�e', '�ito', 'Kodrova',
                   'Jar�e', '�ola Jar�e', 'Pokopali�ka', '�ale', 'Savske Stolpnice', 'Prekmurska', 'Be�igrad',
                   'Razstavi��e', 'Bavarski Dvor', 'Hotel Lev', 'Tivoli', 'Stara cerkev', 'Na jami', 'Bolnica P Dr�aja',
                   'Zgornja �i�ka', 'Tr�nica Koseze', '�ebelarska', 'Ple�i�eva', 'Andreja Bitenca', 'Pr�an'],
    '7L (Letali�ka)': ['Pr�an', 'Andreja Bitenca', 'Ple�i�eva', '�ebelarska', 'Tr�nica Koseze', 'Zgornja �i�ka',
                       'Bolnica P Dr�aja', 'Na Jami', 'Stara cerkev', 'Tivoli', 'Bavarski Dvor',
                       'Razstavi��e', 'Be�igrad', 'Prekmurksa', 'Savske stolpnice', '�ale', 'Pokopali�ka', '�ola Jar�e',
                       'Jar�e', 'Kodrova', '�ito', 'Nove Jar�e', 'Bratislavksa', 'Yulon', 'Leskov�kova', 'GZL', 'Rog',
                       'Letali�ka'],
    '14 (Vrhovci)': ['Savlje', 'Kali�nikov trg', '�erinova', '7. septembra', 'Gorjan�eva', 'Pohorskega bataljona',
                     'Brinje', 'Vodovodna', 'Podmil��akova', 'Bratov �idan', 'Parmova', 'Hranilni�ka', 'Razstavi��e',
                     'Bavarski dvor', 'Ajdov��ina', 'Konzorcij', 'Cankarjev dom', 'Pod Ro�nikom',
                     '�tudentsko naselje', 'Ro�na dolina', 'Cesta XV', 'Jamnikarjeva', 'Vi�ko polje', 'Podmornica',
                     'Preval', 'Brdo', 'Vrhovci'],
    '14 (Savlje)': ['Vrhovci', 'Brdo', 'Preval', 'Podmornica', 'Vi�ko polje', 'Jamnikarjeva', 'Cesta XV',
                    'Ro�na dolina', '�tudentsko naselje', 'Pod Ro�nikom', 'Cankarjev dom', 'Po�ta', 'Bavarski Dvor',
                    'Razstavi��e', 'Hranilni�ka', 'Parmova', 'Bratov �idan', 'Podmil��akova', 'Vodovodna', 'Brinje',
                    'Pohorskega bataljona', 'Gorjan�eva', '7. septembra', '�erinova', 'Kali�nikov trg', 'Savlje']
}
train_stations = {
    'Ljubljana - Grosuplje': ['Ljubljana', 'Ljubljana - Vodmat', 'Ljubljana - Rakovnik','�kofljica', '�marje-Sap',
                              'Grosuplje'],
    'Grosuplje - Ljubljana': ['Grosuplje', '�marje-Sap', '�kofljica', 'Ljubljana - Rakovnik', 'Ljubljana - Vodmat',
                              'Ljubljana'],
    'Ljubljana - Borovnica': ['Ljubljana', 'Ljubljana Tivoli', 'Brezovica', 'Notranje Gorice', 'Preserje', 'Borovnica'],
    'Brezovica - Ljubljana': ['Brezovica', 'Preserje', 'Notranje Gorice', 'Brezovica', 'Ljubljana Tivoli', 'Ljubljana'],
    'Kranj - Ljubljana': ['Kranj', '�kofja Loka', 'Rete�e', 'Medvode', 'Medno', 'Ljubljana Vi�marje',
                          'Ljubljana Stegne', 'Litostroj', 'Ljubljana'],
    'Ljubljana - Kranj': ['Ljubljana', 'Litostroj', 'Ljubljana Stegne', 'Ljubljana Vi�marje', 'Medno', 'Medvode',
                          'Rete�e', '�kofja Loka', 'Kranj'],
    'Ljubljana - Litija': ['Ljubljana', 'Ljubljana Polje', 'Ljubljana Zalog', 'Laze', 'Jevnica', 'Kresnice', 'Litija'],
    'Litija - Ljubljana': ['Litija', 'Kresnice', 'Jevnica', 'Laze', 'Ljubljana Zalog', 'Ljubljana Polje', 'Ljubljana'],
    'Ljubljana - Kamnik': ['Ljubljana', 'Ljubljana Brinje', 'Ljubljana Je�ica', 'Ljubljana �rnu�e', 'Trzin ind. cona',
                           'Trzin Mlake', 'Trzin', 'Dom�ale', 'Rodica', 'Jar�e-Menge�', 'Homec pri Kamniku',
                           '�marca', 'Duplica-Bakovnik', 'Kamnik'],
    'Kamnik - Ljubljana': ['Kamnik', 'Duplica-Bakovnik', '�marca', 'Homec pri Kamniku', 'Rodica', 'Dom�ale', 'Trzin',
                           'Trzin Mlake', 'Trzin ind. cona', 'Ljubljana �rnu�e', 'Ljubljana Je�ica', 'Ljubljana Brinje'
                           'Ljubljana']
}
# bus_stations = {'27 (NS Rudnik)': ['Letali�ka', 'Rog', 'GZL'],
#             '20 (Fuzine)': ['Kri�anke', 'Drama']}


bus_stations = clean_stations(bus_stations)
train_stations = clean_stations(train_stations)
