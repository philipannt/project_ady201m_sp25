import pyodbc
import json

#1. python - how to make sql connection using pyodbc

#2. call sql procedure to insert records to database (without parameter)

#3. read json object and pass json to sql procedure (with parameter)

#4. read json from json file and pass json to sql procedure

#5. how to pass unicode (chinese, hindi) characters from json to sql




#1 Tạo server trước tiên
conn = pyodbc.connect("Driver={SQL Server};Server=LAPTOP-UCC2QQI9;Database=ADY4;Trusted_Connection=yes;")

#'Driver={SQL Server};Server=LAPTOP-UCC2QQI9;Database=Employee;Trusted_Connection=yes;'
# Thay bằng server name của mình vào
# Database = tên mình muốn connect
# Trusted_Connection=yes; : dùng windows authentication

conn.timeout = 400
conn.autocommit = True # Tự động commit ko cần gọi conn.commit sau mỗi excute

try:
    cursor =conn.cursor()


    with open("CHOTOT_motorcycles2.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    json_string = json.dumps(data, separators=(",", ":"), ensure_ascii= False, indent= None).strip()
    
    cursor.execute("EXEC prcInsertDataOfBike @json = ?", json_string)
    print("Inserted Data")

except pyodbc.Error as err:
    print(f"Error {err}")

except:
    print("Something else failed not in pyodbc")


conn.close()
print("Close Database Connection")
