import asyncio
from concurrent.futures import ThreadPoolExecutor

from deep_translator import GoogleTranslator as GT

executor = ThreadPoolExecutor(max_workers=3)

def _execute_translation(text: str, target_lang: str) -> str:
    return GT(source="auto", target=target_lang).translate(text)

async def translate_text(text:str, target_lang: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, _execute_translation, text, target_lang)
