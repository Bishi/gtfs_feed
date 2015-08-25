#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

import zipfile
import os
from init_GTFS import init_GTFS
from init_objects import init_stations, print_routes, init_routes, init_trips, init_calendar, init_stop_times
from init_objects import init_fares, route_type_dict
from stations import bus_stations, train_stations

if __name__ == '__main__':
    # stop_id++ for every station, starting at 1000
    stop_id = 1000
    bus_routes, stop_id = init_stations(bus_stations, stop_id, route_type_dict['Bus'])
    train_routes, stop_id = init_stations(train_stations, stop_id, route_type_dict['Rail'])

    init_GTFS()

    print_routes(bus_stations, bus_routes)
    print_routes(train_stations, train_routes)

    route_list = init_routes(bus_routes, train_routes)

    trips = init_trips(route_list)

    fare_attributes, fare_rules = init_fares(bus_routes, train_routes)

    # all routes work 7 days per week
    calendar = init_calendar(trips, 1, 1, 1, 1, 1, 1, 1, 20070101, 20170101)

    stop_times = init_stop_times(route_list)

    with open('gtfs/stops.txt', 'a') as f:
        for s in bus_stations:
            for r in bus_routes[s]:
                line = "\n" + str(r.stop_id) + "," + r.name + "," + str(r.lat) + "," + str(r.lon)
                f.write(line)
        for s in train_stations:
            for r in train_routes[s]:
                line = "\n" + str(r.stop_id) + "," + r.name + "," + str(r.lat) + "," + str(r.lon)
                f.write(line)
        f.close()

    with open('gtfs/routes.txt', 'a') as f:
        for r in route_list:
            line = "\n" + str(r.route_id) + "," + str(r.route_short_name) + "," + str(r.route_long_name) + ","\
                   + str(r.route_type)
            f.write(line)
        f.close()

    with open('gtfs/trips.txt', 'a') as f:
        for t in trips:
            line = "\n" + str(t.route_id) + "," + str(t.service_id) + "," + str(t.trip_id) + "," + ","
            f.write(line)
        f.close()

    # calendar not implemented correctly
    with open('gtfs/calendar.txt', 'a') as f:
        for c in calendar:
            line = "\n" + str(c.service_id) + "," + str(c.monday) + "," + str(c.tuesday) + ","\
                   + str(c.wednesday) + "," + str(c.thursday) + "," + str(c.friday) + ","\
                   + str(c.saturday) + "," + str(c.sunday) + "," + str(c.start_date) + "," + str(c.end_date)
            f.write(line)
        f.close()

    with open('gtfs/stop_times.txt', 'a') as f:
        for st in stop_times:
            line = "\n" + str(st.trip_id) + "," + str(st.arrival_time) + "," + str(st.departure_time) + ","\
                   + str(st.stop_id) + "," + str(st.stop_sequence)
            f.write(line)
        f.close()

    with open('gtfs/frequencies.txt', 'a') as f:
        for r in route_list:
            if r.route_type == route_type_dict['Bus']:
                line = ("\n%s,05:00:00,23:30:00,60" % r.route_id) # a bus comes every minute
            elif r.route_type == route_type_dict['Rail']:
                line = ("\n%s,05:00:00,23:30:00,600" % r.route_id) # a train comes every 10 minutes
            f.write(line)
        f.close()

    with open('gtfs/fare_attributes.txt', 'a') as f:
        for a in fare_attributes:
            line = "\n" + str(a.fare_id) + "," + str(a.price) + "," + str(a.currency_type) + ","\
                   + str(a.payment_method) + "," + str(a.transfers) + "," + str(a.transfer_duration)
            f.write(line)
        f.close()

    with open('gtfs/fare_rules.txt', 'a') as f:
        for a in fare_rules:
            line = "\n" + str(a.fare_id) + "," + str(a.route_id)
            f.write(line)
        f.close()

    # zip the file -> gtfs.zip
    zf = zipfile.ZipFile('gtfs/gtfs.zip', 'w', zipfile.ZIP_DEFLATED)
    try:
        zf.write('gtfs/stops.txt', os.path.relpath('gtfs/stops.txt', 'gtfs'))
        zf.write('gtfs/routes.txt', os.path.relpath('gtfs/routes.txt', 'gtfs'))
        zf.write('gtfs/agency.txt', os.path.relpath('gtfs/agency.txt', 'gtfs'))
        zf.write('gtfs/trips.txt', os.path.relpath('gtfs/trips.txt', 'gtfs'))
        zf.write('gtfs/calendar.txt', os.path.relpath('gtfs/calendar.txt', 'gtfs'))
        zf.write('gtfs/stop_times.txt', os.path.relpath('gtfs/stop_times.txt', 'gtfs'))
        zf.write('gtfs/frequencies.txt', os.path.relpath('gtfs/frequency.txt', 'gtfs'))
        zf.write('gtfs/shapes.txt', os.path.relpath('gtfs/shapes.txt', 'gtfs'))
        zf.write('gtfs/fare_attributes.txt', os.path.relpath('gtfs/fare_attributes.txt', 'gtfs'))
        zf.write('gtfs/fare_rules.txt', os.path.relpath('gtfs/fare_rules.txt', 'gtfs'))
        print("\nCreating zip file")
        zf.close()
    except:
        zf.close()
