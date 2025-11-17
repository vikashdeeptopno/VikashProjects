import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Database connection details

def load_the_data():
    username = 'root'
    actual_password = 'Vicky1990*'
    password = quote_plus(actual_password)
    host = 'localhost'
    database = 'upi_capstone'

# Engine Creation

    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")

# Creating a List for all the Tables

    tables = [
        'customer_master',
        'device_info',
        'upi_account_details',
        'merchant_info',
        'upi_transaction_history',
        'customer_feedback_surveys',
        'fraud_alert_history'
    ]

# Dictionary to hold the DataFrames
    dfs = {}
    print(" Loading data from MySQL into pandas...\n")

    for table in tables:
        dfs[table] = pd.read_sql(f"SELECT * FROM {table}", con=engine) # Loading the Tables into the DataFrames
        print(f"{table}: {len(dfs[table])} rows loaded")

    print("\n All tables successfully loaded into pandas DataFrames!")

# To display the first few rows of the DataFrames
    print("\nSample from customer_master:")
    print(dfs['customer_master'].head())
    return dfs