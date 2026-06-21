from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from src.config.settings import settings


# Define the exact structure we want the AI to return
class SummaryResponse(BaseModel):
    title: str = Field(description="The clear and compelling headline of the article.")
    summary: str = Field(description="An executive summary consisting of 2 to 3 detailed paragraphs.")
    key_takeaways: list[str] = Field(description="An array containing up to 5 bullet points of the most crucial insights.")
    estimated_reading_time: str = Field(description="Estimated reading time of the original text (e.g., '5 min read').")

# Initialize the Gemini Client passing our API key from settings
client = genai.Client(api_key=settings.gemini_api_key)

async def generate_ai_summary(article_text: str) -> SummaryResponse:
    prompt = f"""
    You are an experienced software engineer and technical researcher.
    Analyze the extracted web content below and generate a professional and highly accurate summary, using simple language.
    Source Text:
    {article_text}
    """

    try:
        # Requesting content from Gemini 1.5 Flash
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SummaryResponse, # Forces Gemini to strictly follow our Pydantic model structure
                temperature=0.3, # Keeps the model focused and deterministic
            ),
        )

        # Validate and parse the JSON string response back into our Pydantic Model object
        parsed_response = SummaryResponse.model_validate_json(response.text)
        return parsed_response

    except Exception as e:
        # Standard error handling if the API fails or validation breaks
        raise ValueError(f"Gemini API or Validation Error: {str(e)}")
