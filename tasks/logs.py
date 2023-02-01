import logging

from immudb_logging.handlers import ImmudbHandler
from utils import chunked

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
handler = ImmudbHandler("immudb", "3322")
logger = logging.getLogger('immudbHandler')
logger.addHandler(handler)


def process_large_logs(file, database, chunk_size: int = 100):
    logger.info(f"Starting process log file: {file.filename}")
    data = {}
    with file.file as content:
        for line in content.readlines():
            key = str(line).split("-", 1)[0].replace("b'", "").rstrip()
            data[key.encode("utf-8")] = line

    for chunk in chunked(data.items(), chunk_size):
        response = database.setAll(chunk)
        assert type(response) != int

    logger.info(f"total saved: {len(data)}")
