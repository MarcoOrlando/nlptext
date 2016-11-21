import json
import csv

with open('dataahok.json') as json_data:
    data = json.load(json_data)
   
    with open("dataahok.csv", "w") as file:
	    csv_file = csv.writer(file)
	    csv_file.writerow(['created_at','text']);
	    item['text'] = unicode(item['text'], 'utf-8', errors='ignore')
	    for item in data:
	        csv_file.writerow([item['created_at'] + ',' + item['text']])