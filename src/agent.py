import os
import pandas as pd
from src.brain import ScisneBrain
from src.providers import SQLTranslator
from src.database import DBExecutor

class ScisneAgent:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        provider = os.getenv("AI_PROVIDER", "ollama")
        model = os.getenv("OLLAMA_MODEL", "llama3")

        self.brain = ScisneBrain()
        self.translator = SQLTranslator(provider=provider, model=model)
        self.db = DBExecutor(db_url)

    def ask(self, question):
        print(f"\n🦢 Scisne Agent processing: '{question}'")
        
        # 1. Retrieve Context
        context = self.brain.get_context(question)
        if not context:
            return "I don't have enough knowledge about your tables to answer that."
        
        # 2. Translate to SQL
        try:
            sql = self.translator.generate_sql(question, context)
            print(f"   [SQL Generated]: {sql}")
        except Exception as e:
            return f"Translation Error: {e}"

        # 3. Execute
        try:
            df = self.db.run_query(sql)
            if df.empty:
                return "Query executed successfully but returned no results."
            return df
        except Exception as e:
            return f"SQL Execution Error: {str(e)}"