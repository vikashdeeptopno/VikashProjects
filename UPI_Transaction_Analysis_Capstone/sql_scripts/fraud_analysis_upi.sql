-- Fraud Summary

CREATE OR REPLACE VIEW fraud_summary AS
SELECT
	COUNT(*) AS total_fraud_alerts,
	COUNT(DISTINCT transaction_id) AS unique_fraud_transactions
FROM fraud_alert_history;

-- Fraud by Merchant

CREATE OR REPLACE VIEW fraud_by_merchant AS
SELECT
    mi.merchant_id,
    mi.merchant_name,
    mi.merchant_type,
    mi.region,
    COUNT(fah.transaction_id) AS total_frauds
FROM fraud_alert_history AS fah
JOIN upi_transaction_history AS uth ON fah.transaction_id = uth.transaction_id
JOIN merchant_info AS mi ON uth.merchant_id = mi.merchant_id
WHERE uth.merchant_id IS NOT NULL
GROUP BY mi.merchant_id, mi.merchant_name, mi.merchant_type
ORDER BY total_frauds DESC;


-- Fraud Distribution by region

CREATE OR REPLACE VIEW fraud_by_region AS
SELECT
	mi.region,
	COUNT(fah.transaction_id) AS frauds,
	ROUND(100*COUNT(fah.transaction_id)/SUM(COUNT(fah.transaction_id))OVER(), 2) AS fraud_rate
FROM fraud_alert_history AS fah
JOIN upi_transaction_history AS uth ON fah.transaction_id = uth.transaction_id
JOIN merchant_info AS mi ON uth.merchant_id = mi.merchant_id
GROUP BY mi.region
ORDER BY frauds desc;

-- Fraud by Transaction type

CREATE OR REPLACE VIEW txn_type AS
SELECT
	uth.transaction_type,
	COUNT(fah.transaction_id) AS frauds,
	ROUND(100*COUNT(fah.transaction_id)/SUM(COUNT(fah.transaction_id))OVER(), 2) AS fraud_rate
FROM fraud_alert_history AS fah
JOIN upi_transaction_history AS uth ON fah.transaction_id = uth.transaction_id
GROUP BY transaction_type
ORDER BY frauds desc;

-- Correlation of fraud rate and Merchant Risk Score

CREATE OR REPLACE VIEW correlation AS
SELECT
	mi.merchant_id,
	mi. merchant_name,
	mi.merchant_type,
	mi.region,
	ROUND(AVG(mi.risk_score)::numeric, 2) AS average_risk_score,
	COUNT(fah.transaction_id) AS frauds,
	ROUND(100*COUNT(fah.transaction_id)/ SUM(COUNT(uth.transaction_id)) OVER(), 2) AS fraud_rate
FROM upi_transaction_history AS uth
JOIN merchant_info AS mi ON mi.merchant_id = uth.merchant_id
LEFT JOIN fraud_alert_history AS fah ON fah.transaction_id = uth.transaction_id
GROUP BY mi.merchant_id, mi.merchant_name, mi.merchant_type, mi.region
ORDER BY fraud_rate desc;