from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from src.services.gemini import SummaryResponse, generate_ai_summary
from src.services.scraper import extract_article_content

router = APIRouter(prefix="/api/v1", tags=["Summarizer"])

class SummaryRequest(BaseModel):
    url: HttpUrl

@router.post(
    "/summarize",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Scrape and summarize a web article",
    description="Takes a URL, extracts the core content, and uses Gemini to generate a structured JSON summary."
)
async def summarize_url(payload: SummaryRequest):
    clean_text = await extract_article_content(str(payload.url))

    try:
        # Awaiting our newly refactored fully asynchronous Gemini service
        ai_analysis = await generate_ai_summary(clean_text)
        return ai_analysis

    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(val_err)
        )
