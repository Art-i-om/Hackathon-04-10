from fastapi import FastAPI
from json import dumps
from csv import DictReader

app = FastAPI()


def read_csv_file_by_id(sharkId: int):
    res = []
    with open(f"sharksData/{sharkId}.csv", "r") as f:
        data = DictReader(f)
        for row in data:
            del row["lc"]
            res.append(row)

    res = dumps(res)
    # with open(f"{sharkId}.json", "w", encoding="utf-8") as out:
    #     out.write(res)

    return res


@app.get("/data/all")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/data/{sharkId}")
def read_item(name: str):
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    read_csv_file_by_id(1)
