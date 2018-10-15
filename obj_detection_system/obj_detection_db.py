"""
Contains the database functions for the object detection system. The
user's parameters should be changed in the configuration file (database.ini).
Creates a table of objects and bounding box coordinates correlating to images.
Also creates views of the top ten scored instances of each object detected. 
"""
import psycopg2
from config import config
import csv


def create_database():
    """Creates our object detection database if necessary"""
    db_drop = (
        """
        DROP DATABASE IF EXISTS obj_detection;
        """)
    db_create = (
        """
        CREATE DATABASE obj_detection;
        """)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(db_drop)
        cur.execute(db_create)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_table():
    """Creates the table of objects and bounding boxes for each image; 
        creates a new table for every directory.
    """
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
            PRIMARY KEY (img_id, box_x, box_y, label, score)
            );
        """)
    table_drop = (
        """
        DROP TABLE IF EXISTS objects;
        """
    )
    
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(database="obj_detection", user="postgres", password="postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(table_drop)
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_objects_from_list(vals_list):
    """Inserts into the table, drawing from a list as its input"""
    command = "INSERT INTO objects VALUES(%s,%s,%s,%s,%s,%s,%s);"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(database="obj_detection", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.executemany(command,vals_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_object_table_from_list(vals_list):
    """Synthesizes table creation and value insertion"""
    create_database()
    create_table()
    insert_objects_from_list(vals_list)


def create_topten_view(cur, label):
    """Creates a view of the top-ten scored instances of the
        object specified in the label argument
    """
    viewname = label.replace(" ", "_")+"_topten"
    command = (
        """
        CREATE OR REPLACE VIEW """ + viewname + """
        AS SELECT * FROM objects
        WHERE label = \'"""+label+"""\'
        ORDER BY score DESC;
    """)
    cur.execute(command)


def create_topten_views():
    """Creates top-ten views for all object labels"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(database="obj_detection", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute("SELECT label FROM objects;")
        labels = cur.fetchall()
        labels = [label[0] for label in labels]
        for label in labels:
            create_topten_view(cur, label)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


