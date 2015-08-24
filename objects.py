class Stop(object):

    def __init__(self, stop_id, name, lat, lon):
        self.stop_id = stop_id
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return self.name


class Route(object):

    def __init__(self, route_id, route_short_name, route_long_name, route_type, stops):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type
        self.stops = stops

    def __str__(self):
        return self.route_long_name


class Trip(object):

    def __init__(self, route_id, service_id, trip_id):
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id

    def __str__(self):
        return str(self.trip_id)


class StopTime(object):

    def __init__(self, trip_id, arrival_time, departure_time, stop_id, stop_sequence):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence

    def __str__(self):
        return str(self.stop_id)


class Calendar(object):

    def __init__(self, service_id, monday, tuesday, wednesday, thursday,
                 friday, saturday, sunday, start_date, end_date):
        self.service_id = service_id
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self. thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return str(self.service_id)
