-- Coffee Shop Analytics Query Pack
-- Assumed table name: coffee_sales
-- Update table name as needed for your SQL environment.

-- 1) Total revenue
SELECT ROUND(SUM(transaction_qty * unit_price), 2) AS total_revenue
FROM coffee_sales;

-- 2) Total orders
SELECT COUNT(DISTINCT transaction_id) AS total_orders
FROM coffee_sales;

-- 3) Average order value
SELECT ROUND(
	SUM(transaction_qty * unit_price) / NULLIF(COUNT(DISTINCT transaction_id), 0),
	2
) AS average_order_value
FROM coffee_sales;

-- 4) Revenue by month
SELECT
	DATE_TRUNC('month', TO_DATE(transaction_date, 'MM/DD/YYYY')) AS month,
	ROUND(SUM(transaction_qty * unit_price), 2) AS revenue
FROM coffee_sales
GROUP BY 1
ORDER BY 1;

-- 5) Top 10 products by revenue
SELECT
	product_detail,
	ROUND(SUM(transaction_qty * unit_price), 2) AS revenue
FROM coffee_sales
GROUP BY product_detail
ORDER BY revenue DESC
LIMIT 10;

-- 6) Sales by hour
SELECT
	EXTRACT(HOUR FROM TO_TIMESTAMP(transaction_time, 'HH24:MI:SS')) AS hour,
	ROUND(SUM(transaction_qty * unit_price), 2) AS revenue
FROM coffee_sales
GROUP BY 1
ORDER BY 1;

-- 7) Revenue by day of week
SELECT
	TO_CHAR(TO_DATE(transaction_date, 'MM/DD/YYYY'), 'Day') AS day_of_week,
	ROUND(SUM(transaction_qty * unit_price), 2) AS revenue
FROM coffee_sales
GROUP BY 1
ORDER BY revenue DESC;

-- 8) Revenue by store location
SELECT
	store_location,
	ROUND(SUM(transaction_qty * unit_price), 2) AS revenue
FROM coffee_sales
GROUP BY store_location
ORDER BY revenue DESC;

