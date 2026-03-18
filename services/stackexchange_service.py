import time
from datetime import datetime, timedelta

class StackExchangeService:
    def __init__(self, client):
        self.client = client

    def get_recent_questions(self, days=30):
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