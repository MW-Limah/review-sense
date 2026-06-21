from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import router as api_router

app = FastAPI(
    title="Smart Content Summarizer AI",
    description="API for scraping and summarizing articles using Gemini 1.5 Flash",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Smart Content Summarizer API is running successfully!"
    }
