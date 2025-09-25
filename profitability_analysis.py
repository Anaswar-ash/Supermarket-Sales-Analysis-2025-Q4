import pandas as pd

def analyze_profitability_of_large_sales():
    """
    Loads the 'large_quantity_sales.csv' file, analyzes which product line
    is the most profitable, and saves the results to a new CSV file.
    """
    print("--- Profitability Analysis of Large-Quantity Sales ---")

    # Define the input and output filenames
    input_filename = 'large_quantity_sales.csv'
    output_filename = 'profitability_of_large_sales.csv'

    try:
        # Step 1: Load the dataset of large-quantity sales
        df_large_sales = pd.read_csv(input_filename)
        print(f"Successfully loaded '{input_filename}'.")

    except FileNotFoundError:
        print(f"\nERROR: The file '{input_filename}' was not found.")
        print("Please run the main 'Supermarket_Analysis.py' script first to generate this file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return

    # Step 2: Perform the profitability analysis
    # We group by 'Product_line' and calculate the sum of 'gross_income'
    # This tells us the total profit generated from bulk purchases in each category.
    profitability = df_large_sales.groupby('Product_line')['gross_income'].sum().sort_values(ascending=False).reset_index()

    print("\nTotal profit from large-quantity sales (quantity >= 5) by product line:")
    print(profitability)

    # Step 2a: Save the analysis results to a CSV file
    profitability.to_csv(output_filename, index=False)
    print(f"\nSaved profitability analysis to '{output_filename}'.")


    # Step 3: Identify and report the most profitable product line
    # Get the first row of the sorted dataframe for the top performer
    if not profitability.empty:
        most_profitable_line = profitability.loc[0, 'Product_line']
        top_profit_value = profitability.loc[0, 'gross_income']

        print("\n--- Key Insight ---")
        print(f"The most profitable product line for bulk purchases is '{most_profitable_line}', generating a total of ${top_profit_value:,.2f} in gross income from these transactions alone.")
    else:
        print("\n--- No Data ---")
        print("No large-quantity sales data was available to analyze.")


    # Step 4: Explain the business value of this insight
    print("\nHow this helps the business:")
    print("This insight is crucial because it goes beyond just sales volume. It tells the supermarket which products are not only popular for bulk purchases but also contribute the most to the bottom line.")
    print("With this knowledge, the business can make smarter decisions, such as:")
    print("  - Creating targeted 'buy more, save more' promotions on the most profitable lines.")
    print("  - Ensuring these high-profit, high-volume items are always well-stocked.")
    print("  - Placing these items in prominent store locations to encourage more bulk sales.")
    print("\n--- Analysis Complete ---")


if __name__ == '__main__':
    analyze_profitability_of_large_sales()

