from fastapi import FastAPI
from json import dumps
from csv import DictReader
import os

app = FastAPI()


def read_csv_file_by_id(sharkId: int):
    res = []
    with open(f"sharksData/{sharkId}.csv", "r") as f:
        data = DictReader(f)
        for row in data:
            del row["lc"]
            res.append(row)

    # res = dumps(res)
    # with open(f"{sharkId}.json", "w", encoding="utf-8") as out:
    #     out.write(res)

    return res


def read_all_data():
    res = []
    for sharkId in sorted([int(fileName.split(".")[0]) for fileName in os.listdir("sharksData")]):
        res.append(read_csv_file_by_id(sharkId))
    return res


@app.get("/data/all")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/data/{sharkId}")
def read_item(name: str):
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    read_csv_file_by_id(1)
    data = dumps(read_all_data())
    with open(f"data.json", "w", encoding="utf-8") as out:
        out.write(data)
