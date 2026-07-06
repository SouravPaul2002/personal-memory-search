from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.schema import initialize_database
from backend.api.status import router as status_router
from backend.api.search import router as search_router
from backend.api.scan import router as scan_router
from backend.api.upload import router as upload_router
from backend.api.files import router as files_router

app = FastAPI(
    title="Personal Memory Search Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()
@app.get("/")
def root():
    return {
        "message": "Welcome to the Personal Memory Search Engine API!"
    }

app.include_router(status_router)
app.include_router(search_router)
app.include_router(scan_router)
app.include_router(upload_router)
app.include_router(files_router)