import requests
import time

class StackExchangeClient:
    BASE_URL = "https://api.stackexchange.com/2.3"

    def __init__(self, site="stackoverflow", api_key=None, max_retries=3):
        self.site = site
        self.api_key = api_key
        self.max_retries = max_retries

    def _make_request(self, endpoint, params):
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                if "backoff" in data:
                    time.sleep(data["backoff"])

                return data
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff

    def fetch_questions(self, from_date, to_date, page=1, pagesize=100):
        params = {
            "site": self.site,
            "key": self.api_key,
            "fromdate": int(from_date.timestamp()),
            "todate": int(to_date.timestamp()),
            "page": page,
            "pagesize": pagesize
            }
        return self._make_request("questions", params)

    def fetch_answers(self, from_date, to_date, page=1, pagesize=100):
        params = {
            "site": self.site,
            "key": self.api_key,
            "fromdate": int(from_date.timestamp()),
            "todate": int(to_date.timestamp()),
            "page": page,
            "pagesize": pagesize,
            "order": "asc",
            "sort": "creation"
        }
        return self._make_request("answers", params)

    def fetch_users(self, user_ids, page=1, pagesize=100):
        id_str = ";".join(map(str, user_ids))
        params = {
            "site": self.site,
            "key": self.api_key,
            "page": page,
            "pagesize": 100,
            "order": "asc",
            "sort": "reputation"
        }
        return self._make_request(f"users/{id_str}", params)
