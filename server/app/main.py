import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

@app.get('/speed/{seconds}')
async def get_fast(seconds: int):
    path = os.path.join(current_dir, 'image.jpg')
    await asyncio.sleep(seconds)
    return FileResponse(path)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)