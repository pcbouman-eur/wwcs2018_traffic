import csv

def read_data(filename):
   with open(filename, encoding='utf-8') as in_file:
      reader = csv.DictReader(in_file)
      return [row for row in reader]


def make_hist(data, ignore=[]):
   result = {}
   for row in data:
      for k,v in row.items():
         if not k in ignore and v != '':
            if k in result:
               result[k] += 1
            else:
               result[k] = 1
   return result


def print_sorted(histogram,total):
   for k,v in sorted(histogram.items(), key=lambda x:-x[1]):
      print('{} {:.2f}%'.format(k, v/total*100))


ignore_cols = ['ID','Date','Longitude','Latitude','Damage','Cars','Comment']
data = read_data('serbia-osm-poi-selected-categories.csv')
print_sorted(make_hist(data,ignore=ignore_cols), len(data))
