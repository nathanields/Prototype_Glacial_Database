headerList = ['aaaa','bbbb','cccc','dddd']
headerString = ', '.join('%s' * len(headerList))
print(headerString)
headerString = "'" + headerString + "'"
print(headerString)
queryString = 'INSERT INTO table VALUES (%s);' %headerString 

final = queryString,headerList
print(final)