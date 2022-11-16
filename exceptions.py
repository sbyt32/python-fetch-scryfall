import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
log = logging.getLogger()

class frank_exception(Exception):
    def __init__(self):
        pass

@app.exception_handler(frank_exception)
async def frank_exception_handler(request: Request, exc: frank_exception): # Yes, 'request: Request' is required.
    return JSONResponse(
        status_code=400,
        content={
            "resp": "error",
            "status": 400,
            "message": "The request failed due to being at root. If you're just testing if it works, yeah it works.",
        }
    )