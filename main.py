
import config
from ingestion.client import StackExchangeClient
from repositories.repository import Repository
from transforms.questions import transform_questions
import sys
from pathlib import Path

from services.stackexchange_service import StackExchangeService

sys.path.append(str(Path(__file__).resolve().parent.parent))

tables = config.TABLES

def run():
    client = StackExchangeClient()
    service = StackExchangeService(client)
    repo = Repository()

    repo.create_table("questions", tables["questions"]["schema"])

    # Step 1: Fetch recent questions
    questions = service.get_recent_questions(days=config.DAYS_TO_FETCH)

    # Step 2: Transform the data
    transformed_questions = transform_questions(questions)

    # Step 3: Output the transformed data (for demonstration, we print it)
    df = transformed_questions.collect()
    repo.upsert("questions", df, tables["questions"]["primary_key"])

    print(df.head(5))

if __name__ == "__main__":
    run()