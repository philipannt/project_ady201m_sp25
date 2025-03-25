import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
import csv


# Tạo Scrape bằng selenium kết hợp beautisoup

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
            # time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, "lxml")
            name = soup.find("title").text.strip()
            
            price_tag = soup.find("b", class_="p26z2wb")
            price = price_tag.text.strip() if price_tag else "Không có giá"
            
            price_elements = soup.find_all("div", class_="p1wx4fkc")
            price_min = price_elements[0].text.strip() if len(price_elements) > 0 else "Price not available"
            price_max = price_elements[1].text.strip() if len(price_elements) > 1 else "Price not available"

            
            price_range_div = soup.find("div", class_="r631mvb")
            if price_range_div:
                price_elements = price_range_div.find_all("div", class_="p1wx4fkc")
                if len(price_elements) >= 2:
                    price_min = price_elements[0].text.strip()
                    price_max = price_elements[1].text.strip()
            
            specs_section = soup.find("h2", class_="tfvqu6u", string="Thông số kỹ thuật")
            specs = {}
            
            if specs_section:
                parent_container = specs_section.parent
                if parent_container:
                    spec_rows = parent_container.find_all("div", class_="pqp26ip")
                    
                    for row in spec_rows:
                        label_span = row.find("span", class_="bwq0cbs")
                        label = label_span.text.strip() if label_span else ""
                        
                        value = ""
                        
                        a_tag = row.find("a")
                        if a_tag:
                            value_span = a_tag.find("span", class_="bwq0cbs")
                            if value_span:
                                value = value_span.text.strip()
                        else:
                            spans = row.find_all("span", class_="bwq0cbs")
                            if len(spans) > 1:
                                value = spans[1].text.strip()
                        
                        if label:  
                            specs[label] = value
            
            product = {
                # "Name": name,
                "Price": price,
                "Min_Price": price_min,
                # "Max_Price": price_max,
                "Brand": specs.get("Hãng xe:", "Không có thông tin"),
                "Model": specs.get("Dòng xe:", "Không có thông tin"),
                "Year of Manufacture": specs.get("Năm đăng ký:", "Không có thông tin"),
                "Kilometer Driven": specs.get("Số Km đã đi:", "Không có thông tin"),
                # "Type": specs.get("Loại xe:", "Không có thông tin"),
                # "Engine Capacity": specs.get("Dung tích xe:", "Không có thông tin"),
                # "Nationality": specs.get("Xuất xứ:", "Không có thông tin")
                
            }
            
            info_spans = soup.find_all("span", class_="bwq0cbs")
            location = ""
            time_posted = ""
            
            for i, span in enumerate(info_spans):
                text = span.text.strip()
                if "Quận" in text or "Huyện" in text or "Phường" in text:
                    location = text
                elif "phút trước" in text or "giờ trước" in text or "ngày trước" in text:
                    time_posted = text
            
            product["Địa điểm"] = location if location else "NaN"
            product["Thời gian đăng"] = time_posted if time_posted else "NaN"

            product_list.append(product)
            print(f"Scrapped: {name}")
        
        if product_list:
            csv_columns = product_list[0].keys()
            
            with open("CHOTOT_motorcycles.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerows(product_list)
            
            print(f"Đã lưu {len(product_list)} sản phẩm vào CHOTOT_motorcycles.csv")
            messagebox.showinfo("Thành công", f"Đã lưu {len(product_list)} sản phẩm vào CHOTOT_motorcycles.csv")
        else:
            print("Không có dữ liệu để lưu")
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu")
        
        # with open("CHOTOT_motorcycles.json", "w", encoding="utf-8") as f:
        #     json.dump(product_list, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("Success", "Data saved in CHOTOT_motorcycles.csv")
        driver.quit()

    except Exception as e:
        messagebox.showerror("Error", f"Warning: {str(e)}")

def create_gui():
    root = tk.Tk()
    root.title("Chotot Scraper Tool")
    root.geometry("400x400")
    root.attributes("-topmost", True)
    
    title = tk.Label(root, text="Chotot Motorcycle Scraper", font=("Arial", 16))
    title.place(width=400, height=30, x=8, y=20)
    
    page = tk.Label(root, text="Number of pages to scrape:")
    page.place(width=200, height=30, x=100, y=60)

    url_label = tk.Label(root, text="Enter the URL:")
    url_label.place(width=200, height=30, x=100, y=130)

    page_entry = tk.Entry(root, font=("Arial", 16))
    page_entry.place(width=200, height=30, x=105, y=100)
    page_entry.focus()

    url_entry = tk.Entry(root, font=("Arial", 12))
    url_entry.place(width=200, height=30, x=105, y=160)
    
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
    
    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="grey", fg="white")
    exit_button.place(width=80, height=30, x=320, y=370)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
