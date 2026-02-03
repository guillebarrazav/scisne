import argparse
import os
import sys
from dotenv import load_dotenv
from src.extractor import SchemaExtractor
from src.brain import ScisneBrain
from src.providers import SQLTranslator
from src.database import DBExecutor
from src.loader import MetadataLoader
from tabulate import tabulate

load_dotenv()

class ScisneAgent:
    """Orchestrates Brain, Translator, and Database execution."""
    def __init__(self):
        self.brain = ScisneBrain()
        self.translator = SQLTranslator(model=os.getenv("OLLAMA_MODEL", "llama3"))
        self.db = DBExecutor(os.getenv("DATABASE_URL"))

    def ask(self, question):
        # 1. Get Context
        context = self.brain.get_context(question)
        if not context:
            return "Knowledge base is empty. Please run '--mode learn' first."

        # 2. Translate to SQL
        sql = self.translator.generate_sql(question, context)
        print(f"📝 SQL Generated: {sql}")

        # 3. Execute
        try:
            return self.db.run_query(sql)
        except Exception as e:
            return f"❌ Error: {str(e)}"

def run_onboarding(import_file=None):
    print("\n--- 🦢 SCISNE ONBOARDING MANAGER ---")
    db_url = os.getenv("DATABASE_URL")
    target_schema = os.getenv("DB_SCHEMA", "public")
    
    extractor = SchemaExtractor(db_url)
    brain = ScisneBrain()

    if import_file:
        loader = MetadataLoader(import_file)
        real_tables = extractor.list_tables(target_schema)
        
        count = 0
        for table in real_tables:
            full_name = f"{target_schema}.{table}" if target_schema else table
            desc, col_meta = loader.get_table_context(full_name)
            
            if desc or col_meta:
                details = extractor.get_schema_details(target_schema, allowed_tables=[table])
                if details:
                    brain.learn(full_name, details[0]['columns'], desc, col_meta)
                    print(f"✅ Indexed: {full_name}")
                    count += 1
        print(f"\n🎉 Successfully learned {count} tables from file.")
    else:
        # Interactive mode logic (simplified for CLI)
        print("Interactive mode: Please use '--file metadata.yaml' for bulk import.")

def run_reset():
    brain = ScisneBrain()
    if input("⚠️ Wipe memory? Type 'DELETE': ") == "DELETE":
        brain.reset_memory()
        print("🗑️ Memory cleared.")

def run_query(q):
    agent = ScisneAgent()
    result = agent.ask(q)
    if isinstance(result, str):
        print(f"\n💬 {result}")
    else:
        print(tabulate(result, headers='keys', tablefmt='psql', showindex=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scisne AI Data Analyst")
    parser.add_argument('--mode', choices=['learn', 'ask', 'reset'], required=True)
    parser.add_argument('--q', type=str, help="Question for the agent")
    parser.add_argument('--file', type=str, help="Metadata YAML file path")

    args = parser.parse_args()
    if args.mode == 'learn': run_onboarding(args.file)
    elif args.mode == 'ask': run_query(args.q)
    elif args.mode == 'reset': run_reset()