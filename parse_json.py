#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from init_objects import read_data

if __name__ == '__main__':
    data = read_data('routes.geojson')

    print(data.keys())
    # print(data['features'][0]['properties']['@relations'][0]['reltags']['ref'])

    # for r in data['features'][0]['properties']['@relations']:
    #     print(r['reltags']['ref'])

    # for d in data['features']:
    #     if '@relations' in d['properties']:
    #         for r in d['properties']['@relations']:
    #             if r['reltags']['ref'] == '7L' and 'name' in r['reltags']['ref']:
    #                 # print(r['reltags']['ref'])
    #
    #                 print(d['properties']['name'])

    f = open('out/out_json.txt', 'w+')
    for d in data['features']:
        # for f in d['properties']:
        ref = ''
        if 'name' in d['properties'] and 'highway' in d['properties']:
            if d['properties']['highway'] == 'bus_stop':
                print(d['properties']['name'])
                name = d['properties']['name']
                if 'ref' in d['properties']:
                    ref = d['properties']['ref']
                else:
                    ref = d['properties']['name'].partition(' ')[0]
                line = "%s - %s\n" % (name, ref)
                f.write(line)
    f.close()
