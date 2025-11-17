import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def connect_to_db():
    username = 'root'
    actual_password = 'Vicky1990*'
    password = quote_plus(actual_password)
    host = 'localhost'
    database = 'upi_capstone'

    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")

    try:
        with engine.connect() as conn:
            print("MySQL connection successful!\n")
            result = conn.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result]
            print("Available tables:")
            for t in tables:
                print("•", t)
            return engine
    except Exception as e:
        print("Connection failed:")
        print(e)
        return None