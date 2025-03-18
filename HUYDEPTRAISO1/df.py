import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MultipleLocator


# Đọc file từ file JSON
df = pd.read_json("CHOTOT_motorcycles2.json")


df_binary = df[["name", "price", "Location", "Year_of_manufacture", "Kilometers_driven"]]

df_binary.columns = ["Name", "Price", "Location", "Year", "Km"]


df_binary["Price"] = pd.to_numeric(df_binary["Price"].str.replace(".", "").str.replace(" đ", ""), errors="coerce")
df_binary["Year"] = pd.to_numeric(df_binary["Year"], errors="coerce")
df_binary["Km"] = pd.to_numeric(df_binary["Km"].str.replace(" km", ""), errors="coerce")
df_binary["Location"] = df_binary["Location"].str.extract(r"(Quận [^,]+)")

print(df_binary)


fig, axes = plt.subplots(2,2, figsize=(18, 10))

sns.regplot(x="Km", y="Price", data=df_binary, ax=axes[0,0])
sns.regplot(x="Year", y="Price", data=df_binary, ax=axes[0,1])
sns.barplot(x="Location", y="Price", data=df_binary, ax=axes[1,0])
axes[1,1].axis("off")

y_max = 600000000
for ax in axes.flatten():
    ax.set_ylim(0, y_max)
    ax.yaxis.set_major_locator(MultipleLocator(50_000_000))
    ax.ticklabel_format(style="plain", axis="y")

axes[0,0].ticklabel_format(style="plain", axis="x")
axes[0,0].tick_params(axis="x", rotation=45)
axes[0,0].set_xlabel("Số Km")

axes[0,1].tick_params(axis="x", rotation=45)
axes[0,1].set_xlabel("Năm sản xuất")

axes[1,0].tick_params(axis="x", rotation=290)
axes[1,0].set_xlabel("Khu vực")

plt.tight_layout()
plt.show()



