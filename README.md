# Data Health Check API

A simple FastAPI application that checks sample datasets for missing values and duplicate IDs.

## Endpoints

| Method | Endpoint | Description | Parameters |
|---|---|---|---|
| GET | `/health` | Checks if the API is running | None |
| GET | `/datasets` | Lists available datasets | None |
| GET | `/datasets/{dataset_id}/quality` | Checks for missing values and duplicate IDs | `dataset_id` (int) |

## Sample Usage

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

Test the endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/datasets
curl http://localhost:8000/datasets/1/quality
curl http://localhost:8000/datasets/2/quality
```

Or run the Python client:

```bash
python client.py
```

## Sample Output

**GET `/health`**
```json
{
    "status": "healthy",
    "message": "Data Health Check API is running"
}
```

**GET `/datasets`**
```json
[
    {"id": 1, "name": "Customer Records", "total_records": 4},
    {"id": 2, "name": "Product Inventory", "total_records": 3}
]
```

**GET `/datasets/1/quality`**
```json
{
    "dataset": "Customer Records",
    "total_records": 4,
    "missing_values": 2,
    "duplicate_ids": 1
}
```

**GET `/datasets/2/quality`**
```json
{
    "dataset": "Product Inventory",
    "total_records": 3,
    "missing_values": 1,
    "duplicate_ids": 0
}
```