from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings

app = FastAPI(
    title='Smart Content Summarizer AI',
    description='API para raspagem e sumarização de artigos usando Gemini 1.5 Flash',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='[http://localhost:3000]',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {
        'status': 'outline',
        'message': 'Smart Content Summarizer API is running sucessfully!'
    }