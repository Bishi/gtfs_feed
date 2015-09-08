#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

import json
import pycurl
from io import BytesIO


def create_routes_dict():
    """
    This method creates the 'out/routes_dict.json' file needed for parse_routes.create_bus_routes()
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

    # 'out/select2.txt' parsing into a dictionary and into a .json file. This is needed for 'parse_routes.py' to get all
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
