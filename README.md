# Data Health Check API

*Mccoy Asas*

A simple FastAPI application that manages sample retail datasets and checks for missing values and duplicate IDs. It supports CRUD operations and stores datasets in a JSON file.

## Setup

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file and add:

```env
FASTAPI_ENDPOINT_URL=http://localhost:8000
```

3. Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

4. Access FastAPI's interactive documentation at `http://localhost:8000/docs` to view and test the available endpoints.

## Endpoints

| Method | Endpoint | Description | Parameters |
|---|---|---|---|
| GET | `/health` | Checks if the API is running | None |
| GET | `/datasets` | Lists available datasets | None |
| GET | `/datasets/{dataset_id}` | Retrieves a specific dataset | `dataset_id` (int, required) |
| GET | `/datasets/{dataset_id}/quality` | Checks for missing values and duplicate IDs | `dataset_id` (int, required) |
| POST | `/datasets` | Creates a new dataset | `name` (str), `records` (list) |
| PATCH | `/datasets/{dataset_id}` | Updates a dataset's name or records | `dataset_id` (int), `name` or `records` (optional) |
| DELETE | `/datasets/{dataset_id}` | Deletes a dataset | `dataset_id` (int, required) |

**Default datasets:**
- `1` — Customer Records
- `2` — Product Inventory

Additional datasets can be created using the POST endpoint. Dataset IDs are generated automatically.

## Sample Usage

Test the GET endpoints using `curl`:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/datasets
curl http://localhost:8000/datasets/1
curl http://localhost:8000/datasets/1/quality
curl http://localhost:8000/datasets/2/quality
```

Create a new dataset using POST:

```bash
curl -X POST http://localhost:8000/datasets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Records",
    "records": [
      {"id": 1, "amount": 500},
      {"id": 2, "amount": null},
      {"id": 2, "amount": 750}
    ]
  }'
```

Update the dataset using PATCH:

```bash
curl -X PATCH http://localhost:8000/datasets/3 \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"id": 1, "amount": 500},
      {"id": 2, "amount": 650},
      {"id": 3, "amount": 750}
    ]
  }'
```

Check the updated data quality:

```bash
curl http://localhost:8000/datasets/3/quality
```

Delete the dataset using DELETE:

```bash
curl -X DELETE http://localhost:8000/datasets/3
```

**Note:** The examples above assume the newly created dataset is assigned ID `3`. The actual ID may differ if additional datasets already exist.

Alternatively, run the Python client in a separate terminal:

```bash
python client.py
```

The Python client tests the CRUD operations and handles HTTP errors using the `requests` module.

## Sample Output

### GET `/health`

```json
{
    "status": "healthy",
    "message": "Data Health Check API is running"
}
```

### GET `/datasets`

```json
[
    {"id": 1, "name": "Customer Records", "total_records": 4},
    {"id": 2, "name": "Product Inventory", "total_records": 3}
]
```

### GET `/datasets/1/quality`

```json
{
    "dataset": "Customer Records",
    "total_records": 4,
    "missing_values": 2,
    "duplicate_ids": 1
}
```

### GET `/datasets/2/quality`

```json
{
    "dataset": "Product Inventory",
    "total_records": 3,
    "missing_values": 1,
    "duplicate_ids": 0
}
```

### POST `/datasets`

```json
{
    "id": 3,
    "name": "Sales Records",
    "records": [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": null},
        {"id": 2, "amount": 750}
    ]
}
```

### PATCH `/datasets/3`

```json
{
    "id": 3,
    "name": "Sales Records",
    "records": [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 650},
        {"id": 3, "amount": 750}
    ]
}
```

### GET `/datasets/3/quality` (After PATCH)

```json
{
    "dataset": "Sales Records",
    "total_records": 3,
    "missing_values": 0,
    "duplicate_ids": 0
}
```

### DELETE `/datasets/3`

Returns `204 No Content` when the dataset is successfully deleted.

## Notes

- The API starts with two sample datasets stored in `datasets.json`.
- New datasets and changes are saved to `datasets.json`.
- Dataset IDs are generated automatically when creating new datasets.
- `missing_values` counts fields containing `None` (or `null` in JSON).
- `duplicate_ids` counts repeated ID occurrences beyond the first, ignoring records without an `id` field.
- PATCH updates the dataset name or replaces its records without changing unspecified fields.
- The quality-check endpoint returns results without modifying the datasets.
- The API returns `404` for nonexistent datasets, `409` for duplicate dataset names, and `422` for invalid requests.
- The Python client uses `requests` to test CRUD operations and handle HTTP errors.