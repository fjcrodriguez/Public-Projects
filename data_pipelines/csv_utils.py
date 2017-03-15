import sys

def getdata():
    """
    read in data file from command-line or from standard input

    :return data: stripped string
    """
    # - Main If
    # read from stdin if there is no other argument passed through command-line
    # else, read from csv file given through command-line
    if len(sys.argv)==1:
        data = sys.stdin.read()
    else:
        f = open(sys.argv[1], 'r')
        data = f.read()
        f.close()
    return data.strip()


def read_csv(data):
    """
    process data that is concatenated in a string

    :param data: str
    :return headers: list of header names
    :return data: list of lists where each list represents a row
    """
    # - Separate into lines
    lines = data.split('\n')
    new_data = [row.split(',') for row in lines]

    return new_data[0], new_data[1:]

def create_csv(headers, data, file_name=None, stdout=True):
    """
    re-create a csv file

    :param headers: list of header names
    :param data: list of lists where each list represents a row
    :param file_name: str
    :param stdout: bool (prints to console if true)
    """
    # - Join data
    # join all the data together in a string
    data_str = ','.join(headers) + '\n'
    for row in data:
        data_str += ','.join(row) + '\n'

    # - Main If
    # if user specifies to return to stdout the print the data string
    # otherwise create a file with the specified file name
    if return2_stdout:
        print data_str
    else:
        # try to write to a file
        # raise type error if user forgets to specifiy file name
        try:
            with open(file_name, 'w') as f:
                f.write(data_str)
        except:
            print "TypeError: filename not specified"
