from sqlalchemy import create_engine, inspect

class SchemaExtractor:
    """
    Handles database connection and schema inspection.
    Supports specific schemas for professional environments like Azure/Postgres.
    """
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.inspector = inspect(self.engine)

    def list_tables(self, target_schema=None):
        """Returns a list of table names available in the specified schema."""
        try:
            return self.inspector.get_table_names(schema=target_schema)
        except Exception as e:
            print(f"⚠️ Error listing tables in schema '{target_schema}': {e}")
            return []

    def get_schema_details(self, target_schema=None, allowed_tables=None):
        """
        Extracts column definitions for allowed tables.
        Returns a list of dictionaries with technical metadata.
        """
        schema_info = []
        all_tables = self.list_tables(target_schema)
        
        # Filter tables based on user selection
        tables_to_process = []
        if allowed_tables:
            allowed_set = set(t.lower().strip() for t in allowed_tables)
            for t in all_tables:
                if t.lower() in allowed_set:
                    tables_to_process.append(t)
        else:
            tables_to_process = all_tables

        for table in tables_to_process:
            try:
                columns = self.inspector.get_columns(table, schema=target_schema)
                # Format: "column_name (DATA_TYPE)"
                col_desc = ", ".join([f"{c['name']} ({c['type']})" for c in columns])
                
                # Standardize full name as 'schema.table'
                full_table_name = f"{target_schema}.{table}" if target_schema else table
                
                schema_info.append({
                    "table_name": full_table_name,
                    "columns": col_desc
                })
            except Exception as e:
                print(f"Skipping table {table} due to error: {e}")
            
        return schema_info