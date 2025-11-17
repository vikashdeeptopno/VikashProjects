-- Device Type

CREATE OR REPLACE VIEW device_type_summary AS
SELECT
	di.device_type,
	COUNT(uth.transaction_id) AS total_transactions,
	ROUND(SUM(uth.amount)::numeric, 2) AS total_value
FROM upi_transaction_history AS uth
JOIN device_info AS di ON uth.device_id = di.device_id
GROUP BY di.device_type
ORDER BY total_transactions desc;

-- Device Overview

CREATE OR REPLACE VIEW device_overview AS
SELECT
	di.device_type,
	COUNT(*) AS total_transactions,
	SUM(CASE WHEN uth.status = 'success' THEN 1 ELSE 0 END) AS successful_transactions,
	SUM(CASE WHEN uth.status = 'failed' THEN 1 ELSE 0 END) AS failed_transactions,
	SUM(CASE WHEN fah.transaction_id IS NOT NULL THEN 1 ELSE 0 END) AS fraud_transactions,
	ROUND(100* SUM(CASE WHEN uth.status = 'success' THEN 1 ELSE 0 END)/ COUNT(*), 2) AS success_rate,
	ROUND(100* SUM(CASE WHEN uth.status = 'failed' THEN 1 ELSE 0 END)/ COUNT(*), 2 )AS failure_rate,
	ROUND(100* SUM(CASE WHEN fah.transaction_id IS NOT NULL THEN 1 ELSE 0 END)/ COUNT(*), 2) AS fraud_rate
FROM upi_transaction_history AS uth
LEFT JOIN fraud_alert_history AS fah ON uth.transaction_id = fah.transaction_id
JOIN device_info AS di ON uth.device_id = di.device_id
GROUP BY di.device_type
ORDER BY total_transactions desc;
	