import csv_utils
import json

def parse_json(json_data):
    """
    given json data object, parse the data into a list of headers and a list
    of lists the represent each row in the data
    """
    headers = data['headers']
    dict_data = data['data']

    data = map(lambda row_data: [row_data[header] for header in headers], dict_data)

    return headers, data

if __name__=="__main__":
    json_data = json.loads(csv.getdata())
    headers, data = parse_json(json_data)
    csv.create_csv(headers, data)
