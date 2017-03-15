import csv
import untangle
import re

def parse_xml(xml):
    """
    given xml object, parse it into a header row (list of strings) and a list
    of lists (rows of data)
    """
    data = []
    headers = xml.file.headers.cdata.split(',')

    for i in range(len(headers)):
        headers[i] = re.sub('_',' ', headers[i])

    for i in range(len(xml.file.data.record)):
        row = [ child.cdata for child in xml.file.data.record[i].children]
        data.append(row)

    return headers, data


if __name__=="__main__":
    xml = untangle.parse(csv.getdata())
    headers, data = parse_xml(xml)
    csv.create_csv(headers, data)
