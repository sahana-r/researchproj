import psycopg2
from config import config
import csv
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_table():
    command = (
        """
        CREATE TABLE objects (
            img_id VARCHAR(255),
            box_height FLOAT,
            box_width FLOAT,
            box_x FLOAT,
            box_y FLOAT,
            label VARCHAR(255),
            score FLOAT,
            PRIMARY KEY (img_id, box_x, box_y)
            )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_objects_from_csv(csv_filename):
    command = "INSERT INTO objects VALUES(%s,%s,%s,%s,%s,%s,%s)"
    vals_list = []
    with open(csv_filename) as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            #parsed = (row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), row[5], float(row[6]))
            #vals_list.append(parsed)
            vals_list.append(tuple(row))
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(command,vals_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

 
 
if __name__ == '__main__':
    #connect()
    #create_table()
    insert_objects_from_csv('obj_detect.csv')
