

import csv
import json

def csv_to_jsonl(csv_file, jsonl_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract headers
        data = [{"input_text": row[0], "output_text": row[1]} for row in reader]

    with open(jsonl_file, 'w') as outfile:
        for item in data:
            json.dump(item, outfile)
            outfile.write('\n')

# Replace 'input.csv' and 'output.jsonl' with your file names
csv_to_jsonl('ishaan_s23.csv', 'output_s23.jsonl')