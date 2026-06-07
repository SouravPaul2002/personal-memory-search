from fastapi import FastAPI

from backend.api.status import router as status_router
from backend.api.search import router as search_router
from backend.api.scan import router as scan_router

app = FastAPI(
    title="Personal Memory Search Engine"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Personal Memory Search Engine API!"
    }

app.include_router(status_router)
app.include_router(search_router)
app.include_router(scan_router)