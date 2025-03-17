import os
from dotenv import load_dotenv
load_dotenv()

import requests
import logging

logger = logging.getLogger(__name__)

YOUR_GENERATED_SECRET = os.getenv("SCENEX_API_KEY")

SCENEX_API_URL = "https://api.scenex.jina.ai/v1/describe"

headers = {
    "x-api-key": f"token {YOUR_GENERATED_SECRET}",
    "content-type": "application/json"
}


def describe_image(data):
    YOUR_GENERATED_SECRET = 'yBmfxlQk3kjaT01klugL:5005bd6d856a544d043c3a64bb82447b12c7149442be05441bba4dd09f3ca97b'

    url = "https://api.scenex.jina.ai/v1/describe"

    headers = {
        "x-api-key": f"token {YOUR_GENERATED_SECRET}",
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()

        print("==== Success ====")
        result = response.json().get('result', [])
        if result:
            return result[0].get('text', 'No text found')
        else:
            return "No result found"

    except requests.exceptions.RequestException as e:
        return None
