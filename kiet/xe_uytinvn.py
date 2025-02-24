import requests
from bs4 import BeautifulSoup
import time
import json

base_url = "https://xeuytin.vn/xecu?thanhpho=&quanhuyen=&hangxe=&loaixe=&tinhtrang=xe-cu&dongxe=&phienban=&loaicuahang=&mausac=&namdangkyxe=&sokmdasudung=&giatu=&giaden=&orderby=&utm_source=website&utm_medium=timkiem&utm_campaign=timkiem"

headers = {"User-Agent": "Mozilla/5.0"}

list_xe = set()

for page in range(1, 6):
    url = base_url + str(page)
    print(f"Đang lấy danh sách xe từ {url} ...")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        xe_links = soup.find_all("a", href=True)
        for link in xe_links:
            href = link["href"]
            if "/xeban/detail/" in href:
                full_url = f"https://xeuytin.vn{href}"
                list_xe.add(full_url)
    time.sleep(2)

list_xe = list(list_xe)
print(f"Tìm thấy {len(list_xe)} xe. Bắt đầu lấy dữ liệu chi tiết...")

data_list = []

for url_xe in list_xe:
    print(f"Đang lấy dữ liệu xe: {url_xe}")
    response = requests.get(url_xe, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        gia_xe = soup.find("span", class_="current font18")
        gia_xe = gia_xe.text.strip() if gia_xe else "Không có dữ liệu"
        
        thong_tin_xe = soup.find("div", class_="alert alert-primary")
        if thong_tin_xe:
            table_rows = thong_tin_xe.find("tbody").find_all("td")
            hang_xe, loai_xe, dong_xe, phien_ban, mau_sac = [td.text.strip() for td in table_rows]
        else:
            hang_xe = loai_xe = dong_xe = phien_ban = mau_sac = "Không có dữ liệu"
        
        thong_tin_dang_ky = soup.find("div", class_="alert alert-danger")
        if thong_tin_dang_ky:
            table_rows = thong_tin_dang_ky.find("tbody").find_all("td")
            bien_so, so_km, nam_dang_ky = [td.text.strip() for td in table_rows]
        else:
            bien_so = so_km = nam_dang_ky = "Không có dữ liệu"
        
        vi_tri_xe = soup.find("div", class_="alert alert-success")
        if vi_tri_xe:
            table_rows = vi_tri_xe.find("tbody").find_all("td")
            thanh_pho, quan_huyen, phuong_xa, duong = [td.text.strip() for td in table_rows]
        else:
            thanh_pho = quan_huyen = phuong_xa = duong = "Không có dữ liệu"
        
        data = {
            "Price": gia_xe,
            "Brand": hang_xe,
            "Type": loai_xe,
            "Model": dong_xe,
            "Version": phien_ban,
            "Color": mau_sac,
            "Lience_plate": bien_so,
            "Mileage": so_km,
            "Registration_year": nam_dang_ky,
            "City": thanh_pho,
            "District": quan_huyen,
            "Ward": phuong_xa,
        }
        data_list.append(data)
    time.sleep(2)

with open("xe_data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print("Đã lưu dữ liệu vào xe_data.json thành công!")
