import pyodbc
from email_trigger2 import mailTrigger
from datetime import datetime
from config2 import server,database,username,password,main_table,schema_of_table,archival_column

history_table=main_table+"_HISTORY"
print(history_table)

try:
    print(archival_column)
    conn_str=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn=pyodbc.connect(conn_str)
    print("COnnection success")

    cursor = conn.cursor()
    print("cursor created")
    cursor.execute(f'''if not exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME='{history_table}')
        begin 
        select * into {schema_of_table}.{history_table} FROM {schema_of_table}.{main_table} WHERE 1=0;
        end''')
    cursor.execute(f'''select count(*) from {schema_of_table}.{history_table};''')
    res=cursor.fetchall()
    q0_i=(res[0][0])
    print('initial count in history table',q0_i)
#check count of records to be pushed into archival table from main_table
    cursor.execute(f'''SELECT count (*) FROM {schema_of_table}.{main_table}
        WHERE {archival_column} < DATEADD(month, -2,  cast(getdate() as date));;''')
    res=cursor.fetchall()
    q1=(res[0][0])
    if q1==0:
        raise ValueError("No records to be pushed from main table")
    print('records to be pushed from main table:',q1)

#q1 execute (push old records into history table )
    cursor.execute(f'''INSERT INTO {schema_of_table}.{history_table} 
        SELECT * FROM {schema_of_table}.{main_table}
        WHERE {archival_column} < DATEADD(month, -2,  cast(getdate() as date));;''')

#validate counts before deleting records from main table
    cursor.execute(f'''select count(*) from {schema_of_table}.{history_table};''')
    res=cursor.fetchall()
    q0_f=(res[0][0])
    if ((q0_i+q1)==q0_f):
        print(q0_i, '+',q1,'=',q0_f,"records count validation-SUCCESS")
        cursor.execute(f'''delete from  {schema_of_table}.{main_table}
            where  {archival_column} < DATEADD(month, -2,  cast(getdate() as date));''') 
        errResponse='Success'
        current_timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mailTrigger(errResponse,errMsg=f"ARCHIVAL SUCCESSFUL until timestamp {current_timestamp}")   
        conn.commit()
        print("archival complete... commiting executed changes")
except ValueError as ve:
    print(ve)
    errResponse='NOT REQ'
    mailTrigger(errResponse,errMsg=f"{ve} -Data Archival not required for table {schema_of_table}.{main_table}")

except Exception as e:
        print(e)
        errResponse='Failed'
        mailTrigger(errResponse,errMsg=f"Data Archival failed for table {schema_of_table}.{main_table}")

finally:
    conn.close()
    print("connection closed")
    print(res[0][0])