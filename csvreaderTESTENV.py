
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

def csv_HeaderReader(f1,conn): #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, all previous rows stored to
                  #memory are concatenated and become the header (completeHeader). 
    import csv
    import psycopg2
    cur = conn.cursor()
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
                dataRow = headerList
                formatedHeader = header_format(dataRow,completeHeader)
                #print(formatedHeader)
                formatedHeader = """CREATE TABLE waws (%s)""" %formatedHeader
                #formatedHeader = """CREATE TABLE waws (RN_float,_Name_text,_Install_date,_Pole_material_text,_Pole_Length__m__float,_Hole_Depth__mbis__float,_Init__Height_of_pole_above_ice_surface__m__float,_Surface_Type_text,_Snow_depth_1__m__float,_Snow_depth_2__m__float,_Snow_depth_3__m__float,_Removal_Date_date,_Final_height_of_pole_above_ice_surface__m__float,_Final_Surface_type_text,_Snow_Melt__m__float,_Ice_Melt__m__float,_Notes_text)"""
                #print(formatedHeader)
                cur.execute(formatedHeader)
                conn.commit()
                return i
                
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
    f1="/home/ndsouza/Prototype_Glacial_Database/datafiles/Poles_2017/Poles_2017.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE) #open file
        rowCount = row_counter(f1)
        headerList = (next(csvreader)) #start iterator, calling header list calls next row
        i = 0
        print('haha')
        s = csv_HeaderReader(f1,conn)
        while i < s:
            headerList = (next(csvreader))
            i = i+1
            print('wow')
        while i != rowCount:
            #insert into sql table
            print(i)
            #print('INSERT INTO awstest VALUES %r' % (tuple(headerList),))
            #headerList = ', '.join(headerList)
            cur.execute(
                'INSERT INTO waws VALUES %r' % (tuple(headerList),)
            )
            conn.commit()
            headerList = (next(csvreader))
            i = i+1



csv_reader()