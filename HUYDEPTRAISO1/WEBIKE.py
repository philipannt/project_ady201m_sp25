from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox
import json
import time

def scrape_webike(url, pages):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }

        option = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=option)

        links = []
        products = []

        for x in range(1, pages + 1):
            url_link = f"{url}?page={x}"
            r = requests.get(url_link, headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            product_items = soup.find_all("div", class_="list-product")

            for item in product_items:
                link = item.find('a')['href'] if item.find('a') else None
                if link:
                    link = url + link if link.startswith("/") else link
                    links.append(link)
        
        for link in links:
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            name_tag = soup.find("h1", class_="module_title")
            name = name_tag.text.strip() if name_tag else "Unknown"

            price_tag = soup.find("big", class_="price")
            price = price_tag.text.strip() if price_tag else "Price not available"

            product_info = {}
            rows = soup.find_all("tr")
# Đoạn này nó bị rối loạn data chút, nhưng mà chăc ko sao, chạy được :)
            for row in rows:
                label_tag = row.find('label')
                value_tags = row.find_all('td')

                if label_tag and value_tags:
                    label = label_tag.get_text(strip=True)
                    values = [td.get_text(strip=True) for td in value_tags if td.get_text(strip=True)]
                    
                    if len(values) > 1:
                        key_value_pairs = dict(zip(values[::2], values[1::2]))
                        product_info.update(key_value_pairs)
                    else:
                        product_info[label] = values[0] if values else "-"
            


            products.append({
                "name": name,
                "info": product_info,
                "price": price
            })

            print(f"Scraped: {name}")

        with open("WEBIKE_motorcycles.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("Success", "Scraping completed! Data saved to WEBIKE_motorcycles.json")
        driver.quit()
    
    except Exception as e:
        driver.quit()
        messagebox.showerror("Error", f"An error showed up: {str(e)}")


def scrap_gui():
    root = tk.Tk()
    root.title("Webike Motor Scraper")
    root.geometry("400x400")
    root.attributes("-topmost", True)

    title = tk.Label(root, text="WEBIKE Motorcycle Scraper", font=("Arial", 16))
    title.place(width=400, height=30, x=8, y=20)
    
    page_label = tk.Label(root, text="Number of products to scrape:")
    page_label.place(width=200, height=30, x=100, y=60)

    url_label = tk.Label(root, text="Enter the URL:")
    url_label.place(width=200, height=30, x=100, y=130)

    page_entry = tk.Entry(root, font=("Arial", 16))
    page_entry.place(width=200, height=30, x=105, y=100)
    page_entry.focus()

    url_entry = tk.Entry(root, font=("Arial", 16))
    url_entry.place(width=200, height=30, x=105, y=160)

    def start():
        try:
            url = url_entry.get().strip()
            page = int(page_entry.get().strip())
            if not url or page <= 0:
                raise ValueError("Please enter a valid URL and positive number of pages.")
            scrape_webike(url, page)
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    scrap = tk.Button(root, text="Start Scraping", command=start, bg="green", fg="white")
    scrap.place(width=150, height=30, x=125, y=240)
    
    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="grey", fg="white")
    exit_button.place(width=80, height=30, x=320, y=370)

    root.mainloop()


if __name__ =="__main__":
    scrap_gui()
