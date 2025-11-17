-- Total transaction, Total value, Average transaction value

CREATE OR REPLACE VIEW transaction_summary AS
SELECT
	COUNT(*) AS total_transaction,
	ROUND(SUM(amount)::numeric,2) AS total_transaction_amount,
	ROUND(AVG(amount)::numeric,2) AS average_transaction_value
FROM upi_transaction_history;


-- Transaction Status

CREATE OR REPLACE VIEW status_summary AS
SELECT
	status AS transaction_status,
	COUNT(*) AS transaction_count,
	ROUND(100 * COUNT(*)/SUM(COUNT(*))OVER(), 2) AS percentage
FROM upi_transaction_history
GROUP BY status
ORDER BY transaction_count desc;

-- Transaction Types

CREATE OR REPLACE VIEW transaction_type_summary AS
SELECT
	transaction_type,
	COUNT (*) AS transaction_count,
	ROUND(100* COUNT (*)/SUM(COUNT(*)) OVER (), 2) AS percentage
FROM upi_transaction_history
GROUP BY transaction_type
ORDER BY transaction_count desc;

-- Channel Usage

CREATE OR REPLACE VIEW channel_summary AS
SELECT
	channel,
	COUNT (*) AS transaction_count,
	ROUND(AVG(amount):: numeric, 2) AS average_transaction_value
FROM upi_transaction_history
GROUP BY channel
ORDER BY transaction_count desc;

-- Monthly UPI account additions

CREATE OR REPLACE VIEW new_accounts_trend AS
SELECT
	DATE_TRUNC('month', date_added):: date AS month,
	COUNT (*) AS new_upi_accounts
FROM upi_account_details
GROUP BY 1
ORDER BY month;

