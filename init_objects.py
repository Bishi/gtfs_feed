#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from urllib import parse, request
import simplejson
import json
from objects import Stop, Route, Trip, StopTime, Calendar, FareAttribute, FareRule


route_type_dict = {'Tram': 0, 'Subway': 1, 'Rail': 2, 'Bus': 3, 'Ferry': 4,
                   'Cable car': 5, 'Gondola': 6, 'Funicular': 7}


def get_coordinates(i, address, city='', station="Transit stop"):
    """
    Get coordinates from address (in our case station name)
    If you call get_coordinates(id, 'address'), it will send a request with 'Transit stop address' as address
    Only used for Rail stations
    :param i: stop_id
    :param address: used for google API query eg. 'Ljubljana Črnuče'
    :param city: add a specific city ot the query
    :param station: add a station type to the query
    :return: Station object with id, name, lat, lon
    """
    google_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    query = station + " " + address + " " + city
    query = query.encode('UTF-8')
    params = {
        'address': query,
        'sensor': "false",
        # use one of the api keys
        'key': 'AIzaSyCyG3oGgSUQkjq5IrgM9SkE_0rqXlS_an0'
        # 'key': 'AIzaSyA6tXxhtw-kSt14NKgyqHtBq1RoVPEiOu4'
        # 'key': 'AIzaSyCWzpKbodAy8D-DfaC_WXLdBIVw8tsTlq8'
        # 'key': 'AIzaSyBIM2IllcbT-SIxK6jBn7FkEdKgjc1W3VM'
    }
    url = google_geocode_url + parse.urlencode(params)
    json_response = request.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        long_address = response['results'][0]['formatted_address']
        station_object = Stop(i, address, latitude, longitude)
        # print(query.decode('UTF-8'))
        print("'%s': %s %s, Long address: '%s'" % (station_object.name, station_object.lat,
                                                   station_object.lon, long_address))
    else:
        print("'%s' <No Results>" % (query.decode("UTF-8")))
        station_object = None
    return station_object if station_object else None


def get_coordinates_json(i, name, file):
    """
    Get coordinates from json file. 'name' is the station number from bus_stations dict.
    eg. "402042" - > "402042 ~ Bolnica 46.0544176 14.5293393"
    Only used for Bus stations
    :param i: stop_id
    :param name: station ID eg. '204031'
    :param file: get data from which file eg. ljubljana.geojson
    :return: Station object with id, name, lat, lon
    """
    data = read_data(file)
    station_object = None
    for d in data['features']:
        try:
            station_number = d['properties']['name'].partition(' ')[0]
            station_name = d['properties']['name']
            if "ref" in d['properties']:
                station_number = d['properties']['ref']
            if station_number == name:
                print("Station num %s name %s" % (station_number, d['properties']['name']))
                station_name = station_name.replace(',', ';')
                station_object = Stop(i, station_name,
                                      d['geometry']['coordinates'][1],
                                      d['geometry']['coordinates'][0])
        except:
            pass
    return station_object if station_object else None


def init_stations(stations, stop_id, route_type):
    """
    Use sleep(0.3) if the servers are busy
    routes = {route_name:[station_object_list]}
    :param stations: takes either bus_stations or train_stations as parameters
    :param stop_id: all stations must have a different ID
    :param route_type: either Bus or Rail
    :return: dict with Stop object list
    """
    routes = {}
    for r in stations:
        route_list = []
        print("  " + r)
        for address in stations[r]:
            station_object = None
            try:
                if route_type == route_type_dict['Bus']:
                    # station_object = get_coordinates(stop_id, address, 'Ljubljana', 'Transit stop', False)
                    station_object = get_coordinates_json(stop_id, address, 'ljubljana.geojson')
                elif route_type == route_type_dict['Rail']:
                    station_object = get_coordinates(stop_id, address, '', 'Train stop')
                stop_id += 1
                if station_object:
                    route_list.append(station_object)
            except ValueError:
                print("No value")
        routes[r] = route_list
        print()
    return routes, stop_id


def init_routes(bus_routes, train_routes):
    """
    :param bus_routes: dict of all bus routes
    :param train_routes: dict of all train routes
    :return: routes dict with Routes object list
    """
    route_list = []
    i = 1
    for r in bus_routes:
        route_object = Route(i, r, r, route_type_dict['Bus'], bus_routes[r])
        route_list.append(route_object)
        i += 1
    for r in train_routes:
        route_object = Route(i, r, r, route_type_dict['Rail'], train_routes[r])
        route_list.append(route_object)
        i += 1
    return route_list


def print_routes(stations, routes):
    """
    Prints all the bus or train stations in order
    :param stations: dict of all stations
    :param routes: dict of all routes
    :return:
    """
    print()
    for s in stations:
        print("\n  Route %s, %s stops." % (s, str(len(routes[s]))))
        for r in routes[s]:
            print(r.name, r.lat, r.lon)


def init_trips(routes):
    """
    :param routes:
    :return: list of Trip objects
    """
    trip_list = []
    i = 1
    for r in routes:
        trip_object = Trip(r.route_id, i, i)
        i += 1
        trip_list.append(trip_object)
    return trip_list


def init_calendar(trips, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date):
    """
    :return: list of Calendar objects
    """
    calendar_list = []
    for t in trips:
        service_object = Calendar(t.trip_id, monday, tuesday, wednesday,
                                  thursday, friday, saturday, sunday, start_date, end_date)
        calendar_list.append(service_object)
    return calendar_list


def init_stop_times(routes):
    """
    Not implemented correctly, adds duplicate stations
    1min30sec travel time between bus and 5min between rail stations
    :param routes: list of all routes
    :return: list of StopTime objects
    """
    stop_times_list = []
    trip = 1
    for r in routes:
        interval = 0  # init interval
        time = 21600  # 6am
        sequence = 1
        if r.route_type == route_type_dict['Bus']:
            interval = 90  # 1.5min for bus
        elif r.route_type == route_type_dict['Rail']:
            interval = 300  # 5min for rail
        for a in r.stops:
            # converts seconds to hours:minutes:seconds
            m, s = divmod(time, 60)
            h, m = divmod(m, 60)
            tmp_time = "%02d:%02d:%02d" % (h, m, s)
            stop_time_object = StopTime(trip, tmp_time, tmp_time, a.stop_id, sequence)
            stop_times_list.append(stop_time_object)
            sequence += 1
            time += interval
        trip += 1
    return stop_times_list


def init_fares(bus_routes, train_routes):
    """
    :param bus_routes: dict of all bus routes
    :param train_routes: dict of all train routes
    :return: list of fare attributes and list of rfare rules
    """
    fare_payment = {'On board': 0, 'Before boarding': 1}
    transfer_type = {'None': 0, 'One': 1, 'Two': 2, 'Unlimited': ''}
    # bus price = 1.2 EUR, train price = 5 EUR
    fare_attributes_list = [FareAttribute(1, 1.2, 'EUR', fare_payment['On board'], transfer_type['Unlimited'], 5400),
                            FareAttribute(2, 5, 'EUR', fare_payment['On board'], transfer_type['Unlimited'], 5400)]
    fare_rule_list = []
    route_id = 1
    for r in bus_routes:
        fare_rule_object = FareRule(1, route_id)
        fare_rule_list.append(fare_rule_object)
        route_id += 1
    for r in train_routes:
        fare_rule_object = FareRule(2, route_id)
        fare_rule_list.append(fare_rule_object)
        route_id += 1
    return fare_attributes_list, fare_rule_list


def clean_stations(stations):
    """
    Replace slovene characters from station and route names
    :param stations: dict that needs to be cleaned
    :return: dict containing no slovene characters
    """
    tmpr = {}
    for r in stations:
        tmps = []
        r_tmp = r.replace('ž', 'z').replace('š', 's').replace('č', 'c').replace('ć', 'c').replace('đ', 'd')
        r_tmp = r_tmp.replace('Ž', 'Z').replace('Š', 'S').replace('Č', 'C').replace('Ć', 'C').replace('Đ', 'D')
        stations[r_tmp] = stations.pop(r)  # stations.pop replaces key with new one
        for s in stations[r_tmp]:
            s = s.replace('ž', 'z').replace('š', 's').replace('č', 'c').replace('ć', 'c').replace('đ', 'd')
            s = s.replace('Ž', 'Z').replace('Š', 'S').replace('Č', 'C').replace('Ć', 'C').replace('Đ', 'D')
            tmps.append(s)
        tmpr[r_tmp] = tmps
    return tmpr


def read_data(file):
    """
    Reads json data from file
    :param file: json file
    :return: data from json file
    """
    with open(file) as f:
        data = json.load(f)
        return data
