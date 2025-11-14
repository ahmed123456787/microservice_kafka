import httpx
from .http_methods import HttpMethod

async def proxy_request(
        method: HttpMethod,
        url: str,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
    ) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body
        )
    return response