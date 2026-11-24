import os
import requests
from dotenv import load_dotenv

load_dotenv()

FASTAPI_ENDPOINT_URL = os.getenv("FASTAPI_ENDPOINT_URL")


def GET_ENDPOINT(route: str):
    full_route = f"{FASTAPI_ENDPOINT_URL}{route}"
    print(f"GET {full_route}")

    res = requests.get(full_route)
    print(res.status_code)
    print(res.json())

    return res


GET_ENDPOINT("/health")
GET_ENDPOINT("/datasets")
GET_ENDPOINT("/datasets/1")
GET_ENDPOINT("/datasets/2")
GET_ENDPOINT("/datasets/1/quality")
GET_ENDPOINT("/datasets/2/quality")