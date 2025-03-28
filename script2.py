import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# AWS S3 Configuration
BUCKET_NAME = "gatono-sales"  # Ensure this matches your S3 bucket name
FILE_KEY = "sales_records.csv"  # Update this if your file is in a subfolder

def download_csv_from_s3(bucket_name, file_key):
    """
    Download CSV file from AWS S3 bucket and return a Pandas DataFrame.
    """
    s3_client = boto3.client("s3", region_name="us-east-1")

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response["Body"].read().decode("utf-8")
        
        # Read into DataFrame
        df = pd.read_csv(StringIO(csv_content))
        return df

    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return None

def analyze_sales_data(df):
    """
    Perform basic sales analysis and generate a bar chart.
    """
    if df is None or df.empty:
        print("No data available for analysis.")
        return
    
    print("\n🔹 First 5 rows of data:")
    print(df.head())

    # Ensure required columns exist
    if "Total_Sales" in df.columns and "Product" in df.columns:
        total_sales = df["Total_Sales"].sum()
        avg_sales = df["Total_Sales"].mean()
        product_sales = df.groupby("Product")["Total_Sales"].sum()

        print(f"\n📊 Total Sales: ${total_sales:,.2f}")
        print(f"📉 Average Sales per Transaction: ${avg_sales:,.2f}")
        print(f"🏆 Top-Selling Product: {product_sales.idxmax()}")

        # Plot sales per product as a bar chart
        plt.figure(figsize=(10, 5))
        sns.barplot(x=product_sales.index, y=product_sales.values, palette="viridis")

        plt.title("Total Sales per Product", fontsize=14)
        plt.xlabel("Product", fontsize=12)
        plt.ylabel("Total Sales ($)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Show the graph
        plt.show()

    else:
        print("⚠️ Required columns ('Total_Sales', 'Product') not found in dataset.")

if __name__ == "__main__":
    # Download and analyze sales data
    sales_df = download_csv_from_s3(BUCKET_NAME, FILE_KEY)
    analyze_sales_data(sales_df)
