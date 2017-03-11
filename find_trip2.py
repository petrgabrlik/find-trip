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
import time

FLIGHTS_PER_TRIP = 5
NUMBER_OF_TRIPS = 100

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


def print_trip(df, trips):
    '''
    Print the trip in the desired format.

    df - dataframe containing all flights
    trips - list of the trips containing indexes of flithts

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
    TODO
    '''
    # print('--->')
    # if current_flight['srccountry'] == current_flight['destcountry']:
    #     # print('<--- -1 src=dest')
    #     return -1
    countries_visited.append(current_flight['destcountry'])
    # flights_of_trip_df = flights_of_trip_df.append(current_flight)
    # flights_of_trip_df.loc[len(flights_of_trip_df)] = current_flight
    flights_of_trip_ind.append(current_flight.name)
    # print(len(trips), flights_of_trip_ind)
    # print('visited: ', len(countries_visited), countries_visited)
    # print(countries_visited)

    # Find next flight which meets requirements
    if len(flights_of_trip_ind) < FLIGHTS_PER_TRIP-1:
        potentional_dests = df[ (current_flight['dest'] == df['src']) &
                                (current_flight['arrtime'] < df['deptime']) &
                                (~df['destcountry'].isin(countries_visited)) &
                                ( ( pd.to_datetime(df['arrtime']) - pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']) ) < pd.to_timedelta('365 days') ) &
                                (True)
                                ]#.sort_values(by='deptime')
        # print('{:} potentional destinations'.format(len(potentional_dests)))
        # if len(potentional_dests) > 0: print(potentional_dests)
        if len(potentional_dests) > 0:
            for index, flight in potentional_dests.iterrows():
                # print('flight index {:}, {:} ({:}) -> {:} ({:})'.format(index, flight['src'], flight['srccountry'], flight['dest'], flight['destcountry']))
                # print(len(countries_visited))
                # Call the recursive find function
                # find(df, flight, countries_visited, trips, flights_of_trip_ind)
                if find(df, flight, countries_visited, trips, flights_of_trip_ind) == 0:
                    # print('return 0 - 0')
                    return 0
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

    # Find the last flight to the initial destination
    elif len(flights_of_trip_ind) == FLIGHTS_PER_TRIP-1:
        potentional_dests = df[ (current_flight['dest'] == df['src']) &
                                (current_flight['arrtime'] < df['deptime']) &
                                (df['dest'] == df.loc[flights_of_trip_ind[0]]['src']) &
                                ( ( pd.to_datetime(df['arrtime']) - pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']) ) < pd.to_timedelta('365 days') ) &
                                (True)
                                ]#.sort_values(by='deptime')
        if len(potentional_dests) > 0:
            for index, flight in potentional_dests.iterrows():
                # Call the recursive find function
                if find(df, flight, countries_visited, trips, flights_of_trip_ind) == 0:
                    # print('return 0 - 1')
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
        # nalezeno pozadovanych 10 letu, uloz to jako trip a odstran posledni, at muze pokracovat ve hledani od minuleho letu
        # trips.append(countries_visited[:])
        trips.append(flights_of_trip_ind[:])
        # print(len(trips), trips[-1])
        print_trip(df, trips)
        # print('<--- 2 nalezeno 10', countries_visited)
        if len(trips) == NUMBER_OF_TRIPS:
            # print('return 0 - 2')
            return 0
        countries_visited.pop()
        flights_of_trip_ind.pop()
    # print(len(trips))

def main(in_path):
    '''
    The main function of the script.
    '''
    # Create airport: country dict
    iata_country = create_airport_dict()

    # Create input data dataframe
    df = pd.read_csv(in_path, sep=';', names=['src', 'dest', 'deptime', 'arrtime'], skiprows=1, parse_dates=[2, 3])
    # Add country columns to the dataframe
    df['srccountry'] = df.apply(lambda x: iata_country.get(x['src'], 'unknown'), axis=1)
    df['destcountry'] = df.apply(lambda x: iata_country.get(x['dest'], 'unknown'), axis=1)

    # Delete domestic flights
    df = df[df['srccountry'] != df['destcountry']]

    # print(len(df))
    # Sort by time
    df.sort_values(by='deptime', ascending=True, inplace=True)

    # print(df.iloc[0]['deptime'].strftime('%d%m%Y'))

    # print(df[df['src']==df['dest']]) # NEFUNGUJE
    # print(df)

    # print(df[(df['srccountry']=='CZ') & (df['destcountry']=='SK')].sort_values(by='deptime'))

    # stop = df.iloc[0]
    # print(stop)
    # print(df[ (df['src'] == df.iloc[0]['dest']) & (df['deptime'] > df.iloc[0]['arrtime']) ].sort_values(by='deptime')[:5])
    # print(df[ (df['src'] == stop['dest']) & (df['deptime'] > stop['arrtime']) ].sort_values(by='deptime').iloc[0])

    # Hledani destinaci z daneho mista, serazeno
    # print(df[df['src']=='KBP'].sort_values(by='deptime'))

    # print(df[:10])

    starttime = time.time()
    # print('Started at', starttime)

    trips = []
    countries_visited = []
    # flights_of_trip_df = pd.DataFrame()
    flights_of_trip_ind = []
    flight = df.iloc[0]

    # print(flight)
    # print(len(df))
    # df = df[ (df['src'] == flight['dest'])].copy()
    # print(df)
    # print(len(df))

    # print(flight.name)
    # flights_of_trip_ind.append(flight.name)
    # print(pd.to_datetime(df.loc[flights_of_trip_ind[0]]['deptime']))

    countries_visited.clear()
    countries_visited.append(flight.srccountry)
    # status = find(df, flight, countries_visited, trips, flights_of_trip_ind)
    # print(status)
    # if status == -1:
    #     print('Nothing found')
    # elif status == 0:
    #     print('Finished')

    # cyklicka inicializace
    for index, flight in df.iterrows():
        countries_visited.clear()
        countries_visited.append(flight.srccountry)
        if find(df, flight, countries_visited, trips, flights_of_trip_ind) == 0:
            break


    stoptime = time.time()
    print('Search finished in ', stoptime - starttime)

    # for trip in trips:
    #     print(trip)
    # print(trips)

    print(len(trips), 'nalezenych tripu')
        # print('Posledni je:')
        # for i in range(len(trips[-1])):
        #     print(df.loc[trips[-1][i]])

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
    ''' TODO osetrit a doplnit argumenty'''
    main(sys.argv[1])
