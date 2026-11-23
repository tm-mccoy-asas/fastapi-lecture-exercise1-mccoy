# Data Health Check API

*Mccoy Asas*

A simple FastAPI application that checks sample retail datasets for missing values and duplicate IDs.

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

## Endpoints

| Method | Endpoint | Description | Parameters |
|---|---|---|---|
| GET | `/health` | Checks if the API is running | None |
| GET | `/datasets` | Lists available datasets | None |
| GET | `/datasets/{dataset_id}/quality` | Checks for missing values and duplicate IDs | `dataset_id` (int, required) |

**Available datasets:**
- `1` — Customer Records
- `2` — Product Inventory

## Sample Usage

Test the endpoints using `curl`:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/datasets
curl http://localhost:8000/datasets/1/quality
curl http://localhost:8000/datasets/2/quality
```

Or run the Python client in a separate terminal:

```bash
python client.py
```

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

## Notes

- The API uses two hardcoded sample datasets.
- `missing_values` counts fields containing `None`.
- `duplicate_ids` counts repeated ID occurrences beyond the first.
- The API returns data quality results without modifying the datasets.