def num_check(s): #num_check trys the value 's' to see if it's a float (number) or a date. If it is, it returns True, if not, returns false
    from dateutil.parser import parse
    try:
        float(s)
        return True
    except ValueError:
        try:
            parse(s)
            return True
        except ValueError:
            return False

def header_check(header,headerFull,i): #header_check builds the headers into a single list to be parsed into the sql server,
    s = 0
    while s < len(header):
        if i > 0:
            headerFull[s] = headerFull[s] + '/' + header[s]
            s = s+1
        else:
            s = s+1
    return headerFull

def csv_HeaderReader(): #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, all previous rows stored to
                  #memory are concatenated and become the header (complete_header). 
    import csv
    #f1="/media/sf_ndsouza/testDATA/Julysept20145MIN1.csv"
    #f1="/media/sf_ndsouza/testDATA/July_Sept_2014_Health.csv"
    f1="/home/ndsouza/Prototype_Glacial_Database/datafiles/Julysept20145MIN1.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        headerList = (next(csvreader)) #start iterator//calling header list calls next row
        headerFull = headerList #Stores first row
        headerVal = headerList[0] #stores first value in called row
        i = 0
        while i < 10:  #amount of rows to check, change this number to check more or less rows
            if num_check(headerVal) == False: #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                              #iterates to the next row and preps the first value for checking
                header = headerList
                complete_header = header_check(header,headerFull,i)
                headerList = (next(csvreader))
                headerVal = headerList[0]
                i = i+1
                ##print('help! Im stuck in a while loop and cant get out!')
            elif num_check(headerVal) == True: #if num_check returns true, this is where the database header building function will be called and implemented. 
                                               #Once it is complete, the loop breaks and the function ends. This should actually ideally concatenate multiple
                                               #rows since it seems a lot of these files use more than one row as a header, with units and other info included
                #print(header)
                #print(i)
                #print("oh god finally, Im free from these mortal coils")
                print(complete_header)
                return (complete_header)
                #headerFull = header_check(i,f1) #-header check is the function which will find all rows of headers and concatenate them into a single list (headerFull)              


def row_counter(f1):
    import csv
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        rowCount = sum(1 for row in csvreader) #counts amount of rows in table for max value of insertion iterator
        return rowCount



def csv_reader():
    #import psycopg2
    #from config import config
    import csv
    f1="/home/ndsouza/Prototype_Glacial_Database/datafiles/Julysept20145MIN1.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        rowCount = row_counter(f1)
        

        headerList = (next(csvreader)) #start iterator, calling header list calls next row
        #headerFull = headerList #Stores first row
        #headerVal = headerList[0] #stores first value in called row
        i = 0
        print(rowCount)        

        while i < rowCount:
            print(headerList)
            headerList = (next(csvreader))
            i = i+1




csv_reader()
#csv_HeaderReader()