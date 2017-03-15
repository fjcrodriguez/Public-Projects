import csv

def build_html(headers, data):
    """
    method for building an html file given headers and data

    :param headers: list of strings
    :param data: list of lists 
    """
    # - top level tags
    # start the html string by adding the beginning
    # of html document with a table
    html = '<html>\n<body>\n<table>\n'

    # - Build header row
    # build header row then add it to the html string
    header_row = ''
    for column in headers:
        header_row += '<th>%s</th>' % column

    html += '<tr>%s</tr>\n' % header_row

    # - Build data
    # build each row then add to the html code
    for row in data:
        data_row = ''
        for element in row:
            data_row += '<td>%s</td>' % element
        html += '<tr>%s</tr>\n' % data_row

    html += '\n</table>\n</body>\n</html>'

if __main__=="__name__":
    headers, data = csv.read_csv(csv.getdata())
    html_data = build_html(headers, data)
    print html_data
