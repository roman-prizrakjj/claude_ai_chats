import requests
import json
import uuid


class Botio:

    def __init__(self, cookie):
        self.cookie = cookie
        self.organization_uuid = self.get_organization_uuid()

    def get_organization_uuid(self):
        url = "https://claude.ai/api/organizations"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': self.cookie
        }

        response = requests.request("GET", url, headers=headers)
        res = json.loads(response.text)
        return res[0]['uuid']

    def get_chats(self):
        url = f"https://claude.ai/api/organizations/{self.organization_uuid}/chat_conversations"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': self.cookie
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def send_message(self, prompt, conversation_id):
        url = "https://claude.ai/api/append_message"

        payload = json.dumps({
            "completion": {
                "prompt": prompt,
                "timezone": "Asia/Kolkata",
                "model": "claude-2"
            },
            "organization_uuid": self.organization_uuid,
            "conversation_uuid": conversation_id,
            "text": prompt,
        })

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/event-stream, text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        response = requests.post(url, headers=headers, data=payload, stream=True)

        decoded_data = response.content.decode("utf-8")
        data = (decoded_data.strip().split('\n')[-3])
        answer = {"answer": json.loads(data[6:])['completion']}['answer']
        return answer

    def create_chats(self):
        url = f"https://claude.ai/api/organizations/{self.organization_uuid}/chat_conversations"
        uuid1 = self.generate_uuid()

        payload = json.dumps({"uuid": uuid1, "name": ""})
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return "чат создан" if response.status_code == 201 else response.status_code

    def create_uuid(self):
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        formatted_uuid = f"{random_uuid_str[0:8]}-{random_uuid_str[8:12]}-{random_uuid_str[12:16]}-{random_uuid_str[16:20]}-{random_uuid_str[20:]}"
        return formatted_uuid