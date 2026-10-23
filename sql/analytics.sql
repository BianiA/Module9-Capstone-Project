-- SQLite analytical queries
SELECT country, COUNT(*) AS purchases, ROUND(SUM(purchaseamount),2) AS total_amount FROM customer_purchases GROUP BY country ORDER BY total_amount DESC;
SELECT age_group, COUNT(*) AS purchases, ROUND(AVG(purchaseamount),2) AS average_amount FROM customer_purchases GROUP BY age_group;
