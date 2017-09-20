#!/usr/bin/python
import sys
import argparse
from geoip import geolite2

class ownParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
 
country_list = []
country_time = []
if __name__ == '__main__':
    parser = ownParser(description='Script que llista el numero de visites per paisos')
    parser.add_argument(dest='log_file', action='store', help='fitxer de access on parsejar les peticions')
    parser.add_argument('-g', dest='grep_str', action='store', help='string per filtrar les peticions')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Activa el mode Debug')

    args=parser.parse_args()

    f = open(args.log_file, 'r')
    for line in f.readlines():
	if args.grep_str is None or args.grep_str in line:
            ip = line.split()[0]
            if args.debug: print ip
            match = geolite2.lookup(ip)
            if match is not None:
                if args.debug: print match.country
                if match.country in country_list:
                    if args.debug: print country_list.index(match.country)
                    if args.debug: print country_time[country_list.index(match.country)]
                    country_time[country_list.index(match.country)] = country_time[country_list.index(match.country)] + 1
                else:
                    country_time.append(1)
                    country_list.append(match.country)

    for country in country_list:
        print "%6i %4s"%(country_time[country_list.index(country)], country) 



