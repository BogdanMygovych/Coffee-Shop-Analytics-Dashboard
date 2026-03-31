# Coffee Shop Analytics

Data analysis project on coffee shop transactions using Python and SQL.

## Overview

This project cleans transaction-level sales data, engineers analysis fields, and produces KPI summaries and dashboard-ready outputs.

## Dataset

- Source file: data/coffee_shop_sales_transactions.csv
- Processed file: data/coffee_shop_sales_enriched.csv
- Grain: one row per transaction
- Current size: 149,116 transactions

## What This Project Does

- Removes duplicate rows
- Removes rows with missing values
- Creates derived columns: revenue, month, hour, day_of_week
- Calculates KPI metrics: total revenue, total orders, average order value
- Builds analysis views: revenue by month, top products by revenue, sales by hour

## Outputs

- Dashboard image: outputs/charts/coffee_shop_dashboard.png
- Individual charts:
- outputs/charts/revenue_over_time.png
- outputs/charts/sales_by_hour.png
- outputs/charts/top_products_by_revenue.png
- Enriched dataset: data/coffee_shop_sales_enriched.csv
- SQL query pack: sql/queries.sql

## Key Insights

- Peak sales occur between 8–10 AM and 2–3 PM
- Top 5 products generate a significant portion of total revenue
- Revenue shows steady growth over time, indicating increasing demand

## Project Structure

- scripts/coffee_shop_analysis.py
- data/coffee_shop_sales_transactions.csv
- data/coffee_shop_sales_enriched.csv
- outputs/charts/coffee_shop_dashboard.png
- sql/queries.sql
- notebooks/analysis.ipynb

## Tech Stack

- Python
- Pandas
- Matplotlib
- Seaborn
- SQL

## Reproducibility

Install dependencies:

```bash
pip install -r requirements.txt
```

Run analysis pipeline:

```bash
python scripts/coffee_shop_analysis.py
```

## SQL Queries

Analysis queries are available in sql/queries.sql, including:

- Total revenue and average order value
- Revenue by month
- Top products by revenue
- Sales by hour and day of week

## Tableau

Use data/coffee_shop_sales_enriched.csv as the Tableau source file.

Recommended dashboard sections:

- KPI cards: Total Revenue, Total Orders, Average Order Value
- Revenue by Month
- Sales by Hour
- Top 10 Products by Revenue

