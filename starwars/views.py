import asyncio
import time

import httpx
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .fetch import fetch_url, fetch_async_url

# Create your views here.

STARWARS_API_URL = 'https://swapi.dev/api'
ENDPOINTS = ['people', 'starships', 'planets']


def starwars_sync_view(request: HttpRequest) -> HttpResponse:
    people_urls = [f'{STARWARS_API_URL}/people/{idx}' for idx in range(1, 11)]
    starship_urls = [f'{STARWARS_API_URL}/starships/{idx}' for idx in range(1, 11)]
    planet_urls = [f'{STARWARS_API_URL}/planets/{idx}' for idx in range(1, 11)]
    url_lists = [people_urls, starship_urls, planet_urls]

    data = []
    start_time = time.time()
    # I/O bound code
    with httpx.Client() as client:
        for url_list in url_lists:
            entities = []
            for url in url_list:
                endpoint_data = fetch_url(client, url)
                entities.append(endpoint_data)
            data.append(entities)

    took_time = time.time() - start_time
    people, starships, planets = data
    context = {'people': people, 'starships': starships, 'planets': planets, 'took_time': took_time}
    return render(request, 'starwars/list.html', context)


async def starwars_async_view(request: HttpRequest) -> HttpResponse:
    urls = [f'{STARWARS_API_URL}/{endpoint}' for endpoint in ENDPOINTS]

    tasks = []
    # Async (concurrent) I/O bound code
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        for url in urls:
            task = asyncio.create_task(fetch_async_url(client, url))
            tasks.append(task)
        data = await asyncio.gather(*tasks)

    took_time = time.time() - start_time

    # Processing of already loaded data
    results = []
    for chunk in data:
        result = chunk['results']
        results.append(result)

    people, starships, planets = results
    context = {'people': people, 'starships': starships, 'planets': planets, 'took_time': took_time}
    return render(request, 'starwars/list.html', context)
