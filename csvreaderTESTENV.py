
def num_check(s):                                    #num_check trys the value 's' to see if it's a float (number) or a date. If it is, it returns True, if not, returns false
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

def header_check(header,headerFull,i):              #header_check builds the headers into a single list 
    s = 0

    while s < len(header):
        if i > 0:
            headerFull[s] = headerFull[s] + '_' + header[s]
            s = s+1

        else:
            s = s+1

    return headerFull

def header_format(dataIndiv,completeHeader):        #header_format builds the headers into a list to be parseble into the sql server, dataIndiv is the list of values one below the header which is used to set the type
    from dateutil.parser import parse

    s = 0
    dataType = 'varchar(80)'

    while s < len(dataIndiv):
        completeHeader[s] = completeHeader[s].replace(" ","_")
        completeHeader[s] = completeHeader[s].replace("(","_")
        completeHeader[s] = completeHeader[s].replace(")","_")
        completeHeader[s] = completeHeader[s].replace(".","_")

        try:
            float(dataIndiv[s])
            dataType = 'float'
            completeHeader[s] = completeHeader[s] + " " + dataType + ","
            s = s+1

        except ValueError:
            try:
                parse(dataIndiv[s])
                dataType = 'date'
                completeHeader[s] = completeHeader[s] + " " + dataType + ","
                s = s+1
            except ValueError:
                try:
                    int(dataIndiv[s])
                    dataType = 'int'
                    completeHeader[s] = completeHeader[s] + " " + dataType + ","
                    s = s+1
                except ValueError:
                    dataType = 'text'
                    completeHeader[s] = completeHeader[s] + " " + dataType + ","
                    s = s+1
    completeHeader = (' '.join(completeHeader))
    completeHeader = completeHeader[:-1]
    return completeHeader

def table_exist(tableName, conn):                   #checks to see if a table exists/returns true or false
    cur = conn.cursor()
    exist = """select exists(select * from information_schema.tables where table_name = '%s')""" %tableName
    print(exist)
    try:
        cur.execute(exist)
        exists = cur.fetchone()[0]
        print('true')
        print(exists)
        return exists
    except ValueError:
        print('false')
        return False


def csv_HeaderReader(f1,conn,tableName):            #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, all previous rows stored to
                                                    #memory are concatenated and become the header (completeHeader). 
    import csv
    ########import psycopg2
    cur = conn.cursor() 
    with open(f1, 'rt') as dataFILE:                #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE)            #open file
        headerList = (next(csvreader))              #start iterator//calling header list calls next row
        headerFull = headerList                     #Stores first row
        headerVal = headerList[0]                   #stores first dataIndiv[s] = dataIndiv[s] + " " + dataType + ","value in called row
        i = 0
        if table_exist(tableName, conn) == True:    #checks for exiting table, if present, counts headers and returns that without making a new table, if no table exists, creates table
            while i < 10:                           #amount of rows to check, change this number to check more or less rows
                if num_check(headerVal) == False:   #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                                    #iterates to the next row and preps the first value for checking
                    header = headerList
                    completeHeader = header_check(header,headerFull,i)
                    headerList = (next(csvreader))
                    headerVal = headerList[0]
                    i = i+1
                elif num_check(headerVal) == True:  #if num_check returns true, this is where the database header building function will be called and implemented. 
                                                    #Once it is complete, the loop breaks and the function ends. This should actually ideally concatenate multiple
                                                    #rows since it seems a lot of these files use more than one row as a header, with units and other info included
                    dataRow = headerList
                    formatedHeader = header_format(dataRow,completeHeader)
                    print('I am not creating a table')
                    return i                        #i is the number of rows the headers occupy
        elif table_exist(tableName, conn) == False: #table creation stream
            while i < 10:                           #amount of rows to check, change this number to check more or less rows
                if num_check(headerVal) == False:   #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                                    #iterates to the next row and preps the first value for checking
                    header = headerList
                    completeHeader = header_check(header,headerFull,i)
                    headerList = (next(csvreader))
                    headerVal = headerList[0]
                    i = i+1
                elif num_check(headerVal) == True:  #if num_check returns true, this is where the database header building function will be called and implemented. 
                                                    #Once it is complete, the loop breaks and the function ends. This should actually ideally concatenate multiple
                                                    #rows since it seems a lot of these files use more than one row as a header, with units and other info included
                    dataRow = headerList
                    formatedHeader = header_format(dataRow,completeHeader)
                    print(formatedHeader)
                    formatedHeader = """CREATE TABLE {} ({})""".format(tableName, formatedHeader)
                    cur.execute(formatedHeader)
                    conn.commit()
                    return i
                
def row_counter(f1):                                #counts total rows in the csv for iteration purpose, returns rowCount
    import csv
    with open(f1, 'rt') as dataFILE:                #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE)
        rowCount = sum(1 for row in csvreader)      #counts amount of rows in table for max value of insertion iterator
        return rowCount



def csv_reader():                                   #heavy lifter, calls other functions for processing, then handles input itself. wraps lines into lists then joins and inputs to the table  
    import psycopg2                                 #uses connection opened here for all writes
    conn = psycopg2.connect("host=localhost dbname=testDB user=ndsouza password=glacier1")
    cur = conn.cursor()
    import csv

    f1 = input('Enter File path:')                  #queries to users
    tableName = input('Enter Table name:')

    with open(f1, 'rt') as dataFILE:                #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE)            #open file
        rowCount = row_counter(f1)
        headerList = (next(csvreader))              #start iterator, calling header list calls the next row
        i = 0
        s = csv_HeaderReader(f1,conn,tableName)
        while i < s:
            headerList = (next(csvreader))
            i = i+1
        while i < rowCount:                         #when all conditions are met, this is where each row is inserted
            print(i)
            headerList = "', '".join(headerList)
            headerList = "'" + headerList + "'"
            cur.execute(                            #wrapping of all rows occurs here
                'INSERT INTO {} VALUES ({})'.format(tableName, headerList)
            )
            conn.commit()                           #final commit locks the string into the database
            headerList = (next(csvreader))
            i = i+1
        print("File loading complete, disconnecting from database")
            



csv_reader()