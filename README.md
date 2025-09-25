# Supermarket-Sales-Analysis-2025-Q4
Supermarket Sales Analysis with Kaggle dataset
Author: Ash.
Supermarket Sales Analysis Project
1. Project Overview
This project conducts a comprehensive analysis of a supermarket's sales data to uncover trends, identify top-performing product categories, and provide actionable insights for business growth. The primary goal is to answer key business questions such as:

Which product lines generate the most revenue?

What are the sales trends over time?

How do different customer segments or store branches perform?

This analysis helps management make data-driven decisions regarding inventory, marketing strategies, and resource allocation.

2. How to Run
Step 2.1: Prerequisites
Python 3.7+

A Kaggle Account

Install the required Python libraries using pip:

pip install pandas matplotlib seaborn kagglehub

Step 2.2: IMPORTANT - Kaggle Authentication
Before running the script, you must authenticate your machine with your Kaggle account.

Log in to Kaggle: Go to www.kaggle.com.

Go to Your Account Settings: Click on your profile picture in the top-right corner and select "Account".

Create New API Token: Scroll down to the "API" section and click the "Create New API Token" button. This will download a file named kaggle.json.

Place the Token:

Windows: Move the kaggle.json file to C:\Users\<Your-Username>\.kaggle\. You may need to create the .kaggle folder if it doesn't exist.

Mac/Linux: Move the file to ~/.kaggle/.

The script will not work without this file in the correct location.

Step 2.3: Execution
Once you have installed the libraries and configured your Kaggle token, run the analysis from your terminal:

python Supermarket_Analysis.py

The script will now download the data automatically, print the analysis results, save two new CSV files, and display two charts.

3. Summary of Findings
Top Revenue Categories: The "Food and beverages" and "Sports and travel" product lines are the highest contributors to total revenue.

Sales Volume vs. Revenue: "Electronic accessories" sell in high quantities but generate lower total revenue, suggesting a lower average price per item.

Sales Trend: There is a noticeable fluctuation in daily revenue, with peaks and troughs that could correspond to specific days of the week or promotional events.

4. Dataset Details
Source Handle: faresashraf1001/supermarket-sales

Columns: 17 (Invoice ID, Branch, City, Customer Type, etc.)