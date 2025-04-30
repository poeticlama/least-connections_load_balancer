import asyncio
import time

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import argparse

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

@app.get('/images/{id}')
async def get_fast(id: int):
    path = os.path.join(current_dir, f'image{id}.jpg')
    if id == 1:
        time.sleep(1)
    elif id == 2:
        time.sleep(3)
    elif id == 3:
        time.sleep(5)
    elif id == 4:
        time.sleep(10)
    return FileResponse(path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    uvicorn.run('main:app', reload=True, port=args.port)