-- To Load the customer_master data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/customer_master.csv'
INTO TABLE customer_master
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, full_name, mobile_number, age, gender, region, @date_joined, business_user, risk_score)
SET date_joined = STR_TO_DATE(@date_joined, '%d-%m-%Y');

-- To Load the device_info data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/device_info.csv'
INTO TABLE device_info
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(device_id, customer_id, device_type, app_version, is_rooted);

-- To Load the upi_account_details data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/upi_account_details.csv'
INTO TABLE upi_account_details
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(upi_id, customer_id, bank_name, account_type, @date_added, status)
SET date_added = STR_TO_DATE(@date_added, '%Y-%m-%d');

-- To Load the merchant_info data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/merchant_info.csv'
INTO TABLE merchant_info
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(merchant_id, merchant_name, merchant_type, region, @onboard_date, risk_score)
SET onboard_date = STR_TO_DATE(@onboard_date, '%Y-%m-%d');

-- To Load customer_feedback_surveys data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/customer_feedback_surveys.csv'
INTO TABLE customer_feedback_surveys
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(feedback_id, customer_id, @date_submitted, feedback_text, satisfaction_score, issue_type, resolved)
SET date_submitted = STR_TO_DATE(@date_submitted, '%d-%m-%Y');

-- To Load the fraud_alert_history data

LOAD DATA LOCAL INFILE 'E:/Data Analytics/Projects/Capstone/UPI Transaction Analysis - Capstone/For SQL Ingestion/fraud_alert_history.csv'
INTO TABLE fraud_alert_history
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(alert_id, transaction_id, alert_type, resolved, remarks);
