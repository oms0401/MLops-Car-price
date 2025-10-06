from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app : FastAPI):
    @app.exception_handler(Exception)
    async def unhandled_exception(request : Request, exc : Exception):
        return JSONResponse(status_code=500, content={'detail':str(exc)})
