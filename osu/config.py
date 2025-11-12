from core.config import ConfigSection, BaseConfigSection


@ConfigSection(name="osu_api")
class OsuAPIConfig(BaseConfigSection):
    client_id: str = ""
    client_secret: str = ""
    api_url: str = "https://osu.ppy.sh/api/v2"
    token_url: str = "https://osu.ppy.sh/oauth/token"
    timeout: float = 10.0
    save_session: bool = True
    session_path: str = "data/session.json"

