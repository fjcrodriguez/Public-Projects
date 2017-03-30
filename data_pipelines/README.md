# Data Pipelines

Although there are many packages in python that allow you to read and write
to many data formats, it is also important to know how to those packages
manipulate data. For my own edification, I have implemented scripts the
following scripts that parse data in a given format and converts the data
to the desired format:

| Beginnging Format | End Format |
| :------------- | :------------- |
| csv     | html       |
| csv     | json       |
| csv     | xml       |
| xml     | csv       |
| json    | csv          |

These scripts are used only through the terminal and have the option of printing
the data to the console, which can then be directed to a .csv, .json, .html,
or .xml file. The other option after reading a data file is writing directly
to a file with a given filename.  
