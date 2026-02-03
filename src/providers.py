import ollama
import re

class SQLTranslator:
    """
    The bridge between natural language and SQL using local LLMs via Ollama.
    Focuses on strict SQL generation based on indexed metadata.
    """
    
    def __init__(self, provider="ollama", model="llama3"):
        self.model = model

    def generate_sql(self, question, context):
        """
        Constructs the prompt and extracts the SQL from the local model.
        """
        system_prompt = (
            "You are a PostgreSQL expert. Convert the user's question into a valid SQL query "
            "using ONLY the provided context.\n\n"
            "RULES:\n"
            "1. Output ONLY raw SQL. No Markdown, no backticks, no explanations.\n"
            "2. Always use fully qualified table names (e.g., schema.table).\n"
            "3. Use appropriate column names based on the definitions provided.\n"
            "4. If context is insufficient, return: SELECT 'Insufficient context';"
        )

        user_content = f"DATABASE CONTEXT:\n{context}\n\nUSER QUESTION: {question}"

        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_content}
            ])
            
            raw_sql = response['message']['content']
            return self._clean_sql(raw_sql)
            
        except Exception as e:
            return f"-- AI Error: {str(e)}"

    def _clean_sql(self, text):
        """
        Removes Markdown formatting or unwanted conversational text from LLM output.
        Uses regular expressions to find content between ```sql ... ``` blocks.
        """
        # Search for SQL blocks specifically
        pattern = r"```sql(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            # If found, take only the code inside the block
            text = match.group(1)
        
        # Final cleanup: remove generic backticks and whitespace
        return text.replace("```", "").strip()