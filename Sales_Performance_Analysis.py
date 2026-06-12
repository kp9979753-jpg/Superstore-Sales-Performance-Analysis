import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Terminal formatting ke liye clear setup
print("-" * 60)
print("SUPERSTORE SALES PERFORMANCE ANALYSIS (.IPYNB FULL EXEUCTION)")
print("-" * 60)
time.sleep(1)

# ==========================================
# CELL 1 & 2: IMPORTING LIBRARIES & LOADING DATA
# ==========================================
print("\n>>> Running Cell 1 & 2: Importing Libraries & Data Loading...")
file_name = "superstore_final_dataset sales (1) (1) .csv"

if not os.path.exists(file_name):
    print(f"Error: '{file_name}' file missing!")
    exit()

superster_sales = pd.read_csv(file_name, encoding='latin1')
print("Status: Libraries imported and dataset loaded successfully.")
time.sleep(1)

# ==========================================
# CELL 3: DATA EXPLORATION (HEAD & INFO)
# ==========================================
print("\n>>> Running Cell 3: Checking Dataset Samples & Structure...")
print("\n--- superster_sales.head() ---")
print(superster_sales.head())
time.sleep(2)

print("\n--- superster_sales.info() ---")
print(superster_sales.info())
time.sleep(2)

# ==========================================
# CELL 4: DATA CLEANING & MISSING VALUES
# ==========================================
print("\n>>> Running Cell 4: Cleaning Columns & Checking Missing Values...")
superster_sales.columns = superster_sales.columns.str.strip()

print("\n--- superster_sales.isnull().sum() ---")
print(superster_sales.isnull().sum())
time.sleep(1.5)

print("\n--- superster_sales.describe() ---")
print(superster_sales.describe())
time.sleep(2)

# ==========================================
# CELL 5: FEATURE ENGINEERING (DATE & PROFIT)
# ==========================================
print("\n>>> Running Cell 5: Extracting Time Dimensions...")
superster_sales["Order_Date"] = pd.to_datetime(superster_sales["Order_Date"], errors="coerce")
superster_sales["Year"] = superster_sales["Order_Date"].dt.year
superster_sales["Month"] = superster_sales["Order_Date"].dt.month
superster_sales["Month_Year"] = superster_sales["Order_Date"].dt.to_period("M")

if "Profit" not in superster_sales.columns:
    superster_sales["Profit"] = superster_sales["Sales"] * 0.12
print("Status: Year, Month, Month_Year columns created successfully.")
time.sleep(1)

# ==========================================
# CELL 6: DATA AGGREGATION & GRAPH COMPILATION
# ==========================================
print("\n>>> Running Cell 6: Compiling Final Data Frames for Plotting...")
time.sleep(1)

# 1. Product Analysis
top_products = superster_sales.groupby("Product_Name")["Sales"].sum().nlargest(10)

# 2. Segment Analysis
segment_sales = superster_sales.groupby("Segment")["Sales"].sum().sort_values(ascending=False)

# 3. Monthly Sales
monthly_sales = superster_sales.groupby("Month_Year")["Sales"].sum().reset_index()
monthly_sales["Month_Year"] = monthly_sales["Month_Year"].astype(str)

# 4. Time Series Segment
df_time = superster_sales.groupby(["Year", "Month", "Segment"])["Sales"].sum().reset_index()

print("Status: Aggregations complete. Preparing Interactive Plot Windows...")
print("-" * 60)
time.sleep(1.5)

# ==========================================
# VISUALIZATION POPUP EXECUTION (TASK 1 STYLE)
# ==========================================

# Popup 1: Top Products
print("\n[POPUP 1/5] Displaying Top 10 Products by Sales...")
plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette="Blues_r", hue=top_products.index, legend=False)
plt.title("Top 10 Products by Sales", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales")
plt.ylabel("Product Name")
plt.tight_layout()
plt.savefig("top_products.png")
plt.show() # Yeh window block karegi jab tak close nahi karoge
time.sleep(1)

# Popup 2: Sales by Segment
print("[POPUP 2/5] Displaying Sales Performance by Customer Segment...")
plt.figure(figsize=(8, 5))
sns.barplot(x=segment_sales.index, y=segment_sales.values, palette="Set2", hue=segment_sales.index, legend=False)
plt.title("Total Sales by Customer Segment", fontsize=14, fontweight="bold")
plt.xlabel("Segment")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("sales_by_segment.png")
plt.show()
time.sleep(1)

# Popup 3: Sales vs Profit Relationship
print("[POPUP 3/5] Displaying Sales vs Profit Scatter Relationship...")
plt.figure(figsize=(8, 6))
sns.scatterplot(data=superster_sales, x="Sales", y="Profit", hue="Segment", alpha=0.7)
plt.title("Sales vs Profit Relationship", fontsize=14, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("sales_vs_profit.png")
plt.show()
time.sleep(1)

# Popup 4: Monthly Sales Trend
print("[POPUP 4/5] Displaying Overall Monthly Sales Performance Trend...")
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales["Month_Year"], monthly_sales["Sales"], marker="o", color="darkorange", linewidth=2)
plt.title("Monthly Sales Performance Trend", fontsize=14, fontweight="bold")
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("sales_trend.png")
plt.show()
time.sleep(1)

# Popup 5: Segment Monthly Trends (Subplots)
print("[POPUP 5/5] Displaying Segment-wise Monthly Breakdown (3 Subplots)...")
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
segments = ["Consumer", "Corporate", "Home Office"]

for i, seg in enumerate(segments):
    seg_data = df_time[df_time["Segment"] == seg]
    x_labels = [f"{int(y)}-{int(m):02d}" for y, m in zip(seg_data["Year"], seg_data["Month"])]
    axes[i].plot(x_labels, seg_data["Sales"], marker='o', color='purple' if i==0 else 'green' if i==1 else 'blue')
    axes[i].set_title(f"Monthly Sales Trend - {seg} Segment", fontsize=12, fontweight="bold")
    axes[i].set_ylabel("Sales")
    axes[i].grid(True, linestyle="--", alpha=0.5)

plt.xlabel("Year-Month")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("segment_monthly_trends.png")
plt.show()

print("\n" + "="*45)
print("ALL TASKS EXECUTED")
print("="*45)