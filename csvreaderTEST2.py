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


def header_check(header,headerFull):
    s = 0
    print(len(header))
    print(len(headerFull))
    while s < len(header):
        headerFull[s] = headerFull[s] + header[s]
        s = s+1
    return headerFull


def csv_reader(): #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, all previous rows stored to
                  #memory are concatenated and become the header (complete_header). 
    import csv
    #f1="/media/sf_ndsouza/testDATA/Julysept20145MIN1.csv"
    f1="/media/sf_ndsouza/testDATA/July_Sept_2014_Health.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE)
        headerList = (next(csvreader))
        headerFull = headerList
        headerVal = headerList[0]
        i = 0
        while i < 10:  #amount of rows to check, change this number to check more or less rows
            if num_check(headerVal) == False: #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                              #iterates to the next row and preps the first value for checking
                i = i+1
                header = headerList
                complete_header = header_check(header,headerFull)
                headerList = (next(csvreader))
                headerVal = headerList[0]
                ##print('help! Im stuck in a while loop and cant get out!')
            elif num_check(headerVal) == True: #if num_check returns true, this is where the database header building function will be called and implemented. 
                                               #Once it is complete, the loop breaks and the function ends. This should actually ideally concatenate multiple
                                               #rows since it seems a lot of these files use more than one row as a header, with units and other info included
                #print(header)
                #print(i)
                print("oh god finally, Im free from these mortal coils")
                print(headerFull)
                #headerFull = header_check(i,f1) #-header check is the function which will find all rows of headers and concatenate them into a single list (headerFull)
                break                


csv_reader()

