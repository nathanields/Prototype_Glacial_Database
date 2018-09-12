import psycopg2

conn = psycopg2.connect("host=localhost dbname=testDB user=ndsouza password=glacier1")
cur = conn.cursor()

headerList = ['aa/aa','bb(bb','cc)cc','d.ddd']
headerString = "%s," * len(headerList)

headerString = headerString[:-1]

#print(headerString)
#headerString = "'" + headerString + "'"

final = 'INSERT INTO values VALUES (%s);' %headerString 

print(final)
print(final, headerList)

cur.execute(final, headerList)
conn.commit
print('complete')