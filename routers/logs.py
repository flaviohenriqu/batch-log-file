from immudb import ImmudbClient

from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile

from deps import get_immudb_client, reuseable_oauth
from settings import get_settings, Settings
from tasks.logs import process_large_logs
from utils import chunked

router = APIRouter()


@router.post("/logs", summary="Batch log file", dependencies=[Depends(reuseable_oauth)])
async def load_logs(
    file: UploadFile,
    database: ImmudbClient = Depends(get_immudb_client),
    settings: Settings = Depends(get_settings),
):
    data = {}
    with file.file as content:
        for line in content.readlines():
            key = str(line).split("-", 1)[0].replace("b'", "").rstrip()
            data[key.encode("utf-8")] = line

    for chunk in chunked(data.items(), settings.chunk_size):
        response = database.setAll(chunk)
        assert type(response) != int

    return {"data": data, "total": len(data)}


@router.post("/logs/large", summary="Batch large log file", dependencies=[Depends(reuseable_oauth)])
async def large_logs(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    database: ImmudbClient = Depends(get_immudb_client),
    settings: Settings = Depends(get_settings),
):
    background_tasks.add_task(process_large_logs, file, database, settings.chunk_size)
    return {"message": f"starting processing file: {file.filename}"}


@router.get("/logs", summary="List logs", dependencies=[Depends(reuseable_oauth)])
async def list_logs(
    size: int = 100,
    database: ImmudbClient = Depends(get_immudb_client),
):
    return database.scan(b"", b"", True, size)


@router.get("/logs/history/{key}", summary="History log by key", dependencies=[Depends(reuseable_oauth)])
async def history_log(
    key: str,
    database: ImmudbClient = Depends(get_immudb_client),
):
    return database.history(key.encode("utf-8"), 0, 100, True)

