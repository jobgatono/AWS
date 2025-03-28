import boto3
import pandas as pd
from io import StringIO

# AWS S3 Configuration
BUCKET_NAME = "gatono-sales"
FILE_KEY = "sales_records.csv"  # Change this to match your actual file name

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
    Perform basic sales analysis.
    """
    if df is None or df.empty:
        print("No data available for analysis.")
        return
    
    print("\n🔹 First 5 rows of data:")
    print(df.head())

    # Assuming columns: 'Product', 'Quantity', 'Price', 'Total_Sales'
    if "Total_Sales" in df.columns:
        total_sales = df["Total_Sales"].sum()
        avg_sales = df["Total_Sales"].mean()
        top_product = df.groupby("Product")["Total_Sales"].sum().idxmax()

        print(f"\n📊 Total Sales: ${total_sales:,.2f}")
        print(f"📉 Average Sales per Transaction: ${avg_sales:,.2f}")
        print(f"🏆 Top-Selling Product: {top_product}")
    else:
        print("⚠️ 'Total_Sales' column not found in dataset.")

if __name__ == "__main__":
    # Download and analyze sales data
    sales_df = download_csv_from_s3(BUCKET_NAME, FILE_KEY)
    analyze_sales_data(sales_df)
