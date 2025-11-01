import json
import os.path
import time

import requests

from core.logger import get_logger
from osu.data import User, Beatmap
from osu.errors import OsuAPIAuthError
from osu.utils import format_token_expiry

logger = get_logger(__name__)


class OsuAPI:
    """
    OsuAPI is a wrapper around the osu! API.
    """
    OSU_URL = "https://osu.ppy.sh/"
    BASE_URL = "https://osu.ppy.sh/api/v2"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"
    SESSION_PATH = "data/session.json"

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the API wrapper.
        :param client_id: OAuth2 ID obtained from the osu API website.
        :param client_secret: OAuth2 client secret obtained from the osu API website.
        """
        if client_id is None or client_secret is None:
            raise ValueError("client_id and client_secret are required")

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: str | None = None
        self.token_expires_at: float = -1.0

        logger.info("OsuAPI initialized")

    def authenticate(self) -> None:
        """
        Authenticates with the osu API using the client credentials.

        This method requests an access token and stores it in memory.
        Automatically sets an expiration timestamp based on `expires_in`.

        Can raise OsuAPIAuthError if an error occurs.
        """
        if self.is_session_alive():
            logger.warning("Tried to authenticate against an existing session")
            logger.info(format_token_expiry(self.token_expires_at))
            return

        if self._recover_session():
            logger.info("Recovered OsuAPI session")
            logger.info(format_token_expiry(self.token_expires_at))
            return

        self._create_session()
        logger.info(format_token_expiry(self.token_expires_at))

    def _create_session(self):
        logger.info("OsuAPI creating session...")
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }

        try:
            response = requests.request("POST", OsuAPI.TOKEN_URL, data=data, timeout=10)
        except requests.RequestException as e:
            raise OsuAPIAuthError(f"Network error during authentication: {e}")

        if response.status_code != 200:
            raise OsuAPIAuthError(f"OsuAPI authentication failed: {response.text}")

        session = response.json()
        self.access_token = session["access_token"]
        self.token_expires_at = time.time() + session["expires_in"]

        self._save_session(OsuAPI.SESSION_PATH)

        logger.info("OsuAPI authenticated")

    def _recover_session(self) -> bool:
        """
        Tries to recover an OsuAPI session.
        Recovers when there's an active session file `SESSION_PATH`
        :return: True when session is recovered else False
        """
        if not os.path.exists(OsuAPI.SESSION_PATH):
            return False  # there is no session

        try:
            with open(OsuAPI.SESSION_PATH) as f:
                session = json.load(f)

                self.client_id = session["client_id"]
                self.access_token = session["token"]
                self.token_expires_at = session["expires_at"]

                if time.time() >= self.token_expires_at:
                    logger.info("OsuAPI session expired")
                    return False  # session is expired

                return True
        except Exception as e:
            logger.warning(f"Recover error: {e}")
            return False  # encountered error while recovering session

    def is_session_alive(self) -> bool:
        """
        Session is alive when there is an access token and is not expired
        :return: Is session alive
        """
        return self.access_token and time.time() < self.token_expires_at

    def _ensure_token(self) -> None:
        """
        Refreshes token if expired
        """
        if not self.is_session_alive():
            self.authenticate()

    # god written deep human intelligence error
    def _get(self, endpoint: str, sure=False):
        if endpoint.startswith('/') and not sure:
            raise RuntimeError("Are you sure?")
        self._ensure_token()
        # REQUEST
        url = f"{OsuAPI.BASE_URL}/{endpoint}"
        payload = {}
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise RuntimeError(f"OsuAPI GET failed: {response.text}")
        return response.json()

    def get_user(self, user_name: str) -> User:
        json_data = self._get(f"users/@{user_name}")
        return User(json_data)

    def get_user_bests(self, user_id: str):
        return self._get(f"users/{user_id}/scores/best")

    def lookup_beatmap(self, checksum: str) -> Beatmap:
        json_data = self._get(f"beatmaps/lookup?checksum={checksum}")
        return Beatmap(json_data)

    def download_beatmap(self, beatmap_id: int) -> str:
        url = f"{OsuAPI.OSU_URL}/osu/{beatmap_id}"
        payload = {}
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise RuntimeError(f"OsuAPI GET failed: {response.text}")
        return response.text

    def _save_session(self, filename: str) -> None:
        """
        Saves current session data to file.
        DOES NOT CHECK IS THE SESSION ALIVE!
        """
        data = {
            "client_id": self.client_id,
            "token": self.access_token,
            "expires_at": self.token_expires_at,
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        logger.info("OsuAPI session saved")
