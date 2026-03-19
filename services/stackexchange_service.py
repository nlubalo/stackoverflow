import time
from datetime import datetime, timedelta

class StackExchangeService:
    def __init__(self, client):
        self.client = client

    def get_recent_questions(self, days=1):
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=days)
        all_questions = []
        page = 1

        while True:
            try:
                data = self.client.fetch_questions(from_date, to_date, page=page)
                questions = data.get("items", [])
                if not questions:
                    break
                all_questions.extend(questions)
                if not data.get("has_more", False):
                    break
                page += 1
                time.sleep(0.5)  # To respect API rate limits
                if "backoff" in data:
                    time.sleep(data["backoff"])
            except Exception as e:
                print(f"Error fetching questions: {e}")
                break
        return all_questions

    def get_recent_answers(self, days=1):
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=days)
        all_answers = []
        page = 1

        while True:
            try:
                data = self.client.fetch_answers(from_date, to_date, page=page)
                answers = data.get("items", [])
                if not answers:
                    break
                all_answers.extend(answers)
                if not data.get("has_more", False):
                    break
                page += 1
                time.sleep(0.5)  # To respect API rate limits
                if "backoff" in data:
                    time.sleep(data["backoff"])
            except Exception as e:
                print(f"Error fetching answers: {e}")
                break
        return all_answers

    def get_answers_for_questions(self, questions_ids, pagesize=100):
        all_answers = []
        chunk_size = 20
        for i in range(0, len(questions_ids), chunk_size):
            chunk_ids = questions_ids[i:i + chunk_size]
            id_str = ";".join(map(str, chunk_ids))

            page = 1
            while True:
                try:
                    data = self.client._make_request(
                        endpoint=f"questions/{id_str}/answers",
                        params={
                            "site": self.client.site,
                            "key": self.client.api_key,
                            "page": page,
                            "pagesize": pagesize,
                            "order": "asc",
                            "sort": "creation",
                            "filter": "withbody"  # To get the answer body as well
                        }
                    )
                    answers = data.get("items", [])
                    if not answers:
                        break
                    all_answers.extend(answers)
                    if not data.get("has_more", False):
                        break
                    page += 1
                    time.sleep(0.5)  # To respect API rate limits
                    if "backoff" in data:
                        time.sleep(data["backoff"])
                except Exception as e:
                    print(f"Error fetching answers for questions {id_str}: {e}")
                    break
        return all_answers
    
    def get_users(self, user_ids, pagesize=100):
        all_users = []
        chunk_size = 20
        for i in range(0, len(user_ids), chunk_size):
            chunk_ids = user_ids[i:i + chunk_size]
            id_str = ";".join(map(str, chunk_ids))
        page = 1
        while True:
            try:
                data = self.client.fetch_users(chunk_ids, page=page, pagesize=pagesize)
                users = data.get("items", [])
                if not users:
                    break
                all_users.extend(users)
                if not data.get("has_more", False):
                    break
                page += 1
                time.sleep(0.5)  # To respect API rate limits
                if "backoff" in data:
                    time.sleep(data["backoff"])
            except Exception as e:
                print(f"Error fetching users {id_str}: {e}")
                break
        return all_users