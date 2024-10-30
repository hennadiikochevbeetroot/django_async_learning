from httpx import AsyncClient, Client


def fetch_url(client: Client, url: str) -> dict | list:
    response = client.get(url)
    return response.json()


async def fetch_async_url(client: AsyncClient, url: str) -> dict | list:
    response = await client.get(url)
    return response.json()
