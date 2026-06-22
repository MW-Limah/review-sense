from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import SavedSummary  # Certifique-se de herdar a classe que criamos no passo anterior
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
    description="Takes a URL, extracts core content, checks SQLite cache, and uses Gemini if not cached."
)
async def summarize_url(payload: SummaryRequest, db: AsyncSession = Depends(get_db)):
    url_str = str(payload.url)

    try:
        # 1. Busca na "Memória" do banco de dados (SQLite)
        result = await db.execute(select(SavedSummary).where(SavedSummary.url == url_str))
        cached_summary = result.scalar_one_or_none()

        if cached_summary:
            # Se já foi sumarizado antes, retorna o histórico imediatamente
            return {
                "title": cached_summary.title,
                "summary": cached_summary.summary,
                "key_takeaways": cached_summary.key_takeaways,
                "estimated_reading_time": cached_summary.estimated_reading_time
            }

        # 2. Se for um link novo, faz o fluxo tradicional de raspagem
        clean_text = await extract_article_content(url_str)

        # 3. Executa a inteligência artificial do Gemini
        ai_analysis = await generate_ai_summary(clean_text)

        # 4. Salva o resultado no banco para futuras requisições do mesmo link
        new_cache = SavedSummary(
            url=url_str,
            title=ai_analysis.title,          # Acessa os atributos baseados na sua classe SummaryResponse
            summary=ai_analysis.summary,
            key_takeaways=ai_analysis.key_takeaways,
            estimated_reading_time=ai_analysis.estimated_reading_time
        )
        db.add(new_cache)
        await db.commit()

        return ai_analysis

    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(val_err)
        )
