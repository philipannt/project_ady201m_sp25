import requests
from bs4 import BeautifulSoup
import json


url = "https://xe.chotot.com/"

#Cái này là fake user tránh bị ban vì nhầm là bot ( lấy web cái nào ổn định thì dùng)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

product_links = [] #List link product để sau đó sẽ chạy loop vào từng link để lấy thông tin sản phẩm


#Lấy link sản phẩm 8 trang trong web :)

for x in range(1, 9):  
    r = requests.get(f"https://xe.chotot.com/mua-ban-xe-may-da-nang?page={x}", headers=headers)

    soup = BeautifulSoup(r.content, "lxml") #Dùng parser "lxml" ổn định ( vừa chính xác vừa nhanh) - parser khác cũng được nhưng không ổn định lắm
    
    products = soup.find_all("a", href=True, itemprop="item") #Đảm bảo sẽ tìm đúng class a với href = True ( cho mặc định) và itemprop là item)
    
    for item in products:
        link = item['href'] 

        link = url + link if link.startswith("/") else link #Link mà có bắt đầu bằng "/" thì thêm url vào trước link đó

        product_links.append(link) 


product_list = [] #List chứa thông tin sản phẩm sau khi đã lấy được thông tin từ từng link sản phẩm

for link in product_links: #Chạy loop vào từng link sản phẩm để lấy thông tin sản phẩm


    r = requests.get(link, headers=headers) #Gửi request vào từng link sản phẩm, headers để tránh bị ban :(
    soup = BeautifulSoup(r.content, "lxml")
    
    name = soup.find("title").text.strip() #Lấy tên sản phẩm, dùng strip() để xóa khoảng trắng ở đầu và cuối chuỗi

    #Đoạn này vì các thông tin sản phẩm đều sử dụng chung 1 class "bwq0cbs" nên ta sẽ chạy loops vào từng span để lấy thông tin, rồi nhét vào list
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
    
    product_list.append(product) #Thêm thông tin product vào list product_list

    print(f"Scraped: {name}") #F5 đi rồi sẽ biết :) 
    
#Lưu thông tin product vào file json
with open("CHOTOT_motorcycles.json", "w", encoding="utf-8") as f:
    json.dump(product_list, f, ensure_ascii=False, indent=4) #ensure_ascii=False để lưu dấu tiếng Việt, indent=4 để đảm bảo data sẽ không trên cùng 1 dòng

print(f"Scraping completed. ALL PRODUCTS are saved and NO BUGS :)")


