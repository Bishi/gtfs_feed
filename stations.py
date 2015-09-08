#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from init_objects import clean_stations
from init_objects import read_data

train_stations = {
    'Ljubljana - Grosuplje': ['Ljubljana', 'Ljubljana - Vodmat', 'Ljubljana - Rakovnik', '�kofljica', '�marje-Sap',
                              'Grosuplje'],
    'Grosuplje - Ljubljana': ['Grosuplje', '�marje-Sap', '�kofljica', 'Ljubljana - Rakovnik', 'Ljubljana - Vodmat',
                              'Ljubljana'],
    'Ljubljana - Borovnica': ['Ljubljana', 'Ljubljana Tivoli', 'Brezovica', 'Notranje Gorice', 'Preserje', 'Borovnica'],
    'Borovnica - Ljubljana': ['Borovnica', 'Preserje', 'Notranje Gorice', 'Brezovica', 'Ljubljana Tivoli', 'Ljubljana'],
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
                           'Ljubljana'],
}

# Test routes
# bus_stations = {
#     '27 (NS Rudnik)': ['204051', '204041', '204031', '204021', '204011', '203191', '203141', '203241', '203131',
#                        '203121', '203111', '203101', '203091', '203041', '202043', '202012', '301011', '300011',
#                        '600012', '600022', '601012', '602022', '602062', '602102', '602112', '503014', '603122',
#                        '603094', '603152', '503052', '504042', '504122', '504052'],
# }

bus_stations = read_data('out/routes.json')
bus_stations = clean_stations(bus_stations)
train_stations = clean_stations(train_stations)


# remove redundant city lines
bus_stations.pop('28 (Mali Lipoglav)', None)
bus_stations.pop('29 (Kajuhova)', None)
bus_stations.pop('29 (Tuji Grm)', None)
bus_stations.pop('30 (Vodice)', None)
bus_stations.pop('30 (Medvode)', None)
bus_stations.pop('51 (Polhov Gradec)', None)
bus_stations.pop('52 (Crni Vrh)', None)
bus_stations.pop('52 (Polhov Gradec)', None)
bus_stations.pop('53 (Suhi Dol)', None)
bus_stations.pop('53 (Polhov Gradec)', None)
bus_stations.pop('56 (Ljubljana)', None)
bus_stations.pop('56 (Sentjost)', None)
bus_stations.pop('60 (Polje obracalisce)', None)
bus_stations.pop('60 (Ljubljana)', None)
bus_stations.pop('61 (Zapoge obracalisce)', None)
bus_stations.pop('61 (Vodice)', None)

for key, value in bus_stations.items():
    print(key)
