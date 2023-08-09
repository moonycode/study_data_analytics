# mysql connect package
# pip --> conda
import pymysql


# connect Mysql
# ip, port, username, password, database name
ip = 'localhost' # 127.0.0.1 or remote ip
port = '3306'
username = 'yojulab'
password = '!yojulab*'
database = 'db_cars'

# editor - statement
connect = pymysql.connect(host=ip, user=username, password=password, database=database)

# make select query
query_select = "select * from car_infors;"

# execute select query
# return result set , display
import pandas
df = pandas.read_sql(sql = query_select, con = connect)

# close
connect.close()

pass