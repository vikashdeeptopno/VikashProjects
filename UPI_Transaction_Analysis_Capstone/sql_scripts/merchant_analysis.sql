-- Merchant Overview

CREATE OR REPLACE VIEW merchant_overview AS
SELECT
	COUNT (DISTINCT merchant_id) AS total_merchants,
	ROUND(AVG(risk_score)::numeric, 2) AS average_risk_score
FROM merchant_info;

-- Top 10 Merchants

CREATE OR REPLACE VIEW top_10_merchants AS
SELECT
	uth.merchant_id,
	mi.merchant_name,
	mi.merchant_type,
	mi.region,
	COUNT(*) AS total_transactions,
	ROUND(SUM(amount)::numeric, 2) AS total_value,
	ROUND(AVG(amount)::numeric, 2) AS average_value
FROM upi_transaction_history AS uth
JOIN merchant_info as mi ON uth.merchant_id = mi.merchant_id
GROUP BY uth.merchant_id, mi.merchant_name,mi.merchant_type, mi.region
ORDER BY total_value DESC
LIMIT 10;

-- Merchant Category

CREATE OR REPLACE VIEW merchant_category AS
SELECT
	mi.merchant_type,
	COUNT(*) AS total_transaction,
	ROUND(SUM(amount)::numeric, 2) AS total_value,
	ROUND(AVG(amount)::numeric, 2) AS average_value
FROM upi_transaction_history AS uth
JOIN merchant_info AS mi ON mi.merchant_id = uth.merchant_id
GROUP BY merchant_type
ORDER BY total_value DESC;

-- Regional Merchant Performance

CREATE OR REPLACE VIEW regional_merchants AS
SELECT
	mi.region,
	COUNT(DISTINCT uth.merchant_id) AS active_merchants,
	COUNT(*) AS total_transactions,
	ROUND(SUM(amount):: numeric, 2) AS total_value,
	ROUND(AVG(amount):: numeric, 2) AS average_value
FROM upi_transaction_history AS uth
JOIN merchant_info AS mi ON uth.merchant_id = mi.merchant_id
GROUP BY mi.region
ORDER BY total_value DESC;

-- Merchant Failure and Fraud Analysis

CREATE OR REPLACE VIEW failure_fraud AS
SELECT
	mi.merchant_id,
	mi.merchant_name,
	mi.merchant_type,
	COUNT(*) AS total_transactions,
	SUM(CASE WHEN uth.status = 'Failed' THEN 1 ELSE 0 END) AS failed_transactions,
	SUM(CASE WHEN uth.fraud_flag = TRUE THEN 1 ELSE 0 END) AS fraud_transactions,
	ROUND(100* SUM(CASE WHEN uth.status = 'Failed' THEN 1 ELSE 0 END)/COUNT(*), 2) AS failed_rate,
	ROUND(100* SUM(CASE WHEN uth.fraud_flag = TRUE THEN 1 ELSE 0 END)/COUNT(*), 2) AS fraud_rate
FROM upi_transaction_history as uth
JOIN merchant_info AS mi ON uth.merchant_id = mi.merchant_id
GROUP BY mi.merchant_type, mi.merchant_id, mi.merchant_name
ORDER BY fraud_rate desc;

