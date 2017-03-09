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
import pandas as pd
import numpy as np

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

def find(df, current_flight, countries_visited, trips, flights_of_trip_ind):
    # print('--->')
    if current_flight['srccountry'] == current_flight['destcountry']:
        # print('<--- -1 src=dest')
        return -1
    countries_visited.append(current_flight['destcountry'])
    # flights_of_trip_df = flights_of_trip_df.append(current_flight)
    # flights_of_trip_df.loc[len(flights_of_trip_df)] = current_flight
    flights_of_trip_ind.append(current_flight.name)
    # print('visited: ', len(countries_visited), countries_visited)
    # print(countries_visited)

    if len(countries_visited) < 3:
        potentional_dests = df[ (current_flight['dest'] == df['src']) &
                                (current_flight['arrtime'] < df['deptime']) &
                                (~df['destcountry'].isin(countries_visited)) &
                                ( ( pd.to_datetime(df['arrtime']) - pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']) ) < pd.to_timedelta('365 days') ) &
                                (True)
                                ].sort_values(by='deptime')
        # print('{:} potentional destinations'.format(len(potentional_dests)))
        # if len(potentional_dests) > 0: print(potentional_dests)
        if len(potentional_dests) > 0:
            for index, flight in potentional_dests.iterrows():
                # print('flight index {:}, {:} ({:}) -> {:} ({:})'.format(index, flight['src'], flight['srccountry'], flight['dest'], flight['destcountry']))
                # print(len(countries_visited))
                find(df, flight, countries_visited, trips, flights_of_trip_ind)
            countries_visited.pop()
            flights_of_trip_ind.pop()
            # print('<--- 1 destinace prohledany')
            return 1
        else:
            # zadne dalsi destinace, slepa vetev, vyhod aktualni destinaci z listu
            countries_visited.pop()
            flights_of_trip_ind.pop()
            # print('<--- -1 zadne destinace')
            return -1

    elif len(countries_visited) == 3:
        # nalezeno pozadovanych 10 letu, uloz to jako trip a odstran posledni, at muze pokracovat ve hledani od minuleho letu
        # trips.append(countries_visited[:])
        trips.append(flights_of_trip_ind[:])
        # print('<--- 2 nalezeno 10', countries_visited)
        countries_visited.pop()
        flights_of_trip_ind.pop()
    # print(len(trips))

def main(in_path):
    # Create airport: country dict
    iata_country = create_airport_dict()

    # Create input data dataframe
    df = pd.read_csv(in_path, sep=';', names=['src', 'dest', 'deptime', 'arrtime'], skiprows=1, parse_dates=True)
    # Add country columns to the dataframe
    df['srccountry'] = df.apply(lambda x: iata_country.get(x['src'], 'unknown'), axis=1)
    df['destcountry'] = df.apply(lambda x: iata_country.get(x['dest'], 'unknown'), axis=1)

    # print(df[(df['srccountry']=='CZ') & (df['destcountry']=='SK')].sort_values(by='deptime'))

    # stop = df.iloc[0]
    # print(stop)
    # print(df[ (df['src'] == df.iloc[0]['dest']) & (df['deptime'] > df.iloc[0]['arrtime']) ].sort_values(by='deptime')[:5])
    # print(df[ (df['src'] == stop['dest']) & (df['deptime'] > stop['arrtime']) ].sort_values(by='deptime').iloc[0])

    # Hledani destinaci z daneho mista, serazeno
    # print(df[df['src']=='KBP'].sort_values(by='deptime'))

    # print(df[:10])

    trips = []
    countries_visited = []
    # flights_of_trip_df = pd.DataFrame()
    flights_of_trip_ind = []
    flight = df.iloc[0]
    # print(flight)
    # print(flight.name)
    # flights_of_trip_ind.append(flight.name)
    # print(pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']))

    countries_visited.clear()
    countries_visited.append(flight.srccountry)
    if find(df, flight, countries_visited, trips, flights_of_trip_ind) == -1:
        print('Nothing found')

    for trip in trips:
        print(trip)
    # print(trips)

    print(len(trips), 'nalezenych tripu')
    print('Posledni je:')
    for i in range(len(trips[-1])):
        print(df.loc[trips[-1][i]])

    # rozdil = pd.to_datetime(flight['arrtime'])-pd.to_datetime(flight['deptime'])
    # rok = pd.to_timedelta('0 days 15:26:00')
    # print(rozdil)
    # print(rok)
    # print(rozdil < rok)

    # Hledani destinaci z daneho mista, serazeno
    # print(df[df['src']=='LHR'].sort_values(by='deptime'))


    # print(df.iloc[12455])
    # join_df(in_path)

if __name__ == '__main__':
    main(sys.argv[1])
