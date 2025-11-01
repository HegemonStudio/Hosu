import time

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR   = 60 * SECONDS_PER_MINUTE
SECONDS_PER_DAY    = 24 * SECONDS_PER_HOUR

def format_token_expiry(expiry_timestamp: float) -> str:
    """
    Returns a human-readable string like:
    "Token expires in 2 hours and 5 minutes."
    """
    now = time.time()
    remaining_secs = int(expiry_timestamp - now)

    if remaining_secs <= 0:
        return "Token has expired."

    days, rem_secs = divmod(remaining_secs, SECONDS_PER_DAY)
    hours, rem_secs = divmod(rem_secs, SECONDS_PER_HOUR)
    minutes, seconds = divmod(rem_secs, SECONDS_PER_MINUTE)

    parts = []
    if days:
        parts.append(f"{days} day{"s" if days != 1 else ""}")
    if hours:
        parts.append(f"{hours} hour{"s" if hours != 1 else ""}")
    if minutes:
        parts.append(f"{minutes} minute{"s" if minutes != 1 else ""}")
    if seconds and not days:
        parts.append(f"{seconds} second{"s" if seconds != 1 else ""}")

    formatted = ", ".join(parts)
    return f"Token expires in {formatted}"
