# Script that finds nearby poi's for accidents in a dataset

import csv
# Install geopy. With anaconda, do 'conda install -c conda-forge geopy'
from geopy.distance import distance
from numpy import mean

def read_data(filename, delim=',', enc='utf-8'):
   with open(filename, encoding=enc) as in_file:
      reader = csv.DictReader(in_file, delimiter=delim)
      return [row for row in reader]


def write_data(data, outfile, delim=','):
   header = []
   header_set = set()
   for row in data:
      for key in row.keys():
         if not key in header_set:
            header.append(key)
            header_set.add(key)
   header = [col for col in header]
   with open(outfile, 'w', newline='', encoding='utf-8') as out_file:
      out = csv.DictWriter(out_file, header)
      out.writeheader()
      for row in data:
         out.writerow(row)


def filter_by_distance(accs,pois,max_dist):
   lat_avg = sum([float(d['Latitude']) for d in accs]) / len(accs)
   lon_avg = sum([float(d['Longitude']) for d in accs]) / len(accs)
   loc_avg = (lat_avg, lon_avg)
   res = []
   for poi in pois:
      poi_loc = (poi['Latitude'], poi['Longitude'])
      dst = distance(loc_avg, poi_loc)
      if dst.meters <= max_dist:
         res.append(poi)
   return res



def join_by_distance(accs,pois,max_dist,skip=['ID','Longitude','Latitude']):
   count = 1
   for row in accs:
      print(str(count)+' out of '+str(len(accs)))
      count += 1
      acc_loc = (row['Longitude'], row['Latitude'])
      for poi in pois:
         poi_loc = (poi['Longitude'], row['Latitude'])
         dst = distance(acc_loc, poi_loc)
         if dst.meters <= max_dist:
            for k,v in poi.items():
               if not k in skip and v != '':
                  if k in row:
                     row[k] += int(v)
                  else:
                     row[k] = int(v)
                  

# File definitions
INPUT_FILE_ACCIDENTS = 'accidents.csv'
INPUT_FILE_OSM = 'serbia-osm-poi-selected-categories.csv'
OUTPUT_FILE = 'output.csv'

# Distance use to determine whether a poi counts as being close enough to an accident
MAX_POI_DISTANCE_METERS = 50
# Used to remove pois that are this far from the mean point of the accident data
# If unsure, set this number very high.
FILTER_DISTANCE_METERS = 100000

accidents = read_data(INPUT_FILE_ACCIDENTS, enc='latin')
pois = read_data(INPUT_FILE_OSM)
pois = filter_by_distance(accidents,pois, FILTER_DISTANCE_METERS)
join_by_distance(accidents, pois, MAX_POI_DISTANCE_METERS)
write_data(accidents, OUTPUT_FILE)
