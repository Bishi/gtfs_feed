#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

import json
import pycurl
from io import BytesIO
from init_objects import read_data


def create_routes_dict():
    """
    This method creates the 'out/routes_dict.json' file needed for create_bus_routes()
    :return: /
    """
    buffer = BytesIO()
    handle = pycurl.Curl()
    handle.setopt(pycurl.URL, 'http://www.lpp.si/sites/default/files/lpp_vozniredi/iskalnik/index.php?stop=0&line=212')
    handle.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    handle.setopt(pycurl.WRITEDATA, buffer)
    handle.perform()
    handle.close()

    body = buffer.getvalue()
    # print(body.decode('UTF-8'))
    tmp_body = body.decode('UTF-8')

    print(tmp_body)

    # Writes the HTML contents fo the LPP url to out/out_rotues.txt
    f = open('out/out_routes.txt', 'w+')
    f.write(tmp_body)
    f.close()

    # The HTML contains two quasi lists; the first one is a list of all stations in Ljubljana, the second one is
    # the list of all bus routes in Ljubljana. The station section is saved to 'out/select1' and the routes section
    # is saved to 'out/select2'
    f_read = open('out/out_routes.txt', 'r+')
    select = False
    count = 1
    for line in f_read:
        if select:
            f.write(line)
        if '<select' in line:
            select = True
            f = open('out/select'+str(count)+".txt", 'w+')
        if '</select' in line:
            select = False
            f.close()
            count += 1

    f_read.close()

    # 'out/select2.txt' parsing into a dictionary and into a .json file. This is needed for 'create_bus_routes()' to get all
    # valid url addresses for our routes
    f_routes = open('out/select2.txt', 'r+')

    routes_dict = {}

    for line in f_routes:
        if 'value=' in line:
            split1 = line.split("value=")
            print("split1[0]  " + split1[0])
            split2 = split1[1].split(">")
            print("split2[0]  " + split2[0])
            print("split2[1]  " + split2[1])
            split3 = split2[1].split("</op")
            print("split3[0]  " + split3[0])
            key = split2[0].replace('"', '')
            value = split3[0]

            print("Key: %s Value %s" % (key, value))
            routes_dict[key] = value

    routes_dict.pop('0', None)
    # routes_dict.pop('.', None)

    print("KEY AND VALUES:\n")
    for key, value in routes_dict.items():
        print(key, value)

    with open('out/routes_dict.json', 'w') as fp:
        json.dump(routes_dict, fp)

    f_routes.close()


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


if __name__ == '__main__':
    create_routes_dict()
    create_bus_routes()
