import sqlite3

## connect to sqlite

connection = sqlite3.connect("student.db")

## Create a cursor object to insert record, create table,retrieve

cursor = connection.cursor()

## create table

table_info = """
  Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

#insert some more records
cursor.execute("""
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES
('Alice', '10', 'A', 85),
('Bob', '10', 'B', 90),
('Charlie', '9', 'A', 78),
('David', '11', 'C', 92),
('Eva', '12', 'B', 88)
""")

print("The inserted records are")

data = cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

## close the connection
connection.commit()
connection.close()