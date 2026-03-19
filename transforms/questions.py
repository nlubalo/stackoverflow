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

def transform_answers(answers):
    return pl.LazyFrame([
        {
            "answer_id": a.get("answer_id"),
            "question_id": a.get("question_id"),
            "creation_date": datetime.utcfromtimestamp(a.get("creation_date")),
            "score": a.get("score"),
            "is_accepted": a.get("is_accepted"),
            "owner_user_id": a.get("owner", {}).get("user_id"),
            "link": a.get("link")
        }
        for a in answers
    ])


def transform_users(users):
    return pl.LazyFrame([
        {
            "user_id": u.get("user_id"),
            "display_name": u.get("display_name"),
            "reputation": u.get("reputation"),
            "profile_image": u.get("profile_image"),
        }
        for u in users
    ])

def transform_comments_for_posts(comments):
    return pl.LazyFrame([
        {
            "comment_id": c.get("comment_id"),
            "post_id": c.get("post_id"),
            "post_type": c.get("post_type"),
            "creation_date": datetime.utcfromtimestamp(c.get("creation_date")),
            "score": c.get("score"),
            "owner_user_id": c.get("owner", {}).get("user_id")
        }
        for c in comments
    ])