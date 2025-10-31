from core.errors import HosuError


class OsuAPIError(HosuError):
    pass


class OsuAPIAuthError(OsuAPIError):
    pass
