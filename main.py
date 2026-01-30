import os
from dotenv import load_dotenv
from src.extractor import SchemaExtractor
from src.brain import ScisneBrain

load_dotenv()

def run_onboarding():
    print("🦢 Welcome to Scisne: Your AI Data Analyst Onboarding")
    
    db_url = os.getenv("DATABASE_URL")
    extractor = SchemaExtractor(db_url)
    brain = ScisneBrain()
    
    tables = extractor.get_full_schema()
    
    for t in tables:
        print(f"\n--- Discovered Table: {t['table_name']} ---")
        print(f"Columns: {t['columns']}")
        
        # This is your differentiator: Human Interpretation
        context = input("What does this table represent for the business? ")
        
        brain.learn(t['table_name'], t['columns'], context)
        print("✓ Context stored in Scisne's brain.")

if __name__ == "__main__":
    run_onboarding()