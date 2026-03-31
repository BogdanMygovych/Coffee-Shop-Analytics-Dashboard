"""Coffee Shop Sales Portfolio Analysis.

This script is designed for a data analyst portfolio project. It:
1) Loads and inspects coffee sales data
2) Cleans duplicate and missing records
3) Creates business-ready features (revenue, month, hour, day of week)
4) Performs key exploratory analysis
5) Builds polished charts
6) Saves cleaned data and visual outputs

Run from the project root:
    python scripts/coffee_shop_analysis.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def normalize_name(name: str) -> str:
    """Normalize a column name for flexible matching."""
    return "".join(ch for ch in name.lower() if ch.isalnum())


def find_column(df: pd.DataFrame, candidates: list[str]) -> str:
    """Find the first matching column from candidate names.

    This helps handle slightly different source column names.
    """
    normalized_map = {normalize_name(col): col for col in df.columns}
    for candidate in candidates:
        key = normalize_name(candidate)
        if key in normalized_map:
            return normalized_map[key]
    raise KeyError(f"Could not find any of these columns: {candidates}")


def print_section(title: str) -> None:
    """Print a consistent section header for terminal output."""
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def format_currency(value: float) -> str:
    """Format float as currency string."""
    return f"${value:,.2f}"


def build_visualizations(
    revenue_by_month: pd.DataFrame,
    top_10_products: pd.DataFrame,
    sales_by_hour: pd.DataFrame,
    product_col: str,
    charts_path: Path,
    total_revenue: float,
    total_orders: int,
    average_order_value: float,
) -> Path:
    """Create and save portfolio-ready charts."""
    plt.rcParams.update({"font.size": 11})
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(11.2, 12.0))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.65, 1.1, 1.6], hspace=0.30, wspace=0.22)

    ax_kpi = fig.add_subplot(gs[0, :])
    ax_month = fig.add_subplot(gs[1, 0])
    ax_hour = fig.add_subplot(gs[1, 1])
    ax_products = fig.add_subplot(gs[2, :])

    fig.suptitle("Coffee Shop Sales Dashboard", fontsize=17, fontweight="bold", y=0.985)

    # Top KPI row for fast executive summary
    ax_kpi.axis("off")
    kpi_style = {
        "bbox": {
            "boxstyle": "round,pad=0.45",
            "facecolor": "#f7f7f7",
            "edgecolor": "#d9d9d9",
        },
        "fontsize": 11,
        "fontweight": "bold",
        "va": "center",
        "ha": "center",
    }
    ax_kpi.text(0.17, 0.5, f"Total Revenue\n{format_currency(total_revenue)}", **kpi_style)
    ax_kpi.text(0.50, 0.5, f"Total Orders\n{total_orders:,}", **kpi_style)
    ax_kpi.text(0.83, 0.5, f"Avg Order Value\n{format_currency(average_order_value)}", **kpi_style)

    currency_fmt = FuncFormatter(lambda x, _: f"${x:,.0f}")

    # Chart 1: Revenue over time (true month-level aggregation)
    month_labels = pd.to_datetime(revenue_by_month["month"], errors="coerce").dt.strftime("%b %Y")
    if month_labels.isna().all():
        month_labels = revenue_by_month["month"]

    ax_month.plot(
        month_labels,
        revenue_by_month["revenue"],
        marker="o",
        linewidth=2.2,
        color="#2C6E91",
    )
    ax_month.set_title("Monthly Revenue Trend", fontsize=12, fontweight="bold", pad=8)
    ax_month.set_xlabel("Month")
    ax_month.set_ylabel("Revenue")
    ax_month.yaxis.set_major_formatter(currency_fmt)
    ax_month.tick_params(axis="x", rotation=0, labelsize=10)

    # Chart 2: Sales by hour
    sns.barplot(data=sales_by_hour, x="hour", y="revenue", color="#C97B63", ax=ax_hour)
    ax_hour.set_title("Sales by Hour", fontsize=12, fontweight="bold", pad=8)
    ax_hour.set_xlabel("Hour of Day")
    ax_hour.set_ylabel("Revenue")
    ax_hour.yaxis.set_major_formatter(currency_fmt)
    ax_hour.tick_params(axis="x", labelsize=10)

    # Chart 3: Top products by revenue
    top_10_sorted = top_10_products.sort_values("revenue", ascending=True)
    sns.barplot(data=top_10_sorted, x="revenue", y=product_col, color="#3F8F87", ax=ax_products)
    ax_products.set_title("Top 10 Products by Revenue", fontsize=12, fontweight="bold", pad=8)
    ax_products.set_xlabel("Revenue")
    ax_products.set_ylabel("Product")
    ax_products.xaxis.set_major_formatter(currency_fmt)
    ax_products.tick_params(axis="y", labelsize=10, pad=2)

    output_file = charts_path / "coffee_shop_dashboard.png"
    fig.subplots_adjust(top=0.93, left=0.20, right=0.98, bottom=0.06)
    fig.savefig(output_file, dpi=150, bbox_inches="tight", pad_inches=0.25)
    plt.show()

    # Also export individual chart files for reporting and presentations.
    month_trend_path = charts_path / "revenue_over_time.png"
    sales_hour_path = charts_path / "sales_by_hour.png"
    top_products_path = charts_path / "top_products_by_revenue.png"

    fig_month, ax_m = plt.subplots(figsize=(11, 5))
    ax_m.plot(month_labels, revenue_by_month["revenue"], marker="o", linewidth=2.2, color="#2C6E91")
    ax_m.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    ax_m.set_xlabel("Month")
    ax_m.set_ylabel("Revenue")
    ax_m.yaxis.set_major_formatter(currency_fmt)
    fig_month.tight_layout()
    fig_month.savefig(month_trend_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig_month)

    fig_hour, ax_h = plt.subplots(figsize=(11, 5))
    sns.barplot(data=sales_by_hour, x="hour", y="revenue", color="#C97B63", ax=ax_h)
    ax_h.set_title("Sales by Hour", fontsize=14, fontweight="bold")
    ax_h.set_xlabel("Hour of Day")
    ax_h.set_ylabel("Revenue")
    ax_h.yaxis.set_major_formatter(currency_fmt)
    fig_hour.tight_layout()
    fig_hour.savefig(sales_hour_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig_hour)

    fig_products, ax_p = plt.subplots(figsize=(11, 6))
    sns.barplot(data=top_10_sorted, x="revenue", y=product_col, color="#3F8F87", ax=ax_p)
    ax_p.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
    ax_p.set_xlabel("Revenue")
    ax_p.set_ylabel("Product")
    ax_p.xaxis.set_major_formatter(currency_fmt)
    fig_products.tight_layout()
    fig_products.savefig(top_products_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig_products)

    return output_file


def main() -> None:
    # Paths
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "data" / "coffee_shop_sales_transactions.csv"
    output_path = project_root / "data" / "coffee_shop_sales_enriched.csv"
    charts_path = project_root / "outputs" / "charts"
    charts_path.mkdir(parents=True, exist_ok=True)

    # 1) Load dataset and display first rows, columns, and dtypes
    df = pd.read_csv(input_path)

    print_section("Dataset Preview")
    print(df.head())

    print_section("Column Names")
    print(df.columns.tolist())

    print_section("Data Types")
    print(df.dtypes)

    # Resolve important columns safely (for slight naming differences)
    qty_col = find_column(df, ["transaction_qty", "quantity", "qty"])
    price_col = find_column(df, ["unit_price", "price"])
    date_col = find_column(df, ["transaction_date", "date", "order_date"])
    time_col = find_column(df, ["transaction_time", "time", "order_time"])
    product_col = find_column(df, ["product_detail", "product", "product_name"])
    order_id_col = find_column(df, ["transaction_id", "order_id", "id"])

    # 2) Clean dataset
    before_rows = len(df)
    df = df.drop_duplicates()
    after_dedup_rows = len(df)

    df = df.dropna()
    after_dropna_rows = len(df)

    print_section("Cleaning Summary")
    print(f"Rows before cleaning: {before_rows}")
    print(f"Rows after removing duplicates: {after_dedup_rows}")
    print(f"Rows after dropping missing values: {after_dropna_rows}")

    # 3) Create new columns
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # Parse time reliably; fallback keeps script robust to slight format variations.
    parsed_time = pd.to_datetime(df[time_col], format="%H:%M:%S", errors="coerce")
    if parsed_time.isna().any():
        parsed_time = pd.to_datetime(df[time_col], errors="coerce")
    df = df.loc[parsed_time.notna()].copy()
    parsed_time = parsed_time.loc[parsed_time.notna()]
    df[time_col] = parsed_time.dt.time

    df["revenue"] = df[qty_col] * df[price_col]
    df["month"] = df[date_col].dt.to_period("M")
    df["hour"] = parsed_time.dt.hour
    df["day_of_week"] = df[date_col].dt.day_name()

    # 4) Exploratory data analysis
    total_revenue = df["revenue"].sum()
    total_orders = df[order_id_col].nunique()
    average_order_value = total_revenue / total_orders if total_orders else 0

    revenue_by_month = df.groupby("month", as_index=False)["revenue"].sum()
    revenue_by_month = revenue_by_month.sort_values("month")
    revenue_by_month["month"] = revenue_by_month["month"].dt.to_timestamp()

    top_10_products = (
        df.groupby(product_col, as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )
    sales_by_hour = df.groupby("hour", as_index=False)["revenue"].sum().sort_values("hour")

    print_section("EDA Metrics")
    print(f"Total Revenue: {format_currency(total_revenue)}")
    print(f"Total Orders: {total_orders:,}")
    print(f"Average Order Value: {format_currency(average_order_value)}")

    print_section("Revenue by Month")
    print(revenue_by_month)

    print_section("Top 10 Products by Revenue")
    print(top_10_products)

    print_section("Sales by Hour")
    print(sales_by_hour)

    # 5) Visualizations
    dashboard_path = build_visualizations(
        revenue_by_month=revenue_by_month,
        top_10_products=top_10_products,
        sales_by_hour=sales_by_hour,
        product_col=product_col,
        charts_path=charts_path,
        total_revenue=total_revenue,
        total_orders=total_orders,
        average_order_value=average_order_value,
    )

    # 6) Save cleaned dataset
    df["month"] = df["month"].astype(str)
    df.to_csv(output_path, index=False)
    print_section("Saved Outputs")
    print(f"Cleaned dataset: {output_path}")
    print(f"Dashboard chart: {dashboard_path}")


if __name__ == "__main__":
    main()
