
class User():
    def __init__(self, name: str, discord_id: str) -> None:
        self._discordId: str = discord_id
        self._name: str = name
        self._mmr: int = 0
    
    def GetName(self) -> str:
        return self._name
    
    def GetMmr(self) -> int:
        return self._mmr

    def GetDiscordId(self) -> str:
        return self._discordId