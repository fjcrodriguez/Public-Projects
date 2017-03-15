from csv_utils import *
import re


def build_xml(headers, data):
    """
    method for building an xml data file given headers, data

    :param headers: list of strings
    :param data: list of lists
    """
    xml = '<?xml version="1.0"?>\n<file>\n'
    xml += '  <headers>%s</headers>\n  <data>\n' % ','.join(headers)

    for row in data:
        xml += '    <record>\n'
        record = ""
        for i in range(len(headers)):
            formatted_header = re.sub(' ', '_', headers[i])
            record += '<%s>%s</%s>' % (formatted_header, row[i], formatted_header)

        xml += '      %s\n' % record
        xml += '    </record>\n'

    xml += '  </data>\n'
    xml += '</file>\n'

    return xml

if __name__=="__main__":
    headers, data = csv.read_csv(getdata())
    xml = build_xml(headers, data)
    print xml
