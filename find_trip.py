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

def join_df(in_path):
    iata_country = create_airport_dict()
    df = pd.read_csv(in_path, sep=';', names=['src', 'dest', 'deptime', 'arrtime'], skiprows=1, parse_dates=True)
    # print(dff[dff['src']=='PRG'])
    # print(dff[:10])
    # print(dff['src'].values)
    # print(dff[])
    # dfa = pd.read_csv('airports.csv', sep=',')
    # print(dfa[(dfa['iso_country']=='SK') & (dfa['iata_code'].isnull()==False)][['iso_country', 'iata_code']])
    # print(dfa[dfa['iata_code'].isin(['PRG', 'BTS'])]['iso_country'])
    # print(dfa[dfa['iata_code']=='PRG']['iso_country'].item())
    # print( dfa[dfa['iata_code'].isin(dff['src'].values)][['iso_country','iata_code']] )

    # df = dff.copy()
    # print(iata_country[df['src']])
    # print(df['src'])
    # df['c'] = df.apply(lambda x: max(len(x['a']), len(x['b'])), axis=1)
    # df['srccountry'] = df.apply(lambda x: dfa[dfa['iata_code']=='PRG']['iso_country'].item() , axis=1)
    # df['srccountry'] = df.apply(lambda x: x['src'] , axis=1)
    # df['srccountry'] = df.apply(lambda x: 'PRG' , axis=1)
    df['srccountry'] = df.apply(lambda x: iata_country.get(x['src'], 'unknown'), axis=1)
    df['destcountry'] = df.apply(lambda x: iata_country.get(x['dest'], 'unknown'), axis=1)
    print(df[(df['srccountry']=='CZ') & (df['destcountry']=='SK')].sort_values(by='deptime'))

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
    # Create airport: country dict
    iata_country = create_airport_dict()

    # DEBUG Find unknown iata codes in airport dictionary
    # unknown_iata = set()
    # with open(in_path, encoding="utf-8") as fp:
    #     reader = csv.reader(fp, delimiter=';', skipinitialspace=True)
    #     next(reader, None) # skip header
    #     for line in reader:
    #         if len(line) == 4:
    #             try:
    #                 print(line, iata_country[line[0]])
    #             except:
    #                 unknown_iata.add(line[0])
    # print(unknown_iata)

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
    print(df[df['src']=='AHB'].sort_values(by='deptime'))

    r = 651
    countries = []
    while len(countries) < 11:
        countries.clear()
        stop = df.iloc[r].copy()
        # countries.add(stop['srccountry'])
        countries.append(stop['srccountry'])
        print(r)
        for i in range(10):
            countries.append(stop['destcountry'])
            if stop['destcountry'] == stop['srccountry']:
                break
            # print(stop)
            # print(countries)
            # stop = df[ (df['src'] == stop['dest']) & (df['deptime'] > stop['arrtime']) ].sort_values(by='deptime').iloc[0].copy()
            if len(countries) < 10:
                try:
                    stop = df[ (df['src'] == stop['dest']) & (df['deptime'] > stop['arrtime']) & (~df['destcountry'].isin(countries)) ].sort_values(by='deptime').iloc[0].copy()
                    # print(stop)
                    # udelat dataframe z nalezenych letu
                except:
                    # print("\nDalsi destinace nenalezena.")
                    break
            else:
                try:
                    stop = df[ (df['src'] == stop['dest']) & (df['deptime'] > stop['arrtime']) & (df['destcountry'] == countries[0]) ].sort_values(by='deptime').iloc[0].copy()
                    # print(stop)
                except:
                    break
        r += 1
    print(countries)

    # join_df(in_path)

if __name__ == '__main__':
    main(sys.argv[1])
