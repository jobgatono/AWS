import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# AWS S3 Configuration
BUCKET_NAME = "gatono-sales"  # Update with your actual bucket name
FILE_KEY = "sales_records.csv"  # Update with correct file path if needed

def download_csv_from_s3(bucket_name, file_key):
    """
    Download CSV file from AWS S3 bucket and return a Pandas DataFrame.
    """
    s3_client = boto3.client("s3", region_name="us-east-1")

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response["Body"].read().decode("utf-8")
        
        # Read CSV into a DataFrame
        df = pd.read_csv(StringIO(csv_content))
        return df

    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return None

def generate_pivot_table(df):
    """
    Generate a pivot table summarizing total and average sales per product.
    Export it to Excel and visualize it as a heatmap.
    """
    if df is None or df.empty:
        print("No data available for analysis.")
        return
    
    print("\n🔹 First 5 rows of data:")
    print(df.head())

    # Ensure required columns exist
    required_columns = {"Date", "Product", "Total_Sales"}
    if required_columns.issubset(df.columns):
        # Convert 'Date' column to datetime
        df["Date"] = pd.to_datetime(df["Date"])

        # Create Pivot Table
        pivot_table = df.pivot_table(
            values="Total_Sales",
            index="Product",
            columns=df["Date"].dt.to_period("M"),  # Group by month
            aggfunc="sum",  # Summarize with total sales
            fill_value=0  # Replace missing values with 0
        )

        print("\n📊 Sales Pivot Table:")
        print(pivot_table)

        # ✅ Export pivot table to Excel
        excel_filename = "sales_pivot.xlsx"
        pivot_table.to_excel(excel_filename)
        print(f"📂 Pivot table saved to: {excel_filename}")

        # ✅ Generate heatmap visualization
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

        plt.title("Sales Heatmap (Total Sales per Product & Month)", fontsize=14)
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Product", fontsize=12)
        plt.xticks(rotation=45)

        # Show the heatmap
        plt.show()

    else:
        print("⚠️ Required columns ('Date', 'Product', 'Total_Sales') not found in dataset.")

if __name__ == "__main__":
    # Download and analyze sales data
    sales_df = download_csv_from_s3(BUCKET_NAME, FILE_KEY)
    generate_pivot_table(sales_df)
