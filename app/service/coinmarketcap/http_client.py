from aiohttp import ClientSession


class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url, headers={"X-CMC_PRO_API_KEY": api_key}
        )

    async def close_session(self):
        await self._session.close()
        self._session = None
