-- To Create the Master Customer Table

CREATE TABLE customer_master (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100),
    mobile_number BIGINT,
    age INT,
    gender VARCHAR(10),
    region VARCHAR(50),
    date_joined DATE,
    business_user TINYINT(1),
    risk_score DECIMAL(4,2)
);

--  To create the Device Info Table
CREATE TABLE device_info (
    device_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    device_type VARCHAR(50),
    app_version VARCHAR(20),
    is_rooted TINYINT,
    FOREIGN KEY (customer_id) REFERENCES customer_master(customer_id)
);

-- To create the UPI Account Details Table
CREATE TABLE upi_account_details (
    upi_id VARCHAR(100) PRIMARY KEY,
    customer_id VARCHAR(20),
    bank_name VARCHAR(100),
    account_type VARCHAR(50),
    date_added DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customer_master(customer_id)
);

-- To create the UPI Transaction data
CREATE TABLE upi_transaction_history (
    transaction_id VARCHAR(20) PRIMARY KEY,
    upi_id VARCHAR(100),
    customer_id VARCHAR(20),
    amount DECIMAL(12,2),
    transaction_type VARCHAR(20),
    merchant_id VARCHAR(20),
    counterparty_upi VARCHAR(100),
    status VARCHAR(20),
    device_id VARCHAR(20),
    device_type VARCHAR(50),
    channel VARCHAR(20),
    fraud_flag_fixed TINYINT,
    reversal_flag_fixed TINYINT,
    failure_reason VARCHAR(300),
    FOREIGN KEY (upi_id) REFERENCES upi_account_details(upi_id),
    FOREIGN KEY (customer_id) REFERENCES customer_master(customer_id),
    FOREIGN KEY (merchant_id) REFERENCES merchant_info(merchant_id),
    FOREIGN KEY (device_id) REFERENCES device_info(device_id)
);

-- To create Customer Feedback Table
CREATE TABLE customer_feedback_surveys (
    feedback_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    date_submitted DATE,
    feedback_text TEXT,
    satisfaction_score INT,
    issue_type VARCHAR(50),
    resolved TINYINT,
    FOREIGN KEY (customer_id) REFERENCES customer_master(customer_id)
);

-- To create Fraud Alert Table
CREATE TABLE fraud_alert_history (
    alert_id VARCHAR(20) PRIMARY KEY,
    transaction_id VARCHAR(20),
    alert_type VARCHAR(100),
    resolved TINYINT,
    remarks TEXT,
    FOREIGN KEY (transaction_id) REFERENCES upi_transaction_history(transaction_id)
);