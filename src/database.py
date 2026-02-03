import pandas as pd
from sqlalchemy import create_engine, text

class DBExecutor:
    """Handles secure, read-only SQL execution."""
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def run_query(self, sql_query):
        """Executes query and returns results in a Pandas DataFrame."""
        try:
            with self.engine.connect() as connection:
                return pd.read_sql_query(text(sql_query), connection)
        except Exception as e:
            raise Exception(f"DB Execution error: {str(e)}")