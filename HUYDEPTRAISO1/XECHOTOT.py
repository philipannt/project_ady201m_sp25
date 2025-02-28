import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import json

def scrape_chotot(url, pages):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        
        product_links = []
        product_list = []
        
        for x in range(1, pages + 1):
            url_link = f"{url}?page={x}"

            r = requests.get(url_link, headers=headers)

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


def create_gui():
    root = tk.Tk()
    root.title("Chotot Scraper Tool")
    root.geometry("400x400")
    root.attributes("-topmost", True)
    
    title = tk.Label(root, text="Chotot Motorcycle Scraper", font=("Arial", 16))
    title.place(width=400, height=30, x=8, y=20)
    
    page = tk.Label(root, text="Number of pages to scrape:")
    page.place(width=200, height=30, x=100, y=60)

    url_entry = tk.Label(root, text="Enter the URL:")
    url_entry.place(width=200, height=30, x=100, y=130)

    page_entry = tk.Entry(root, font=("Arial", 16))
    page_entry.place(width=200, height=30, x=105, y=100)
    page_entry.focus()

    url_entry = tk.Entry(root, font=("Arial", 12))
    url_entry.place(width=200, height=30, x=105, y=160)
    url_entry.focus()
    

    def start_scraping():
        try:
            url = url_entry.get().strip()
            pages = int(page_entry.get())
            if not url or pages <= 0:
                raise ValueError("Please enter a positive number.")
            scrape_chotot(url, pages)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    
    scrap = tk.Button(root, text="Start Scraping", command=start_scraping, bg="green", fg="white")
    scrap.place(width=150, height=30, x=125, y=240)
    
    exit = tk.Button(root, text="Exit", command=root.quit, bg="grey", fg="white")
    exit.place(width=80, height=30, x=320, y=370)
    
    root.mainloop()


if __name__ == "__main__":
    create_gui()

