import pandas as pd

def analyze_total_sales():
    """
    Loads the 'important_sales.csv' file, calculates the total sales for each
    product line, and saves the results to a new CSV file.
    """
    print("--- Total Sales Analysis of Important Sales ---")

    # Define the input and output filenames
    input_filename = 'important_sales.csv'
    output_filename = 'total_sales_by_product_line.csv'

    try:
        # Step 1: Load the dataset of important sales
        df_important_sales = pd.read_csv(input_filename)
        print(f"Successfully loaded '{input_filename}'.")

    except FileNotFoundError:
        print(f"\nERROR: The file '{input_filename}' was not found.")
        print("Please run the main 'Supermarket_Analysis.py' script first to generate this file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return

    # Step 2: Perform the total sales analysis
    # We group by 'Product_line' and calculate the sum of the 'Total' column.
    total_sales = df_important_sales.groupby('Product_line')['Total'].sum().sort_values(ascending=False).reset_index()

    print("\nTotal sales by product line:")
    print(total_sales)

    # Step 3: Save the analysis results to a CSV file
    total_sales.to_csv(output_filename, index=False)
    print(f"\nSaved total sales analysis to '{output_filename}'.")

    # Step 4: Identify and report the top-selling product line
    if not total_sales.empty:
        top_selling_line = total_sales.loc[0, 'Product_line']
        top_sales_value = total_sales.loc[0, 'Total']

        print("\n--- Key Insight ---")
        print(f"The top-selling product line is '{top_selling_line}', generating a total of ${top_sales_value:,.2f} in sales.")
    else:
        print("\n--- No Data ---")
        print("No sales data was available to analyze.")

    # Step 5: Explain the business value of this insight
    print("\nHow this helps the business:")
    print("This analysis provides a clear, high-level view of which product categories are the primary drivers of revenue.")
    print("This information is fundamental for strategic decisions in:")
    print("  - Marketing: Allocating advertising budget to top-performing categories.")
    print("  - Inventory Management: Ensuring stock levels are sufficient for high-demand product lines.")
    print("  - Business Strategy: Identifying core strengths and potential areas for growth.")
    print("\n--- Analysis Complete ---")


if __name__ == '__main__':
    analyze_total_sales()
