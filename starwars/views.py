import time

import httpx
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .fetch import fetch_url

# Create your views here.

STARWARS_API_URL = 'https://swapi.dev/api'
ENDPOINTS = ['people', 'starships', 'planets']


def starwars_sync_view(request: HttpRequest) -> HttpResponse:
    urls = [f'{STARWARS_API_URL}/{endpoint}' for endpoint in ENDPOINTS]
    data = []

    start_time = time.time()
    # I/O bound code
    with httpx.Client() as client:
        for url in urls:
            endpoint_data = fetch_url(client, url)
            results = endpoint_data['results']
            data.append(results)

    took_time = time.time() - start_time

    people, starships, planets = data
    context = {'people': people, 'starships': starships, 'planets': planets, 'took_time': took_time}
    return render(request, 'starwars/list.html', context)


async def starwars_async_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse()
