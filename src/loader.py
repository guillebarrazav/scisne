import yaml
import os

class MetadataLoader:
    """Loads business metadata and column definitions from a YAML file."""
    def __init__(self, filepath="metadata.yaml"):
        self.data = {}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f) or {}

    def get_table_context(self, table_name):
        """Returns description and column dictionary for a given table."""
        table_info = self.data.get('tables', {}).get(table_name, {})
        return table_info.get('description', ""), table_info.get('columns', {})