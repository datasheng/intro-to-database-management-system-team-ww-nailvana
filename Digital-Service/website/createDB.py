import os 
import pandas as pd
import mysql.connector
import pymysql
import datetime 


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


def check_availability(args):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="databases336",
        port = 3306, 
        database = "catcare"
    )
    results = []
    #formatted_results = []
    mycursor = mydb.cursor()
    mycursor.callproc("check_availability", args)
    for result in mycursor.stored_results():
        #print(result.fetchall())
        results.append(result.fetchall())
    # for result in results: 
    #     for i in result:
    #         formatted_results.append(i) 
    #         # for x in i:
    #         #     formatted_results += (f'{x} ')
    #         # formatted_results += "\n"
    # #myresult = mycursor.fetchall()
    mydb.close()  # Close the database connection
    #print (formatted_results)
    return results


def check_provider(args):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="databases336",
        port = 3306, 
        database = "catcare"
    )
    results = []
    #formatted_results = []
    mycursor = mydb.cursor()
    mycursor.callproc("check_provider", args)
    for result in mycursor.stored_results():
        #print(result.fetchall())
        results.append(result.fetchall())
    # for result in results: 
    #     for i in result:
    #         formatted_results.append(i) 
    #         # for x in i:
    #         #     formatted_results += (f'{x} ')
    #         # formatted_results += "\n"
    # #myresult = mycursor.fetchall()
    mydb.close()  # Close the database connection
    #print (formatted_results)
    return results


# # args = ('2024-05-01 13:00:00', '2024-05-01 16:30:00')
# # check_availability(args)

# args = ['2024-05-01T15:00', '2024-05-01T16:30']
# check_availability(args)