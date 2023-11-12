import pandas as pd
import os


def step_dictionary(df):
    station_dict = {}
    zone_dict = {}

    # get data row by row
    for index, row in df.iterrows():
    
        start_station = row[0]
        end_station = row[1]
        act_cost = int(row[3])

        zone1 = row[4]
        zone2 = row[5]

        # station dictionary of child station tuples (child_name, cost from parent to the child)
        # {"Mile End": [("Stepney Green", 2), ("Wembley", 1)]}
        
        # Add entry for start_station if not present
        if start_station not in station_dict:
            station_dict[start_station] = []
        
        # Add entry for end_station if not present
        if end_station not in station_dict:
            station_dict[end_station] = []

        station_dict[start_station].append((end_station, act_cost))
        station_dict[end_station].append((start_station, act_cost))  # add the other direction of the tube "step"

        # add the main zone
        if start_station not in zone_dict:
            zone_dict[start_station] = set()
        zone_dict[start_station].add(zone1)

        # add the secondary zone
        if end_station not in zone_dict:
            zone_dict[end_station] = set()

        if zone2 != "0":
            zone_dict[start_station].add(zone2)
            # if the secondary zone is not 0 it's the main zone for the ending station
            zone_dict[end_station].add(zone2)
        else:
            # otherwise the main zone for the ending station is the same as for the starting station
            zone_dict[end_station].add(zone1)

    return station_dict, zone_dict


def main():
    df = pd.read_csv('tubedata.csv', 
                    names=['start','end','tube_line','average_time','zone1','zone2'],
                    header=None)

    # Create lookup dictionary with integer indices
    station_names = df['start'].unique()
    inv_station_dict = {}
    for i, station in enumerate(station_names):
        inv_station_dict[station] = i

    
    station_dict, zone_dict = step_dictionary(df)
    
    # Use lookup dictionary to create adjacency matrix
    n = len(station_names)  
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for station in station_dict:
        for child, cost in station_dict[station]:
            adj_matrix[inv_station_dict[station]][inv_station_dict[child]] = cost