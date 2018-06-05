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


def csv_reader(): #csv_reader opens a csv, calls it into memory, and checks the first 10 rows to see if data is there. If it is data, it backs one row up
                  #and stores those as values as headers. 
    import csv
    f1="/media/sf_ndsouza/testDATA/July_Sept_2014_Health.csv"
    with open(f1, 'rt') as dataFILE: #opens file and sets up reader and iterator
        csvreader = csv.reader(dataFILE)
        headerList = (next(csvreader))
        headerVal = headerList[0]
        i = 0
        while i < 10:  #amount of rows to check, change this number to check more or less rows
            if num_check(headerVal) == False: #calls num_check (see above function). If this row is not data, function saves it (incase it is the header), then
                                              #iterates to the next row and preps the first value for checking
                i = i+1
                header = headerList
                headerList = (next(csvreader))
                headerVal = headerList[0]
                ##print('help! Im stuck in a while loop and cant get out!')
            elif num_check(headerVal) == True: #if num_check returns true, this is where the database header building function will be called and implemented. 
                                               #Once it is complete, the loop breaks and the function ends.
                ##print("oh god finally, Im free from these mortal coils")
                print(header)
                break                


csv_reader()

