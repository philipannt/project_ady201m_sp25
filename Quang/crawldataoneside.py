import requests
import json
import os
import re
from bs4 import BeautifulSoup

def fetch_chotot_data(ad_id):
    api_url = f'https://gateway.chotot.com/v1/public/ad-listing/{ad_id}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_motorbike_type(name):
    name_lower = name.lower()
    if any(keyword in name_lower for keyword in ["exciter", "winner", "raider", "r15", "zx"]):
        return "Xe côn tay"
    elif any(keyword in name_lower for keyword in ["wave", "future", "jupiter", "sirius"]):
        return "Xe số"
    elif any(keyword in name_lower for keyword in ["vespa", "sh", "vision", "lead", "airblade", "click"]):
        return "Xe tay ga"
    return "Không rõ"

def scrape_chotot_xe(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"API lỗi: {url}")
        return False
    
    # Lấy ID từ URL
    ad_id = url.split('/')[-1].split('.')[0]
    api_data = fetch_chotot_data(ad_id)
    if not api_data:
        print(f"API lỗi: {url}")
        return False

    # Chỉ lưu URL vào JSON
    data_entry = {"url": url}

    # In ra chỉ URL
    print(f"URL: {data_entry['url']}")

    filename = 'xe_url.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {"selection": []}
    else:
        existing_data = {"selection": []}

    existing_data["selection"].append(data_entry)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    return True

def scrape_listing_page(base_url, max_pages=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for page in range(1, max_pages + 1):
        print(f"Đang cào dữ liệu trang {page}...")
        page_url = f"{base_url}&page={page}"
        try:
            response = requests.get(page_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            print(f"Không thể truy cập trang {page}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        ad_links = soup.find_all('a', href=True)

        for link in ad_links:
            ad_url = link['href']
            if ad_url.startswith("/"):
                full_ad_url = f'https://xe.chotot.com{ad_url}'
            elif ad_url.startswith("https://"):
                full_ad_url = ad_url
            else:
                continue  

            scrape_chotot_xe(full_ad_url)

scrape_listing_page("https://xe.chotot.com/mua-ban-xe-may-piaggio-sdmb3?motorbiketype=1", max_pages=5)
