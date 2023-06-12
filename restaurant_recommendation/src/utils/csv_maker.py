#Transforming list of json objects into csv 
import csv
import json

import pandas as pd


def csv_maker(input_file, restaurant_data):

# Define the headers for the CSV file
    headers = set()
    for j in input_file:
        headers.update(j.keys())

# Open a new CSV file for writing
    with open(restaurant_data, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for j in input_file:
            writer.writerow(j)
