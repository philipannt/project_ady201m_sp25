import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

def connect_cloud():
    load_dotenv()
    
    config = {
        "host": os.getenv("AIVEN_DB_HOST"),
        "port": int(os.getenv("AIVEN_DB_PORT")),
        "user": os.getenv("AIVEN_DB_USER"),
        "password": os.getenv("AIVEN_DB_PASS"),
        "database": os.getenv("AIVEN_DB_NAME"),
        "ssl_ca": os.getenv("AIVEN_DB_CA")
    }

    try:
        conn = mysql.connector.connect(**config)
        return conn
    except:
        print(f"Connection error.")

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS PROJ_ADY")
    except:
        print(f"Create database error.")

def create_table(cursor):
    try:
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tbl_Xemaychotot(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Name_Bike VARCHAR(100),
            Year_Of_Manufacture VARCHAR(4),
            Distance_of_Bike VARCHAR(50),
            Nationality VARCHAR(50),
            Location_bike VARCHAR(200),
            Listing_time VARCHAR(50),
            Price VARCHAR(20),
            Price_min VARCHAR(20),
            Price_max VARCHAR(20)
        );
        '''
        cursor.execute(create_table_query)
    except:
        print("Create table error.")

def insert_data(cursor, df):
    try:
        insert_query = '''
        INSERT INTO tbl_Xemaychotot (
            Name_Bike, 
            Year_Of_Manufacture, 
            Distance_of_Bike, Nationality, 
            Location_bike, 
            Listing_time, 
            Price, 
            Price_min, 
            Price_max
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row['name'], 
                row['Year_of_manufacture'], 
                row['Kilometers_driven'],
                row['Nationality'], 
                row['Location'], 
                row['Listing_time'],
                row['price'], 
                row['price_min'], 
                row['price_max']
            ))
    except:
        print("Insert error")

def main():
    try:
        conn = connect_cloud()
        cursor = conn.cursor()
        create_database(cursor)
        conn.database = "PROJ_ADY"
        create_table(cursor)
        conn.commit()
        print("Done.")
        
        data = {
            "name": ["Honda", "Yamaha"],
            "Year_of_manufacture": ["2018", "2020"],
            "Kilometers_driven": ["15000", "10000"],
            "Nationality": ["Japan", "Japan"],
            "Location": ["Hanoi", "HCMC"],
            "Listing_time": ["2023-01-01", "2023-02-01"],
            "price": ["50000000", "70000000"],
            "price_min": ["48000000", "68000000"],
            "price_max": ["52000000", "72000000"]
        }
        df = pd.DataFrame(data)

        insert_data(cursor, df)
        conn.commit()
        print("Data inserted successfully.")

    except:
        print("Main error.")
    finally:
        cursor.close()
        conn.close()

if __name__=="__main__":
    main()