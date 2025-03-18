import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

Made by Huy lo


def figure1(df):
    """ Vẽ 4 biểu đồ phân tích mối quan hệ giữa các biến:
    - Km vs Price (regression)
    - Year vs Price (regression)
    - Location vs Price (barplot)
    - Nation vs Price (violinplot)"""

    fig, axes = plt.subplots(2,2, figsize=(18, 10))

    sns.regplot(x="Km", y="Price", data=df, ax=axes[0,0])
    sns.regplot(x="Year", y="Price", data=df, ax=axes[0,1])
    sns.barplot(x="Location", y="Price", data=df, ax=axes[1,0])
    sns.violinplot(x="Nation", y = "Price", data=df, ax=axes[1,1])
    y_max = 600000000
    for ax in axes.flatten():
        ax.set_ylim(0, y_max)
        ax.yaxis.set_major_locator(MultipleLocator(50_000_000))
        ax.ticklabel_format(style="plain", axis="y")

    axes[0,0].ticklabel_format(style="plain", axis="x")
    axes[0,0].tick_params(axis="x", rotation=45)
    axes[0,0].set_xlabel("Kilometers Driven")

    axes[0,1].tick_params(axis="x", rotation=45)
    axes[0,1].set_xlabel("Year of Manufacture")

    axes[1,0].tick_params(axis="x", rotation=290)
    axes[1,0].set_xlabel("District")

    axes[1,1].tick_params(axis="x", rotation=290)

    plt.tight_layout()
    plt.show()


def figure2(df):
    """Vẽ các biểu đồ phân tích bổ sung cho dự đoán giá xe:
    - Correlation heatmap
    - Price distribution analysis
    - Age analysis
    - Km analysis"""
    
    fig1, axes1 = plt.subplots(2, 2, figsize=(18, 10))
    
    sns.heatmap(df[["Price", "Year", "Km"]].corr(), annot=True, cmap="coolwarm", ax=axes1[0,0], fmt=".2f")
    
    current_year = pd.Timestamp.now().year
    df["Age"] = (current_year - df["Year"]).astype(int)
    sns.boxplot(data=df, x="Age", y="Price", ax=axes1[0,1])
    
    sns.scatterplot(data=df, x="Age", y="Km", alpha=0.5, ax=axes1[1,0])
    
    
    axes1[0,0].set_title("Correlation Matrix", fontsize=15)
    
    
    axes1[0,1].ticklabel_format(style="plain", axis="y")
    axes1[0,1].set_xlabel("Age of Bike")
    axes1[0,1].set_ylabel("Price")

    axes1[1,0].set_xlabel("Age of Bike")
    axes1[1,0].set_ylabel("Kilometers Driven")

    axes1[1,1].axis("off")


    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = pd.read_json("CHOTOT_motorcycles2.json")


    df_binary = df[["name", "price", "Location", "Year_of_manufacture", "Kilometers_driven", "Nationality", "Listing_time"]]

    df_binary.columns = ["Name", "Price", "Location", "Year", "Km", "Nation", "Time Post"]


    df_binary["Price"] = pd.to_numeric(df_binary["Price"].str.replace(".", "").str.replace(" đ", ""), errors="coerce")
    df_binary["Year"] = pd.to_numeric(df_binary["Year"], errors="coerce")
    df_binary["Km"] = pd.to_numeric(df_binary["Km"].str.replace(" km", ""), errors="coerce")
    df_binary["Location"] = df_binary["Location"].str.extract(r"(Quận [^,]+)")
    df_binary["Nation"] = df_binary["Nation"].where(
        (df_binary["Nation"] != "Đang cập nhật") & (~df_binary["Nation"].str.contains("Phường"))
    )

    df_binary= df_binary.dropna(subset=["Price", "Year", "Km", "Location", "Nation", "Time Post"])

    print(df_binary)
    
    figure1(df_binary)
    figure2(df_binary)


