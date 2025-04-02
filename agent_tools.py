import http.client
import json
from pydantic_ai import RunContext


async def query_streaming_availability(title: str) -> str:
    """Query the streaming availability for the given title.

    Args:
        title: The title of the movie or TV show.

    Returns:
        A string message with streaming information.
    """
    conn = http.client.HTTPSConnection("streaming-availability.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY",
        'x-rapidapi-host': "streaming-availability.p.rapidapi.com"
    }

    conn.request("GET", f"/shows/title/{title}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    availability = json.loads(data.decode("utf-8"))

    if availability:
        return f"{title} is available on {', '.join(availability.get('services', []))}."
    else:
        return f"{title} is not available on any streaming services. We are sorry :)"