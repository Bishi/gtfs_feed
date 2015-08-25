#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from urllib import parse, request
from time import sleep
import simplejson
from objects import Stop, Route, Trip, StopTime, Calendar, FareAttribute, FareRule


route_type_dict = {'Tram': 0, 'Subway': 1, 'Rail': 2, 'Bus': 3, 'Ferry': 4,
                   'Cable car': 5, 'Gondola': 6, 'Funicular': 7}


# Get coordinates from address (in our case station name), returns Station object with id, name, lat, lon
# If you call get_coordinates(id, 'address'), it will send a request with 'Transit stop address' as address
def get_coordinates(i, address, city='', station="Transit stop", from_sensor=False):
    google_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    query = station + " " + address + " " + city
    query = query.encode('UTF-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false",
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


# returns dict with Station object list
# takes either bus_stations or train_stations as parameters
# routes = {route_name:[station_object_list]}
# use sleep(0.3) if the servers are busy
def init_stations(stations, stop_id, route_type):
    routes = {}
    for r in stations:
        route_list = []
        print("  " + r)
        for address in stations[r]:
            station_object = None
            try:
                if route_type == route_type_dict['Bus']:
                    station_object = get_coordinates(stop_id, address, 'Ljubljana', 'Transit stop', False)
                elif route_type == route_type_dict['Rail']:
                    station_object = get_coordinates(stop_id, address, '', 'Train stop', False)
                stop_id += 1
                if station_object:
                    route_list.append(station_object)
            except:
                print("No value")
            # sleep(0.3)
        routes[r] = route_list
        print()
    return routes, stop_id


# returns routes dict with Routes object list
def init_routes(bus_routes, train_routes):
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


# prints all the bus or train stations in order
def print_routes(stations, routes):
    print()
    for s in stations:
        print("\n  Route %s, %s stops." % (s, str(len(routes[s]))))
        for r in routes[s]:
            print(r.name, r.lat, r.lon)


# returns list of Trip objects
def init_trips(routes):
    trip_list = []
    i = 1
    for r in routes:
        trip_object = Trip(r.route_id, i, i)
        i += 1
        trip_list.append(trip_object)
    return trip_list


# returns list of Calendar objects
def init_calendar(trips, monday, truestday, wednesday, thursday, friday, saturday, sunday, start_date, end_date):
    calendar_list = []
    for t in trips:
        service_object = Calendar(t.trip_id, monday, truestday, wednesday,
                                  thursday, friday, saturday, sunday, start_date, end_date)
        calendar_list.append(service_object)
    return calendar_list


# returns list of StopTime objects
# not implemented correctly, adds duplicate stations
# 1min30sec travel time between ALL adjacent stations
def init_stop_times(routes):
    stop_times_list = []
    # arrival_time = '12:00:00'
    # departure_time = '12:00:00'
    trip = 1
    for r in routes:
        time = 21600  # 6am
        sequence = 1
        if r.route_type == route_type_dict['Bus']:
            interval = 90 # 1.5min for bus
        elif r.route_type == route_type_dict['Rail']:
            interval = 300 # 5min for rail
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


# returns list of fare attributes and list of fare rules
def init_fares(bus_routes, train_routes):
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


# replace slovene characters from station and route names
def clean_stations(stations):
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
