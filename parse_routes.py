#!/usr/bin/python
# -*- coding: iso-8859-2 -*-
import json
import pycurl
from io import BytesIO
from init_objects import read_data


def create_bus_routes():
    """
    This method parses the HTML of the LPP page, eg.
    http://www.lpp.si/sites/default/files/lpp_vozniredi/iskalnik/index.php?stop=0&line=282
    It goes through all the entries contained in the 'out/routes_dicts.json' file, where the key (282 in the example's
    case) is an arbitrary value used in the LPP url to get the correct route number, and the value is the route name
    itself.

    :return: dictionary with bus routes eg. {'20 (Fuzine)': ['123451', '123461', '654261', ...], ...} where the key
    is the route name and the value is a list of all stations in that route, sorted from first to last. Also writes
    'out/routes.json', needed for the main program to get the bus boutes.
    """
    print("Making routes, please wait")

    routes_dict = read_data('out/routes_dict.json')

    url = 'http://www.lpp.si/sites/default/files/lpp_vozniredi/iskalnik/index.php?stop=0&line='

    final_routes_dict = {}

    for key, value in routes_dict.items():
        buffer = BytesIO()
        handle = pycurl.Curl()
        handle.setopt(pycurl.URL, url + '' + key)
        handle.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        handle.setopt(pycurl.WRITEDATA, buffer)
        handle.perform()
        handle.close()

        body = buffer.getvalue()
        # print(body.decode('UTF-8'))
        tmp_body = body.decode('UTF-8')

        tmp_file = open('out/tmp_file.txt', 'w+')
        tmp_file.write(tmp_body)
        tmp_file.close()
        tmp_file_read = open('out/tmp_file.txt', 'r+')
        table = False
        stations = []
        full_name = ''
        for line in tmp_file_read:
            if table:
                # print(line)
                pass
            if '<div class="col-md-6">' in line:
                table = True
            if line.startswith('            </div>'):
                final_routes_dict[full_name] = stations
                table = False
            if 'smer' in line:
                line_num = line.split('<b>')[1].split('</b>')[0]
                line_name = line.split('smer: <b>')[1].split('</b>')[0]
                full_name = "%s (%s)" % (line_num, line_name)
                stations = []
            if '<em>' in line:
                st_num = line.split('<em>')[1].split('</em>')[0]
                stations.append(st_num)

        # final_routes_dict[full_name] = stations
        tmp_file_read.close()

    # print(final_routes_dict)

    with open('out/routes.json', 'w') as fp:
        json.dump(final_routes_dict, fp)

    return final_routes_dict