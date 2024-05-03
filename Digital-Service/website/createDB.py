import os 
import pandas as pd
import mysql.connector
import pymysql


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="databases336",
    port = 3306, 
    database = "catcare"
)


my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE catcare")

# my_cursor.execute("SHOW DATABASES")

# for db in my_cursor:
#     print(db)


def execute_sql(sql):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="databases336",
        port = 3306, 
        database = "catcare"
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mydb.close()  # Close the database connection
    return myresult


def sql_provider():
    sql = "SELECT * FROM provider;"
    result = execute_sql(sql)

    df = pd.DataFrame()
    for x in result: 
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])

    df.to_html('./Digital-Service/website/templates/sql-provider-data.html')


def sql_customer():
    sql = "SELECT customerid, name, email FROM customer;"
    result = execute_sql(sql)

    return result

    # df = pd.DataFrame()
    # for x in result: 
    #     df2 = pd.DataFrame(list(x)).T
    #     df = pd.concat([df,df2])

    # df.to_html('./templates/sql-customer-data.html')


def sql_stored_procedure():
    sql = "BEGIN SELECT provider.ProviderID, provider.Name, providerschedule.StartTime, providerschedule.EndTime FROM providerschedule INNER JOIN provider ON providerschedule.ProviderID = provider.ProviderID WHERE providerschedule.StartTime >= int_start AND providerschedule.EndTime <= int_end; END;"
    execute_sql(sql)


