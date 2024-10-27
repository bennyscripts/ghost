import json
import requests
import base64

from . import config

def encode_image(avatar_url):
    return base64.b64encode(requests.get(avatar_url).content).decode("utf-8")

def create_webhook(channel_id, name, avatar_url = ""):
    cfg = config.Config()
    payload = {
        "name": name,
        "avatar": "data:image/jpeg;base64," + encode_image(avatar_url) if avatar_url else "",
        "channel_id": channel_id
    }

    resp = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/webhooks", headers={"Content-Type": "application/json", "Authorization": cfg.get("token")}, data=json.dumps(payload))
    return Webhook(**resp.json())

class Webhook:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.avatar = kwargs.get("avatar")
        self.channel_id = kwargs.get("channel_id")
        self.guild_id = kwargs.get("guild_id")
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.type = kwargs.get("type")
        self.token = kwargs.get("token")

        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json"
        }

    @staticmethod
    def from_url(url):
        resp = requests.get(url)
        return Webhook(**resp.json())

    def send(self, content="", embed=None, embeds=None):
        payload = {
            "content": content,
            "embeds": embeds if embeds else [embed] if embed else []
        }

        return self.session.post(self.url, headers=self.headers, data=json.dumps(payload))
    
    def edit(self, name, avatar_url = ""):
        payload = {
            "avatar": "data:image/jpeg;base64," + encode_image(avatar_url) if avatar_url else "",
            "name": name
        }

        return self.session.patch(self.url, headers=self.headers, data=json.dumps(payload))
    
if __name__ == "__main__":
    name = input("Enter the name of the webhook: ")
    channel_id = input("Enter the channel ID: ")

    webhook = create_webhook(channel_id, name)
    print(f"Webhook created: {webhook.url}")

    message = input("Enter the message to send: ")
    webhook.send(message)