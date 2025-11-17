
-- Rows count check for all the tables
SELECT COUNT(*)
FROM customer_feedback_surveys;

SELECT COUNT(*)
FROM customer_master;

SELECT COUNT(*)
FROM device_info;

SELECT COUNT(*)
FROM fraud_alert_history;

SELECT COUNT(*)
FROM merchant_info;

SELECT COUNT(*)
FROM upi_account_details;

SELECT COUNT(*)
FROM upi_transaction_history;


-- Check to see the relationship validity after ingestion
SELECT 
    COUNT(DISTINCT uth.upi_id) AS upi_ids_in_transactions,
    COUNT(DISTINCT uad.upi_id) AS upi_ids_in_acc_details,
    COUNT(DISTINCT uth.merchant_id) AS merchants_in_transaction,
    COUNT(DISTINCT mi.merchant_id) AS merchants_in_master,
    COUNT(DISTINCT uth.device_id) AS devices_in_transaction,
    COUNT(DISTINCT di.device_id) AS devices_in_master
FROM upi_transaction_history AS uth
LEFT JOIN upi_account_details AS uad ON uth.upi_id = uad.upi_id
LEFT JOIN merchant_info AS mi ON uth.merchant_id = mi.merchant_id
LEFT JOIN device_info AS di ON uth.device_id = di.device_id;

-- Check to see the relationship validity of customer and transaction
SELECT
	COUNT (DISTINCT uad.customer_id) AS customers_in_upi_accounts,
	COUNT (DISTINCT cm.customer_id) AS customers_in_master,
	COUNT (DISTINCT cfs.customer_id) AS customers_in_feedback,
	COUNT (DISTINCT fah.transaction_id) AS transactions_in_fraud,
	COUNT (DISTINCT uth.transaction_id) AS transactions_in_history
FROM customer_master AS cm
LEFT JOIN upi_account_details AS uad ON uad.customer_id = cm.customer_id
LEFT JOIN customer_feedback_surveys AS cfs ON cfs.customer_id = cm.customer_id
LEFT JOIN upi_transaction_history AS uth ON cm.customer_id = uth.customer_id
LEFT JOIN fraud_alert_history AS fah ON uth.transaction_id = fah.transaction_id;
