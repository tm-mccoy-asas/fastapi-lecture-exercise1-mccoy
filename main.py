import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Dataset(BaseModel):
    name: str
    records: list[dict]

class DatasetUpdate(BaseModel):
    name: str | None = None
    records: list[dict] | None = None

DATASETS_PATH = Path(__file__).with_name("datasets.json")


def load_datasets():
    with open(DATASETS_PATH, "r") as file:
        data = json.load(file)

    return {int(dataset_id): dataset for dataset_id, dataset in data.items()}


def save_datasets():
    with open(DATASETS_PATH, "w") as file:
        json.dump(datasets, file, indent=4)


datasets = load_datasets()


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

@app.post("/datasets", status_code=status.HTTP_201_CREATED)
def create_dataset(payload: Dataset):
    if any(dataset["name"] == payload.name for dataset in datasets.values()):
        raise HTTPException(409, "Dataset name already exists")

    new_id = max(datasets.keys(), default=0) + 1

    datasets[new_id] = payload.model_dump()
    save_datasets()

    return {"id": new_id, **datasets[new_id]}

@app.patch("/datasets/{dataset_id}")
def update_dataset(dataset_id: int, payload: DatasetUpdate):
    dataset = datasets.get(dataset_id)

    if dataset is None:
        raise HTTPException(404, "Dataset not found")

    changes = payload.model_dump(exclude_unset=True)

    if any(value is None for value in changes.values()):
        raise HTTPException(422, "Dataset fields cannot be null")

    if "name" in changes:
        if any(
            item["name"] == changes["name"]
            for item_id, item in datasets.items()
            if item_id != dataset_id
        ):
            raise HTTPException(409, "Dataset name already exists")

    dataset.update(changes)
    save_datasets()

    return {"id": dataset_id, **dataset}

@app.delete("/datasets/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(dataset_id: int):
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")

    del datasets[dataset_id]
    save_datasets()

# new endpoint based on the feedback  
@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int):
    dataset = datasets.get(dataset_id)

    if dataset is None:
        raise HTTPException(404, "Dataset not found")

    return {"id": dataset_id, **dataset}


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

    ids = [record["id"] for record in records if "id" in record]
    duplicate_ids = len(ids) - len(set(ids))

    return {
        "dataset": dataset["name"],
        "total_records": total_records,
        "missing_values": missing_values,
        "duplicate_ids": duplicate_ids
    }