import os
import requests
from dotenv import load_dotenv

load_dotenv()
FASTAPI_ENDPOINT_URL = os.getenv("FASTAPI_ENDPOINT_URL")


def request_api(method, route, payload=None):
    url = f"{FASTAPI_ENDPOINT_URL}{route}"

    try:
        response = requests.request(method, url, json=payload, timeout=10)

        print(f"{method} {route}: {response.status_code}")

        if response.content:
            print(response.json())

        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")


# test existing GET endpoints
request_api("GET", "/health")
request_api("GET", "/datasets")
request_api("GET", "/datasets/1/quality")

# Test POST
created = request_api("POST", "/datasets", {
    "name": "Sales Records",
    "records": [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": None},
        {"id": 2, "amount": 750}
    ]
})

if created:
    dataset_id = created.json()["id"]

    # test PATCH
    request_api("PATCH", f"/datasets/{dataset_id}", {
        "records": [
            {"id": 1, "amount": 500},
            {"id": 2, "amount": 650},
            {"id": 3, "amount": 750}
        ]
    })

    # check updated quality
    request_api("GET", f"/datasets/{dataset_id}/quality")

    # test DELETE
    request_api("DELETE", f"/datasets/{dataset_id}")

    # confirm deletion returns 404
    request_api("GET", f"/datasets/{dataset_id}")

# test nonexistent dataset
request_api("GET", "/datasets/999")