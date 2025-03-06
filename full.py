from selenium import webdriver
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
import requests
import os

def scrape_chotot(url, pages):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }

        product_links = []
        product_list = []

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        for x in range(1, pages + 1):
            url_link = f"{url}?page={x}"
            r = requests.get(url_link, headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            products = soup.find_all("a", href=True, itemprop="item", class_="cebeqpz")

            for item in products:
                link = item['href']
                link = url + link if link.startswith("/") else link 
                product_links.append(link)

        for link in product_links:
            driver.get(link)
            
            soup = BeautifulSoup(driver.page_source, "lxml")
            name = soup.find("title").text.strip()
            
            info_spans = soup.find_all("span", class_="bwq0cbs")
            info_list = [span.text.strip() for span in info_spans]

            year = info_list[0] if len(info_list) > 0 else "NONE"
            km = info_list[1] if len(info_list) > 1 else "NONE"
            nation = info_list[2] if len(info_list) > 2 else "NONE"
            location = info_list[3] if len(info_list) > 3 else "NONE"
            time = info_list[4] if len(info_list) > 4 else "NONE"
            
            price_tag = soup.find("b", class_="p26z2wb")
            price = price_tag.text.strip() if price_tag else "Price not available"

            price_elements = soup.find_all("div", class_="p1wx4fkc")
            price_min = price_elements[0].text.strip() if len(price_elements) > 0 else "Price not available"
            price_max = price_elements[1].text.strip() if len(price_elements) > 1 else "Price not available"

            product = {
                "name": name,
                "Year_of_manufacture": year,
                "Kilometers_driven": km,
                "Nationality": nation,
                "Location": location,
                "Listing_time": time,
                "price": price,
                "price_min": price_min,
                "price_max": price_max
            }

            product_list.append(product)
            
            print(product_links.index(link) + 1)
        
        driver.quit()
        return pd.DataFrame(product_list)

    except:
        return "Crawl error."

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
        print("Connected")
        return conn

    except:
        return "Connection error."

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS PROJ_ADY")

    except:
        return "Create database error."

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
        return "Create table error."

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

        cursor.executemany(insert_query, df.to_records(index=False))

    except:
        return "Insert error"

def show_data(cursor):
    try:
        cursor.execute("SELECT * FROM tbl_Xemaychotot")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)

    except:
        return "Collect error"

def main():
    try:
        conn = connect_cloud()
        cursor = conn.cursor()

        create_database(cursor)
        conn.database = "PROJ_ADY"

        create_table(cursor)
        conn.commit()
        print("Done.")
        
        df = scrape_chotot("https://xe.chotot.com/mua-ban-xe-may-da-nang", 9)
        insert_data(cursor, df)
        conn.commit()
        print("Done.")

        print("Data inserted successfully.")

        # data = show_data(cursor)
        # data.to_csv("output.csv", index=False, encoding="utf-8")

    except:
        return "Main error."

    finally:
        cursor.close()
        conn.close()

if __name__=="__main__":
    main()