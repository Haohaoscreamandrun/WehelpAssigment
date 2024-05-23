import mysql.connector
from dotenv import load_dotenv
import os
import time
load_dotenv()
DBpassword = os.getenv('password')

mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= DBpassword,
  database="website"
  )

mycursor = mydb.cursor()

# for i in range(100000, 500000):
#   sql = "INSERT INTO member (name, username, password)\
#           VALUES (%s, %s, %s)"
#   val = (f'name{i}', f'username{i}', f'password{i}')
#   mycursor.execute(sql, val)

# mydb.commit()
# print(mycursor.rowcount, "record inserted.")

timer_start = time.time()

sql = "SELECT username, password\
        FROM member\
        WHERE username = 'test'\
        AND password= 'test'"

mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)
timer_end = time.time()
print('The SQL process took about', (timer_end - timer_start)*1000, 'milliseconds')
