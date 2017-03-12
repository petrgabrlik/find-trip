#!/usr/bin/env python

'''
Solution for Kiwi python weekend entry task.

More info:
https://gist.github.com/MichalCab/2176c0eb2d996d906eea38e9ec9835d2
'''

__author__ = "Petr Gabrlik"
__email__ = "petrgabrlik@email.cz"

import sys
import csv
import pandas as pd
import time

FLIGHTS_PER_TRIP = 4
NUMBER_OF_TRIPS = 100
DEBUG = True

def create_airport_dict():
    '''
    Create dictionary of airports and their countries.

    This function creates and returns a dictionary containing codes
    of airports (IATA) and codes of countries (ISO 3166-1 alpha-2) in
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


def print_trip(df, trips):
    '''
    Print the trip in the desired format.

    df - dataframe containing all flights
    trips - list of the trips containing indexes of flights

    Format:
    <trip_id>;<country_code>;<source>;<destination>;
        <local_departure_time>;<local_arrival_time>

    Example:
    1;CZ;PRG;BRU;2017-03-04T13:15;2017-03-04T15:15
    1;AA;BRU;LON;2017-04-04T13:15;2017-04-04T15:15
    1;BB;LON;VIE;2017-05-04T13:15;2017-05-04T15:15
    1;CC;VIE;AAA;2017-06-04T13:15;2017-06-04T15:15
    1;DD;AAA;HHH;2017-07-04T13:15;2017-07-04T15:15
    1;EE;HHH;KKK;2017-08-04T13:15;2017-08-04T15:15
    1;FF;KKK;LLL;2017-09-04T13:15;2017-09-04T15:15
    1;GG;LLL;GGG;2017-10-04T13:15;2017-10-04T15:15
    1;HH;GGG;UUU;2017-11-04T13:15;2017-11-04T15:15
    1;II;UUU;PRG;2017-12-04T13:15;2017-12-04T15:15
    '''
    trip = trips[-1]
    for flight_idx in trip:
        print(  len(trips),
                df.loc[flight_idx]['srccountry'],
                df.loc[flight_idx]['src'],
                df.loc[flight_idx]['dest'],
                df.loc[flight_idx]['deptime'].strftime('%Y-%m-%dT%H:%M'),
                df.loc[flight_idx]['arrtime'].strftime('%Y-%m-%dT%H:%M'),
                sep=';')


def find(df, current_flight, countries_visited, trips, flights_of_trip_ind):
    '''
    Find the next flight of the trip which meets the requirements.

    df - dataframe containing all flights
    current_flight - the last flight
    countries_visited - the list of the visited countries
    trips - the list of trips. Each trip contains indexes of the flights
    flights_of_trip_ind - the list of indexes of flights (current trip)
    '''
    countries_visited.append(current_flight['destcountry'])
    flights_of_trip_ind.append(current_flight.name)

    if DEBUG:
        print('>>>', len(trips), flights_of_trip_ind)

    # Find next flight
    if len(flights_of_trip_ind) < FLIGHTS_PER_TRIP-1:
        potentional_dests = df[ (current_flight['dest'] == df['src']) &
                                (current_flight['arrtime'] < df['deptime']) &
                                (~df['destcountry'].isin(countries_visited)) &
                                ( ( pd.to_datetime(df['arrtime']) - pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']) ) < pd.to_timedelta('365 days') )
                                ]
        if len(potentional_dests) > 0:
            for index, flight in potentional_dests.iterrows():
                # Call the recursive find function
                if find(df, flight, countries_visited, trips,
                        flights_of_trip_ind) == 0:
                    return 0
            countries_visited.pop()
            flights_of_trip_ind.pop()
            return 1
        else:
            countries_visited.pop()
            flights_of_trip_ind.pop()
            return -1

    # Find the last flight to the initial destination
    elif len(flights_of_trip_ind) == FLIGHTS_PER_TRIP-1:
        potentional_dests = df[ (current_flight['dest'] == df['src']) &
                                (current_flight['arrtime'] < df['deptime']) &
                                (df['dest'] == df.loc[flights_of_trip_ind[0]]['src']) &
                                ( ( pd.to_datetime(df['arrtime']) - pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']) ) < pd.to_timedelta('365 days') )
                                ]
        if len(potentional_dests) > 0:
            for index, flight in potentional_dests.iterrows():
                # Call the recursive find function
                if find(df, flight, countries_visited, trips,
                        flights_of_trip_ind) == 0:
                    return 0
            countries_visited.pop()
            flights_of_trip_ind.pop()
            return 1
        else:
            countries_visited.pop()
            flights_of_trip_ind.pop()
            return -1

    # Trip found! Save it and pop the last flight
    elif len(flights_of_trip_ind) == FLIGHTS_PER_TRIP:
        trips.append(flights_of_trip_ind[:])
        print_trip(df, trips)
        if len(trips) == NUMBER_OF_TRIPS:
            return 0
        countries_visited.pop()
        flights_of_trip_ind.pop()


def main(in_path):
    '''
    The main function of the script.
    '''
    # Create airport: country dict
    iata_country = create_airport_dict()

    # Create input data dataframe
    df = pd.read_csv(in_path, sep=';',
                    names=['src', 'dest', 'deptime', 'arrtime'],
                    skiprows=1, parse_dates=[2, 3])

    # Add source and destination country columns to the dataframe
    df['srccountry'] = df.apply(lambda x:
                                iata_country.get(x['src'], 'unknown'), axis=1)
    df['destcountry'] = df.apply(lambda x:
                                iata_country.get(x['dest'], 'unknown'), axis=1)

    # Delete domestic flights
    df = df[df['srccountry'] != df['destcountry']]

    # Sort by time
    df.sort_values(by='deptime', ascending=True, inplace=True)

    if DEBUG:
        starttime = time.time()

    trips = []
    countries_visited = []
    flights_of_trip_ind = []
    # Call find function
    for index, flight in df.iterrows():
        countries_visited.clear()
        countries_visited.append(flight.srccountry)
        if find(df, flight, countries_visited, trips, flights_of_trip_ind) == 0:
            break

    if DEBUG:
        stoptime = time.time()
        print('>>>', 'Search finished in', stoptime - starttime)
        print('>>>', len(trips), 'trips found')


if __name__ == '__main__':
    main(sys.argv[1])
