from fastapi import FastAPI, HTTPException

app = FastAPI()


datasets = {
    1: {
        "name": "Customer Records",
        "records": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": None},
            {"id": 2, "name": "Bob", "email": None},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ]
    },
    2: {
        "name": "Product Inventory",
        "records": [
            {"id": 1, "name": "Laptop", "price": 45000},
            {"id": 2, "name": "Mouse", "price": 500},
            {"id": 3, "name": "Keyboard", "price": None}
        ]
    }
}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Data Health Check API is running"
    }


@app.get("/datasets")
def get_datasets():
    return [
        {
            "id": dataset_id,
            "name": dataset["name"],
            "total_records": len(dataset["records"])
        }
        for dataset_id, dataset in datasets.items()
    ]


@app.get("/datasets/{dataset_id}/quality")
def get_data_quality(dataset_id: int):
    dataset = datasets.get(dataset_id)

    if dataset is None:
        raise HTTPException(404, "Dataset not found")

    records = dataset["records"]

    total_records = len(records)

    missing_values = sum(
        value is None
        for record in records
        for value in record.values()
    )

    ids = [record["id"] for record in records]
    duplicate_ids = len(ids) - len(set(ids))

    return {
        "dataset": dataset["name"],
        "total_records": total_records,
        "missing_values": missing_values,
        "duplicate_ids": duplicate_ids
    }