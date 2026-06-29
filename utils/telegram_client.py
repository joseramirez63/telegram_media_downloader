"""Centralized TelegramClient factory."""

from typing import Optional

from telethon import TelegramClient

from utils.meta import APP_VERSION, DEVICE_MODEL, LANG_CODE, SYSTEM_VERSION


def build_telegram_client(
    api_id: int,
    api_hash: str,
    *,
    session_name: str = "media_downloader",
) -> TelegramClient:
    """Build a TelegramClient with the standard device metadata.

    Parameters
    ----------
    api_id: int
        Telegram API ID.
    api_hash: str
        Telegram API hash.
    session_name: str
        Session file name (default: ``"media_downloader"``).

    Returns
    -------
    TelegramClient
        A Telethon client instance (not yet connected).
    """
    return TelegramClient(
        session_name,
        api_id=api_id,
        api_hash=api_hash,
        device_model=DEVICE_MODEL,
        system_version=SYSTEM_VERSION,
        app_version=APP_VERSION,
        lang_code=LANG_CODE,
    )
