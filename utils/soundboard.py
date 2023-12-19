import requests
import base64
import mimetypes

class Sound:
    def __init__(self, name, sound_id, volume, emoji_id, emoji_name, override_path, user_id, available):
        self.name = name
        self.id = sound_id
        self.volume = volume
        self.emoji_id = emoji_id
        self.emoji_name = emoji_name
        self.override_path = override_path
        self.user_id = user_id
        self.available = available

class Soundboard:
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.headers = {
            "Authorization": self.token,
            "content-type": "application/json"
        }

    @staticmethod
    def encode(sound_file):
        with open(sound_file, "rb") as sound:
            encoded = base64.b64encode(sound.read()).decode('utf-8')

        content_type = mimetypes.guess_type(sound_file)[0]
        return f"data:{content_type};base64,{encoded}"
    
    def upload_sound(self, sound_file, name, emoji_id, volume):
        endpoint = f"https://discord.com/api/v9/guilds/{self.guild_id}/soundboard-sounds"
        encoded = self.encode(sound_file)
        data = {
            "name": name,
            "emoji_id": emoji_id,
            "volume": volume,
            "sound": encoded
        }

        res = requests.post(endpoint, json=data, headers=self.headers)

        if res.status_code in [200, 201]:
            data = res.json()

            return Sound(
                name=data["name"],
                sound_id=data["sound_id"],
                volume=data["volume"],
                emoji_id=data["emoji_id"],
                emoji_name=data["emoji_name"],
                override_path=data["override_path"],
                user_id=data["user_id"],
                available=data.get("available", False)
            )
        
        else:
            return res
        
    def delete_sound(self, sound_id):
        endpoint = f"https://discord.com/api/v9/guilds/{self.guild_id}/soundboard-sounds/{sound_id}"
        res = requests.delete(endpoint, headers=self.headers)

        return True if res.status_code == 204 else False
    
    def play_sound(self, sound_id, source_guild_id = True, override_path = None):
        endpoint = f"https://discord.com/api/v9/channels/{self.channel_id}/voice-channel-effects"
        data = {"sound_id": sound_id, "source_guild_id": self.guild_id, "override_path": override_path}

        if source_guild_id == False or source_guild_id == None:
            data.pop("source_guild_id")
        if override_path == None or override_path == False:
            data.pop("override_path")

        return requests.post(endpoint, json=data, headers=self.headers)

    def get_default_sounds(self):
        endpoint = f"https://discord.com/api/v9/soundboard-default-sounds"
        res = requests.get(endpoint, headers=self.headers)
        sounds = []

        if res.status_code == 200:
            data = res.json()
            for obj in data:
                sounds.append(Sound(
                    name=obj["name"],
                    sound_id=obj["sound_id"],
                    volume=obj["volume"],
                    emoji_id=obj["emoji_id"],
                    emoji_name=obj["emoji_name"],
                    override_path=obj["override_path"],
                    user_id=obj["user_id"],
                    available=True
                ))

        return sounds
    
if __name__ == "__main__":
    soundboard = Soundboard("MTA0MjE1Mzk5ODI1OTYwNTYwNA.GF04HF.XElxlFoI5rf_hspq0wupiqHNDa4UShm-xQlXn4", "1108750276028022855", "1116797349361106964")
    sound = soundboard.upload_sound("hello.mp3", name="testing", emoji_id=None, volume=1)
    print(sound.id)