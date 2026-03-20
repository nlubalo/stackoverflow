import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ensure project root is in path (do this early)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import config
from ingestion.client import StackExchangeClient
from repositories.repository import Repository
from services.stackexchange_service import StackExchangeService
from transforms.questions import (
    transform_questions,
    transform_answers,
    transform_users,
    transform_comments_for_posts,
)

# Load env variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
TABLES = config.TABLES


# -----------------------------
# Helpers
# -----------------------------
def create_tables(repo: Repository):
    for table_name, table_config in TABLES.items():
        repo.create_table(table_name, table_config["schema"])


def extract_user_ids(questions, answers):
    user_ids = set()

    for q in questions:
        if "owner" in q and "user_id" in q["owner"]:
            user_ids.add(q["owner"]["user_id"])

    for a in answers:
        if "owner" in a and "user_id" in a["owner"]:
            user_ids.add(a["owner"]["user_id"])

    return list(user_ids)


def upsert_comments(repo, comments, table_config):
    transformed = transform_comments_for_posts(comments).collect()
    repo.upsert("comments", transformed, table_config["primary_key"])


# -----------------------------
# Main pipeline
# -----------------------------
def run():
    # Init
    client = StackExchangeClient(api_key=API_KEY)
    service = StackExchangeService(client)
    repo = Repository()

    create_tables(repo)

    # -------------------------
    # Step 1: Fetch data
    # -------------------------
    questions = service.get_recent_questions(days=config.DAYS_TO_FETCH)
    question_ids = [q["question_id"] for q in questions]

    answers = service.get_answers_for_questions(question_ids)
    answer_ids = [a["answer_id"] for a in answers]

    q_comments = service.get_comments_for_posts(question_ids, post_type="questions")
    a_comments = service.get_comments_for_posts(answer_ids, post_type="answers")

    # -------------------------
    # Step 2: Transform & Load
    # -------------------------

    # Comments
    upsert_comments(repo, q_comments, TABLES["comments"])
    upsert_comments(repo, a_comments, TABLES["comments"])

    # Users
    user_ids = extract_user_ids(questions, answers)
    users = service.get_users(user_ids)

    users_df = transform_users(users).collect()
    repo.upsert("users", users_df, TABLES["users"]["primary_key"])
    print(users_df.head(5))

    # Questions
    questions_df = transform_questions(questions).collect()
    repo.upsert("questions", questions_df, TABLES["questions"]["primary_key"])
    print(questions_df.head(5))

    # Answers
    answers_df = transform_answers(answers).collect()
    repo.upsert("answers", answers_df, TABLES["answers"]["primary_key"])
    print(answers_df.head(5))


if __name__ == "__main__":
    run()