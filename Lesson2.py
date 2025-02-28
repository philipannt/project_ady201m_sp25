import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import json

def scrape_chotot(pages):
    try:
        url = "https://xe.chotot.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        
        product_links = []
        product_list = []
        
        for x in range(1, pages + 1):

            r = requests.get(f"https://xe.chotot.com/mua-ban-xe-may-da-nang?page={x}", headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            products = soup.find_all("a", href=True, itemprop="item")
            
            
            for item in products:
                link = item['href']
                link = url + link if link.startswith("/") else link
                product_links.append(link)
        
        
        for link in product_links:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            name = soup.find("title").text.strip()
            
            info_spans = soup.find_all("span", class_="bwq0cbs")
            info_list = [span.text.strip() for span in info_spans]
            
            price_tag = soup.find("b", class_="p26z2wb")
            price = price_tag.text.strip() if price_tag else "Price not available"
            
            product = {
                "name": name,
                "info": {
                    "Year of manufacture": info_list[0] if len(info_list) > 0 else "NONE",
                    "Kilometers driven": info_list[1] if len(info_list) > 1 else "NONE",
                    "Nationality": info_list[2] if len(info_list) > 2 else "NONE",
                    "Location": info_list[3] if len(info_list) > 3 else "NONE",
                    "Listing time": info_list[4] if len(info_list) > 4 else "NONE"
                },
                "price": price
            }
            
            product_list.append(product)
            print(f"Scraped: {name}")
        
        with open("CHOTOT_motorcycles.json", "w", encoding="utf-8") as f:
            json.dump(product_list, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("Success", "Scraping completed! Data saved to CHOTOT_motorcycles.json")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def crawl_sele():
    import re
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.honda.com.vn/xe-may/san-pham"
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "category-item")))

    bike_elements = driver.find_elements(By.CLASS_NAME, "category-item")

    data = []

    for bike in bike_elements:
        try:
            brand = "Honda"
            name = bike.find_element(By.CLASS_NAME, "nameAndColor").text.strip()
            price_text = bike.get_attribute("data-price_from")
            price = re.sub(r"[^\d]", "", price_text) if price_text else "N/A"
            url = bike.find_element(By.TAG_NAME, "a").get_attribute("href")

            data.append([brand, name, price, url])

        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")

    driver.quit()

    df = pd.DataFrame(data, columns=["Thương hiệu", "Model", "Giá", "Link"])
    df.to_csv("honda.csv", index=False, encoding="utf-8-sig")

    print("Done")

def create_gui():
    root = tk.Tk()
    root.title("Chotot Scraper Tool")
    root.geometry("400x400")
    root.attributes("-topmost", True)
    
    title = tk.Label(root, text="Chotot Motorcycle Scraper", font=("Arial", 16))
    title.place(width=400, height=30, x=8, y=20)
    
    page = tk.Label(root, text="Number of pages to scrape:")
    page.place(width=200, height=30, x=100, y=60)

    page_entry = tk.Entry(root, font=("Arial", 16))
    page_entry.place(width=200, height=30, x=105, y=100)
    page_entry.focus()
    

    def start_scraping():
        try:
            pages = int(page_entry.get())
            if pages <= 0:
                raise ValueError("Please enter a positive number.")
            scrape_chotot(pages)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    
    scrap = tk.Button(root, text="Start Scraping", command=crawl_sele, bg="green", fg="white")
    scrap.place(width=150, height=30, x=125, y=160)
    
    exit = tk.Button(root, text="Exit", command=root.quit, bg="grey", fg="white")
    exit.place(width=80, height=30, x=320, y=370)
    
    root.mainloop()


if __name__ == "__main__":
    create_gui()

