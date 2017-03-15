import csv

def build_json(headers, data):
    """
    method for building a json data file

    :param headers: list of strings
    :param data: list of lists
    """
    json = '{'
    string_headers = ''
    for column in headers:
        string_headers += '"%s", ' % column

    json += '  "headers":[%s],\n' % string_headers[:-2]
    json += '  "data":[\n'

    for j in range(len(data)):
        json += '    {\n'
        record = '      '
        for i in range(len(headers)):
            record += '"%s":"%s", ' % (headers[i], data[j][i])
        json += record[:-2] + "\n"
        if j == len(data)-1:
            json += '    }\n'
        else:
            json += '    },\n'

    json += '  ]\n'
    json += '}\n'

    return json

if __name__=="__main__":
    headers, data = csv.readcsv(csv.getdata())
    json = build_json(headers, data)
    print json
