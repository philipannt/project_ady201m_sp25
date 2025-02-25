import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

BASE_URL = "https://www.webike.vn"

def get_total_pages(url):
    """Lấy tổng số trang từ phân trang"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Không thể truy cập trang web!")
        return 1  # Mặc định 1 trang nếu không tìm thấy

    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.select("ul.pagination a")  # Tìm tất cả các thẻ chuyển trang

    page_numbers = []
    for a in pagination:
        if a.text.isdigit():
            page_numbers.append(int(a.text))  # Lưu số trang dưới dạng số nguyên

    return max(page_numbers) if page_numbers else 1  # Trả về số trang lớn nhất

def scrape_list_page(url, max_pages=5):
    """Cào danh sách xe từ tối đa max_pages trang"""
    total_pages = get_total_pages(url)
    bike_links = set()

    for page in range(1, min(total_pages, max_pages) + 1):  # Giới hạn số trang
        print(f"Đang cào trang {page}/{min(total_pages, max_pages)}...")
        page_url = f"{url}?page={page}"  # Thêm tham số ?page= vào URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(page_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Không thể truy cập {page_url}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            if "bike-detail" in a["href"]:
                full_link = a["href"] if a["href"].startswith("http") else urljoin(BASE_URL, a["href"])
                bike_links.add(full_link)

        time.sleep(1.5)  # Tránh bị chặn vì gửi request quá nhanh

    return list(bike_links)

def get_text_by_label(soup, label_title):
    # Tìm label có tiêu đề phù hợp
    label = soup.find("label", {"title": label_title})
    if label:
        td = label.find_parent("td")  # Tìm ô chứa label
        if td:
            next_td = td.find_next("td")  # Lấy ô dữ liệu kế bên
            return " ".join(next_td.text.split()).strip() if next_td else "Không có dữ liệu"
    return "Không có dữ liệu"

def scrape_bike_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Không thể truy cập {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.select_one("big.price")
    seller = soup.select_one(".customer_info p.name a b")

    bike_data = {
        "Dòng xe": get_text_by_label(soup, ''),
        "Giá": price.text.strip() if price else "Không có dữ liệu",
        "Năm sản xuất": get_text_by_label(soup, "Đời xe"),
        "Số km đã đi": get_text_by_label(soup, "Đã đi"),
        "Địa điểm": get_text_by_label(soup, "Địa điểm"),
        "Người bán": seller.text.strip() if seller else "Không có dữ liệu",
        "URL": url
    }

    return bike_data

list_url = "https://www.webike.vn/cho-xe-may/bike-list/honda/st-xe-ga/xe-cu.html"
bike_links = scrape_list_page(list_url, max_pages=5)  # Chỉ lấy tối đa 2 trang

bike_data_list = []
if bike_links:
    print(f"Tìm thấy tổng cộng {len(bike_links)} xe.")

    for link in bike_links:
        data = scrape_bike_details(link)
        if data:
            bike_data_list.append(data)
        time.sleep(2)  # Tránh bị chặn khi gửi quá nhiều request nhanh

    with open("bike_data.json", "w", encoding="utf-8") as f:
        json.dump(bike_data_list, f, ensure_ascii=False, indent=4)
    print("Dữ liệu đã được lưu vào bike_data.json")
