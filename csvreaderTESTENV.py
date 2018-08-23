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

def header_check(header,headerFull,i): #header_check builds the headers into a single list 
    s = 0
    while s < len(header):
        if i > 0:
            headerFull[s] = headerFull[s] + '_' + header[s]
            s = s+1
        else:
            s = s+1
    return headerFull

def header_format(dataIndiv,completeHeader): #header_format builds the headers into a list to be parseble into the sql server, dataIndiv is the list of values one below the header which is used to set the type
    from dateutil.parser import parse
    s = 0
    dataType = 'varchar(80)'
    while s < len(dataIndiv):
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
                    dataType = 'varchar(80)'
                    completeHeader[s] = completeHeader[s] + " " + dataType + ","
                    s = s+1
    
    return completeHeader
        

def csv_HeaderReader(): #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, all previous rows stored to
                  #memory are concatenated and become the header (completeHeader). 
    import csv
    import psycopg2
    conn = psycopg2.connect("host=localhost dbname=testDB user=ndsouza password=glacier1")
    cur = conn.cursor()
    #f1="/media/sf_ndsouza/testDATA/Julysept20145MIN1.csv"
    #f1="/media/sf_ndsouza/testDATA/July_Sept_2014_Health.csv"
    f1="/home/ndsouza/Prototype_Glacial_Database/datafiles/July_Sept_2014_HalfHour.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        headerList = (next(csvreader)) #start iterator//calling header list calls next row
        headerFull = headerList #Stores first row
        headerVal = headerList[0] #stores first dataIndiv[s] = dataIndiv[s] + " " + dataType + ","value in called row
        i = 0
        while i < 10:  #amount of rows to check, change this number to check more or less rows
            if num_check(headerVal) == False: #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                              #iterates to the next row and preps the first value for checking
                header = headerList
                completeHeader = header_check(header,headerFull,i)
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
                dataRow = headerList
                formatedHeader = header_format(dataRow,completeHeader)
                heado = (''.join(formatedHeader))
                heado = heado[:-1]
                head = """CREATE TABLE awstest(%s)""" % heado
                print(head)
                cur.execute(head)
                conn.commit()
                break

def row_counter(f1):
    import csv
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        rowCount = sum(1 for row in csvreader) #counts amount of rows in table for max value of insertion iterator
        return rowCount


def csv_reader():
    import psycopg2
    conn = psycopg2.connect("host=localhost dbname=testDB user=ndsouza password=glacier1")
    cur = conn.cursor()
    import csv
    #f1="/home/ndsouza/Prototype_Glacial_Database/datafiles/Julysept20145MIN1.csv"
    f1='/home/ndsouza/Prototype_Glacial_Database/datafiles/July_Sept_2014_FiveMin.csv'
    #completeHeader = csv_HeaderReader()
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        rowCount = row_counter(f1)
        #cur.execute("""
        #CREATE TABLE tablenamevariable(
        #    
        #)
        #""")
        headerList = (next(csvreader)) #start iterator, calling header list calls next row
        #headerFull = headerList #Stores first row
        #headerVal = headerList[0] #stores first value in called row
        i = 0
        print(rowCount)        

        while i != rowCount:
            #print(headerList) #insert into sql table
            print(i)
            cur.execute(
                'INSERT INTO awstest VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                headerList
            )
            conn.commit()
            headerList = (next(csvreader))
            i = i+1



csv_HeaderReader()