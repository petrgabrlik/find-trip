#!/usr/bin/env python

'''
Trip finder

TODO:
- OK ke kodu letiste zjistit zemi
- vytvorit tridu pro kazdy trip?
- nastudovat spravne predavani argumentu z command line
'''

__author__ = "Petr Gabrlik"
__email__ = "petrgabrlik@email.cz"
__license__ = "MIT"

import sys
import csv

CHANGE_MIN_TIME = 1
FLIGHTS_PER_TRIP = 10
COUNTRIES_PER_TRIP = FLIGHTS_PER_TRIP

def create_airport_dict():
    '''
    Create dictionary of airports and their countries.

    This function creates a dictionary containing codes of
    airports (IATA) and codes of countries (ISO 3166-1 alpha-2) in
    the following format: key: value = iata_airport: iso_country.

    The data is obtained form *.csv file containing airport
    information. Data source: http://ourairports.com/data/
    '''
    path = 'airports.csv'
    iata_country = {}
    with open(path, encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"',
                            skipinitialspace=True)
        next(reader, None) # skip header
        for line in reader:
            iata_country[line[13]] = line[8]

    return iata_country

def main(in_path):
    iata_country = create_airport_dict()

    # path = 'input_data.csv'
    unknown_iata = set()
    with open(in_path, encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=';', skipinitialspace=True)
        next(reader, None) # skip header
        for line in reader:
            if len(line) == 4:
                try:
                    print(line, iata_country[line[0]])
                except:
                    unknown_iata.add(line[0])

    print(unknown_iata)

if __name__ == '__main__':
    main(sys.argv[1])
