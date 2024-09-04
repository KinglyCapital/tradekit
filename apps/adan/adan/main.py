from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adan.routers import prices_router

app = FastAPI()

app.include_router(prices_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="__main__:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
