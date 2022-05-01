from MySQLdb import OperationalError
import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user=env("MYSQL_USER"),
  password=env("MYSQL_PASSWORD"),
  database=env("MYSQL_DATABASE"),
  auth_plugin='mysql_native_password'
)
cursor= connection.cursor()

creation_script_file =  open("DatabaseCreation\\create_tables.sql", "r")
creation_script = creation_script_file.read().split(';')
creation_script_file.close()
for sta in creation_script:
  cursor.execute(sta)

connection.commit()
    

