import os
import json
from typing import Dict, Any, Optional
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from utils.logger import logger

class GroqClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = AsyncGroq(api_key=self.api_key)
        self.model = model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(f"Retrying Groq API call... Attempt {retry_state.attempt_number}")
    )
    async def generate_completion(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            logger.info(f"Groq API Success | Tokens: {usage.total_tokens} (Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens})")
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            raise
