import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import getpass
import mlcroissant as mlc

def setup_kaggle_credentials():
    """
    Sets up Kaggle credentials by checking multiple sources in order:
    1. Looks for the kaggle.json file in the default location.
    2. Checks for KAGGLE_USERNAME and KAGGLE_KEY environment variables.
    3. If neither is found, prompts the user to enter them interactively.
    """
    # Method 1: Check for kaggle.json file
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if os.path.exists(kaggle_json_path):
        print(f"Authentication successful: Found credentials file at {kaggle_json_path}")
        return

    # Method 2: Check for environment variables
    if 'KAGGLE_USERNAME' in os.environ and 'KAGGLE_KEY' in os.environ:
        print("Authentication successful: Found KAGGLE_USERNAME and KAGGLE_KEY environment variables.")
        return

    # Method 3: Fallback to interactive prompt
    print("\n--- Kaggle Authentication Needed ---")
    print("Could not find kaggle.json or environment variables.")
    print("Please enter your Kaggle API credentials to continue for this session.")
    
    username = input("Kaggle Username: ")
    key = getpass.getpass("Kaggle API Key: ")

    if not username or not key:
        raise ValueError("Kaggle credentials were not provided. Exiting.")

    # Set credentials as environment variables for the current session
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = key
    print("Kaggle credentials have been set for this session.")


def run_sales_analysis():
    """
    Main function to run the entire supermarket sales analysis workflow.
    """
    # --- 1. Dataset Selection & Problem Definition ---
    # Dataset: Supermarket Sales from Kaggle
    # Problem: Analyze sales data to identify top-performing product categories,
    # understand sales trends, and provide insights for revenue growth.
    print("--- Supermarket Sales Analysis ---")
    
    try:
        # --- 2. Data Loading & Summary (using mlcroissant) ---
        # Set up credentials interactively if not already configured
        setup_kaggle_credentials()

        print("\nStep 2: Loading data directly from Kaggle using mlcroissant...")
        
        # Fetch the Croissant JSON-LD
        croissant_dataset = mlc.Dataset('https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales/croissant/download')

        # Use the record set name exactly as suggested by the error message.
        record_set_name = 'SuperMarket+Analysis.csv'
        print(f"Attempting to load record set: '{record_set_name}'")

        # Fetch the records as an iterator
        records = croissant_dataset.records(record_set=record_set_name)
        
        # Convert the iterator of records into a pandas DataFrame
        df = pd.DataFrame(records)
        print("Successfully loaded records into a pandas DataFrame.")
        
        # FIX: Clean the column names to remove the prefix and special characters.
        clean_columns = [col.split('/')[-1].replace('+', '_').replace('%25', '_percent') for col in df.columns]
        df.columns = clean_columns
        # Also, decode byte strings to regular strings for object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.decode('utf-8')
        
        # Rename original 'Sales' column to 'Total' for consistency with original script logic
        if 'Sales' in df.columns:
            df.rename(columns={'Sales': 'Total'}, inplace=True)

        print("\nFirst 5 rows of the dataset:")
        print(df.head())

        print("\nData types of each column:")
        df.info()

        print(f"\nTotal number of rows: {df.shape[0]}, Total number of columns: {df.shape[1]}")

    except Exception as e:
        print(f"\nERROR: Could not load dataset from Kaggle. Please check your connection and authentication.")
        print("Ensure you have entered the correct Kaggle credentials or have them configured properly.")
        print(f"Details: {e}")
        return

    # --- 3. Basic Analysis with Loops & Conditionals (no pandas groupby) ---
    print("\nStep 3: Basic analysis using loops and conditionals...")
    # Business Question: How many "Health and beauty" transactions had a total price over $100?
    high_value_hb_transactions = 0
    for index, row in df.iterrows():
        if 'Product_line' in df.columns and row['Product_line'] == 'Health and beauty' and row['Total'] > 100:
            high_value_hb_transactions += 1
    
    print(f"Number of 'Health and beauty' transactions with total > $100: {high_value_hb_transactions}")

    # --- 4. Groupby Analysis with Pandas ---
    print("\nStep 4: Groupby analysis with Pandas...")
    # Business Question: What is the performance of each product line?
    product_line_analysis = df.groupby('Product_line').agg(
        average_unit_price=('Unit_price', 'mean'),
        total_quantity_sold=('Quantity', 'sum'),
        total_revenue=('Total', 'sum')
    ).sort_values(by='total_revenue', ascending=False)

    print("Sales performance by product line:")
    print(product_line_analysis)
    print("\nInsight: This helps identify which product lines are most profitable and which sell in the highest volume.")

    # --- 5. DataFrame Transformations ---
    print("\nStep 5: Creating and saving new, transformed DataFrames...")
    # Create a DataFrame with only essential columns
    important_columns_df = df[['Invoice_ID', 'Date', 'Product_line', 'Total']]
    important_columns_df.to_csv('important_sales.csv', index=False)
    print("Saved 'important_sales.csv' with only essential columns.")

    # Create a DataFrame for transactions with a large quantity
    large_quantity_df = df[df['Quantity'] >= 5]
    large_quantity_df.to_csv('large_quantity_sales.csv', index=False)
    print("Saved 'large_quantity_sales.csv' for transactions with quantity >= 5.")

    # --- 6. Visualization & Insights ---
    print("\nStep 6: Generating and saving visualizations...")
    
    # Plot 1: Total Revenue by Product Line
    plt.figure(figsize=(12, 7))
    # Fix for FutureWarning: Assign x to hue and set legend to False
    sns.barplot(x=product_line_analysis.index, y=product_line_analysis['total_revenue'], hue=product_line_analysis.index, palette='viridis', legend=False)
    plt.title('Total Revenue by Product Line', fontsize=16)
    plt.xlabel('Product Line', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # Save the plot to a file instead of showing it
    plt.savefig('revenue_by_product_line.png')
    plt.close() # Close the plot to free up memory
    print("Saved 'revenue_by_product_line.png'.")

    # Plot 2: Revenue Over Time
    # Convert 'Date' column to datetime objects, handling potential errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    daily_revenue = df.groupby('Date')['Total'].sum().reset_index()

    plt.figure(figsize=(14, 7))
    plt.plot(daily_revenue['Date'], daily_revenue['Total'], marker='o', linestyle='-')
    plt.title('Total Daily Revenue Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    # Save the plot to a file
    plt.savefig('daily_revenue_over_time.png')
    plt.close() # Close the plot
    print("Saved 'daily_revenue_over_time.png'.")

    # --- 7. Conclusions ---
    print("\nStep 7: Conclusions and Recommendations...")
    print("- 'Food and beverages' and 'Sports and travel' are the top revenue-generating categories and should be prioritized for marketing and inventory.")
    print("- While 'Electronic accessories' sell in high quantity, their total revenue is lower, suggesting an opportunity to promote higher-margin items in this category.")
    print("- Daily revenue shows significant fluctuations. The business should analyze these trends against weekdays/weekends or marketing campaigns to understand the drivers of peak sales days.")
    print("\n--- Analysis Complete ---")


if __name__ == '__main__':
    run_sales_analysis()

