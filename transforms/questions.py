import polars as pl
from datetime import datetime


def transform_questions(questions):
    return pl.LazyFrame([
        {
            "question_id": q.get("question_id"),
            "title": q.get("title"),
            "creation_date": datetime.utcfromtimestamp(q.get("creation_date")),
            "score": q.get("score"),
            "view_count": q.get("view_count"),
            "answer_count": q.get("answer_count"),
            "accepted_answer_id": q.get("accepted_answer_id"),
            "owner_user_id": q.get("owner", {}).get("user_id"),
            "tags": q.get("tags"),
            "link": q.get("link")
        }
        for q in questions
    ])
    return df