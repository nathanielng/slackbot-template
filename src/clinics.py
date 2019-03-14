import argparse
import geocoder
import numpy as np
import os
import pandas as pd
import time


def geocode(df, address_col, zone_col='ZONE'):
    # for row in df[column_name].iteritems():
    for row in df.iterrows():
        # idx, address = row
        idx, data = row
        address = data[address_col]
        if not np.isnan(data['Lat']):
            continue

        if data[zone_col] == 'JOHOR BAHRU':
            address = f'{address}, Johor Bahru, Malaysia'
        else:
            address = f'{address}, Singapore'
        print(f'{idx}: "{address}"', end='')

        g = geocoder.osm(address)
        try:
            lat, lon = g.latlng
            df.loc[idx, 'Lat'] = lat
            df.loc[idx, 'Lon'] = lon
            print(f'... ({lat}, {lon})')
            if 'features' in g.geojson.keys():
                geo = g.geojson['features']
                if len(geo) > 0:
                    geo = geo[0]
                df.loc[idx, 'geo'] = str(geo)
        except Exception as e:
            print(f'... (FAILED)')
        time.sleep(2)
    return df


def load_data(filename):
    df = pd.read_excel(filename)
    df.drop(labels=[0], axis=0, inplace=True)
    df.drop(labels=[550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560],
            axis=0, inplace=True)
    df.set_index('S/N', inplace=True)
    df['Lat'] = np.nan
    df['Lon'] = np.nan
    df['geo'] = np.nan
    return df


def process(infile, outfile, preprocess=True):
    if preprocess is True:
        df = load_data(infile)
    elif infile.endswith('.xlsx'):
        df = pd.read_excel(infile)
    elif infile.endswith('.csv'):
        df = pd.read_csv(infile)
    else:
        print('Error')
        quit()

    df = geocode(df, 'ADDRESS 1')

    basename, ext = os.path.splitext(outfile) 
    csvfile = f'{basename}.csv'
    xlsxfile = f'{basename}.xlsx'
    df.to_csv(csvfile)
    df.to_excel(xlsxfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('--preprocess', action='store_true')
    args = parser.parse_args()

    process(infile=os.path.abspath(args.infile),
            outfile=os.path.abspath(args.outfile),
            preprocess=args.preprocess)

