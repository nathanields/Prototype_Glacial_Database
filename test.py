import psycopg2
import math
x=float('nan')
math.isnan(x)

conn = psycopg2.connect("host=localhost dbname=testDB user=ndsouza password=glacier1")
cur = conn.cursor()

headerList = ['aa/aa','bb(bb','cc)cc','d.ddd']
headerString = "%s," * len(headerList)

headerString = headerString[:-1]

print(headerString)
#headerString = "'" + headerString + "'"

final = 'INSERT INTO wow VALUES (%s)' %headerString 

print(final)
print(final, headerList)
wow = final, headerList
print(wow)

cur.execute(final, headerList)
conn.commit
print('complete')