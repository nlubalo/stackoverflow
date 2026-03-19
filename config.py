DATA_PATH ="data/questions.parquet"
DAYS_TO_FETCH = 1

TABLES = {
    "questions": {
        "schema": """
            question_id INTEGER,
            title TEXT,
            creation_date TIMESTAMP,
            score INTEGER,
            view_count INTEGER,
            answer_count INTEGER,
            accepted_answer_id INTEGER,
            owner_user_id INTEGER,
            tags TEXT[],
            link TEXT
        """,
        "primary_key": "question_id"
    },
    "answers": {
        "schema": """
            answer_id INTEGER,
            question_id INTEGER,
            creation_date TIMESTAMP,
            score INTEGER,
            is_accepted BOOLEAN,
            owner_user_id INTEGER,
            link TEXT
        """,
        "primary_key": "answer_id"
    },
    "users": {
        "schema": """
            user_id INTEGER,
            display_name TEXT,
            reputation INTEGER,
            profile_image TEXT,
        """,
        "primary_key": "user_id"
    }
}