# Credit: verticalsync 
# Github: https://github.com/verticalsync
# Discord: verticalsync.
# I have slightly modified the code to add different devices.

from discord.gateway import DiscordWebSocket

properties = {
    "mobile": ["iOS", "Discord iOS", "iOS"],
    "desktop": ["Windows", "Discord Client", "Windows"],
    "web": ["Windows", "Chrome", "Windows"],
    "embedded": ["Xbox", "Discord Embedded", "Xbox"],
}
original_method = None
os = "mobile"

async def new_method(self):
    if original_method is None:
        return await self._identify()
    
    self._super_properties["$os"] = properties[os][0]
    self._super_properties["$browser"] = properties[os][1]
    self._super_properties["$device"] = properties[os][2]

    return await original_method(self)

def patch_identify(new_os):
    global original_method, os

    if new_os not in properties:
        os = "desktop"
    
    os = new_os
    original_method = DiscordWebSocket.identify
    DiscordWebSocket.identify = new_method