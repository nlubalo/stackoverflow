
import os

from dotenv import load_dotenv

import config
from ingestion.client import StackExchangeClient
from repositories.repository import Repository
from transforms.questions import (
    transform_questions,
    transform_answers,
    transform_users,
    transform_comments_for_posts
    )
import sys
from pathlib import Path
load_dotenv()
from services.stackexchange_service import StackExchangeService

sys.path.append(str(Path(__file__).resolve().parent.parent))

tables = config.TABLES

API_KEY = os.getenv("API_KEY")
def run():
    client = StackExchangeClient(api_key=API_KEY)
    service = StackExchangeService(client)
    repo = Repository()

    repo.create_table("questions", tables["questions"]["schema"])
    repo.create_table("answers", tables["answers"]["schema"])
    repo.create_table("users", tables["users"]["schema"])
    repo.create_table("comments", tables["comments"]["schema"])

    # Step 1: Fetch recent questions
    questions = service.get_recent_questions(days=config.DAYS_TO_FETCH)
    question_ids = [q["question_id"] for q in questions]

    # Step 1.5: Fetch answers for the recent questions
    answers = service.get_answers_for_questions(question_ids)
    answer_ids = [a["answer_id"] for a in answers]
    q_comments = service.get_comments_for_posts(question_ids, post_type="questions")
    a_comments = service.get_comments_for_posts(answer_ids, post_type="answers")

    # Step 2: Transform the data
    transformed_questions = transform_questions(questions)
    transformed_answers = transform_answers(answers)
    transformed_q_comments = transform_comments_for_posts(q_comments)
    transformed_a_comments = transform_comments_for_posts(a_comments)

    transformed_q_comments_df = transformed_q_comments.collect()
    repo.upsert("comments", transformed_q_comments_df, tables["comments"]["primary_key"])
    transformed_a_comments_df = transformed_a_comments.collect()
    repo.upsert("comments", transformed_a_comments_df, tables["comments"]["primary_key"])


    # USERS
    user_ids = set()
    # from questions

    for q in questions:
        if "owner" in q and "user_id" in q["owner"]:
            user_ids.add(q["owner"]["user_id"])

    # from answers
    for a in answers:
        if "owner" in a and "user_id" in a["owner"]:
            user_ids.add(a["owner"]["user_id"])

    users = service.get_users(list(user_ids))
    users_df = transform_users(users)
    users_df  = users_df.collect()
    repo.upsert("users", users_df, tables["users"]["primary_key"])
    print(users_df.head(5))

    # Step 3: Output the transformed data (for demonstration, we print it)
    df = transformed_questions.collect()
    repo.upsert("questions", df, tables["questions"]["primary_key"])

    print(df.head(5))

    df_answers = transformed_answers.collect()
    repo.upsert("answers", df_answers, tables["answers"]["primary_key"])

    print(df_answers.head(5))

if __name__ == "__main__":
    run()